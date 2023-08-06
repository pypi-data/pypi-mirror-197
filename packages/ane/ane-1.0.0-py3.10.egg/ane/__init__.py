# SPDX-License-Identifier: MIT
# Copyright 2022 Eileen Yoon <eyn@gmx.com>

import ctypes
from ctypes import c_void_p, c_int, c_long, byref
from ctypes import create_string_buffer

import atexit
import numpy as np
from copy import deepcopy


TILE_COUNT = 0x20

class ANE:
	def __init__(self, path):
		self.lib = ctypes.cdll.LoadLibrary(path)
		self.lib.pyane_free.argtypes = [c_void_p]
		self.lib.pyane_exec.argtypes = [c_void_p]
		self.lib.pyane_send.argtypes = [c_void_p] + [c_void_p] * TILE_COUNT
		self.lib.pyane_read.argtypes = [c_void_p] + [c_void_p] * TILE_COUNT
		self.lib.pyane_tile.argtypes = [c_void_p] + [c_void_p, c_void_p, c_int]
		self.lib.pyane_info.argtypes = [c_void_p] + [ctypes.POINTER(c_int)] * 2
		self.lib.pyane_size.argtypes = [c_void_p] + [ctypes.POINTER(c_long)] * 1 * TILE_COUNT * 2
		self.lib.pyane_nchw.argtypes = [c_void_p] + [ctypes.POINTER(c_long)] * 6 * TILE_COUNT * 2
		self.handles = {}
		atexit.register(self.cleanup)

	def cleanup(self):
		for handle in self.handles:
			self.lib.pyane_free(handle)

	def register(self, model):
		handle = model.initf()
		if (handle == None): raise RuntimeError("driver error")
		self.handles[handle] = handle
		model.handle = handle


class ANE_MODEL:
	def runtime(self, path):
		self.ane = ANE(path)

	def register(self, initf):
		self.initf = initf
		self.initf.restype = c_void_p
		self.ane.register(self)

		info = [ctypes.c_int() for x in range(2)]
		self.ane.lib.pyane_info(self.handle, *[byref(info[n]) for n in range(len(info))])
		self.src_count, self.dst_count = [info[n].value for n in range(len(info))]

		size = [ctypes.c_long() for x in range(TILE_COUNT * 1 * 2)]
		self.ane.lib.pyane_size(self.handle, *[byref(size[n]) for n in range(len(size))])
		self.src_size = tuple([size[n].value for n in range(self.src_count)])
		self.dst_size = tuple([size[n].value for n in range(TILE_COUNT, TILE_COUNT + self.dst_count)])

		nchw = [ctypes.c_long() for x in range(TILE_COUNT * 6 * 2)]
		self.ane.lib.pyane_nchw(self.handle, *[byref(nchw[n]) for n in range(len(nchw))])
		self.src_nchw = tuple([tuple(x.value for x in nchw[n*6:(n+1)*6]) for n in range(self.src_count)])
		self.dst_nchw = tuple([tuple(x.value for x in nchw[n*6:(n+1)*6]) for n in range(TILE_COUNT, TILE_COUNT + self.dst_count)])

		self.outputs = [create_string_buffer(self.dst_size[idx]) for idx in range(self.dst_count)] + [b''] * (TILE_COUNT - self.dst_count)

	def predict(self, inputs):
		assert(len(inputs) == self.src_count)
		padded = inputs + [b''] * (TILE_COUNT - self.src_count)
		self.ane.lib.pyane_send(self.handle, *padded)
		self.ane.lib.pyane_exec(self.handle)
		self.ane.lib.pyane_read(self.handle, *self.outputs)
		return deepcopy(self.outputs[:self.dst_count])

	def arr2tile(self, arr, idx):
		assert((arr.dtype == np.float16) and (arr.shape == self.src_nchw[idx][:4]))
		data = arr.tobytes(order='C')
		tile = create_string_buffer(self.src_size[idx])
		self.ane.lib.pyane_tile(self.handle, data, tile, idx)
		return tile

	def tile2arr(self, tile, idx):
		N, C, H, W, P, R = self.dst_nchw[idx]
		new_N, new_C, new_H, new_W = N, C, P//R, R//2
		arr = np.frombuffer(tile, dtype=np.float16)[:new_N*new_C*new_H*new_W]
		return arr.reshape((new_N, new_C, new_H, new_W))[:N, :C, :H, :W]

	def tile(self, inarrs):  # list of numpy arrays
		return [self.arr2tile(inarrs[idx], idx) for idx in range(self.src_count)]

	def untile(self, outtiles):  # list of bytes tiles
		return [self.tile2arr(outtiles[idx], idx) for idx in range(self.dst_count)]
