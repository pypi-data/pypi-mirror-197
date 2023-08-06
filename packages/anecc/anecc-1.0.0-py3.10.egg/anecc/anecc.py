#!/usr/bin/python3

# SPDX-License-Identifier: MIT
# Copyright 2022 Eileen Yoon <eyn@gmx.com>

import os
import shlex
import shutil
import logging
import tempfile
import subprocess
import argparse

from anect import anec_convert
from anect import anec_whdr, anec_wbin

logging.basicConfig()
logger = logging.getLogger('anecc')
logger.setLevel(logging.INFO)

CC = "gcc"
PYTHON_HDR = "/usr/include/python3.10"
LIBDRM_HDR = "/usr/include/libdrm"
DRIVER_HDR = "/home/eileen/ane/ane/src/include"
ANELIB_HDR = "/home/eileen/ane/anelib/include"
ANELIB_OBJ = "/home/eileen/ane/build/anelib.o"


def anecc_compile(hwxpath, name="model", outdir=""):

	res = anec_convert(hwxpath, name=name)
	name = res.name  # override with sanitized name

	if (not outdir):
		outdir = os.getcwd()

	with tempfile.TemporaryDirectory() as tmpdir:
		os.chdir(tmpdir)

		anec_hdr = anec_whdr(res, prefix=tmpdir)
		anec_bin = anec_wbin(res, prefix=tmpdir)

		anec_obj = f'{name}.anec.o'
		cmd = f'ld -r -b binary -o {anec_obj} {anec_bin}'
		logger.info(cmd)
		subprocess.run(shlex.split(cmd))

		pyane_src = os.path.join(tmpdir, f'pyane_{name}.c')
		pyane_obj = os.path.join(tmpdir, f'pyane_{name}.so')
		with open(pyane_src, "w") as f:
			f.write(f'#include "pyane.h"\n')
			f.write(f'#include "{anec_hdr}"\n')

		cmd = f'{CC} -shared -pthread -fPIC -fno-strict-aliasing \
			-I. -Wall -Werror \
			-I/{PYTHON_HDR} -I/{LIBDRM_HDR} \
			-I/{DRIVER_HDR} -I/{ANELIB_HDR} \
			{ANELIB_OBJ} {anec_obj} \
			{pyane_src} -o {pyane_obj}'
		logger.info(cmd)
		subprocess.run(shlex.split(cmd))

		outpath = os.path.join(outdir, f'pyane_{name}.so')
		shutil.copyfile(pyane_obj, outpath)
		logger.info(f'created {outpath}')

	return


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='ane compiler')
	parser.add_argument('hwxpath', type=str, help='path to hwx')
	parser.add_argument('-n', '--name', type=str, help='name')
	parser.add_argument('-o', '--outdir', type=str, default='')
	args = parser.parse_args()

	anecc_compile(args.hwxpath, name=args.name, outdir=args.outdir)
