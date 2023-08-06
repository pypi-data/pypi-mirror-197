#!/usr/bin/python3

# SPDX-License-Identifier: MIT
# Copyright 2022 Eileen Yoon <eyn@gmx.com>

import click
from anect import anect_convert, anect_save, anect_print

@click.command()
@click.option('--path', '-i', required=True, type=str)
@click.option('--name', '-n', type=str)
@click.option('--outd', '-o', type=str, default='')
@click.option('--save', '-s', is_flag=True, show_default=True, default=False)
@click.option('--show', '-p', is_flag=True, show_default=True, default=False)
@click.option('--force', '-f', is_flag=True, show_default=True, default=False)
def run(path, name, outd, save, show, force):
	res = anect_convert(path, name, force)
	if (show):
		anect_print(res)
	if (save):
		anect_save(res, prefix=outd)
