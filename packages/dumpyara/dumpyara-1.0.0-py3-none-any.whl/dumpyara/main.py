#
# Copyright (C) 2022 Dumpyara Project
#
# SPDX-License-Identifier: GPL-3.0
#

from argparse import ArgumentParser
from dumpyara import __version__ as version, current_path
from dumpyara.dumpyara import dumpyara
from dumpyara.utils.logging import setup_logging
from pathlib import Path
from sebaubuntu_libs.liblocale import setup_locale

def main():
	print(f"Dumpyara\n"
	      f"Version {version}\n")

	parser = ArgumentParser(prog='python3 -m dumpyara')

	# Main arguments
	parser.add_argument("file", type=Path,
						help="path to a device OTA")
	parser.add_argument("-o", "--output", type=Path, default=current_path / "working",
						help="custom output folder")

	# Optional arguments
	parser.add_argument("-d", "--debug", action='store_true',
						help="enable debugging features")

	args = parser.parse_args()

	setup_locale()

	setup_logging(args.debug)

	output_path = dumpyara(args.file, args.output, args.debug)

	print(f"\nDone! You can find the dump in {str(output_path)}")
