#!/usr/bin/python3

# SPDX-License-Identifier: MIT
# Copyright 2022 Eileen Yoon <eyn@gmx.com>

import click
from anecc import anecc_compile

@click.command()
@click.option('--path', '-i', required=True, type=str)
@click.option('--name', '-n', type=str)
@click.option('--outd', '-o', type=str, default='')
def run(path, name, outd):
	anecc_compile(path, name, outd)
