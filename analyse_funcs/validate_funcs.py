import os
import sys
from pathlib import Path
from typing import Tuple

from weather_funcs.appid_class import AppId


def validate_input(args) -> Tuple:
    """
    Analise args from command line
    """
    if not os.path.exists(args.input_file):
        sys.stderr.write(f"Cannot find file with hotels: invalid '{args.input_file}'")
        sys.exit(1)

    threads = args.threads if args.threads > 0 else 64
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    input_file = Path(args.input_file)
    appid_conductor = AppId(Path(args.appidpath))
    if args.appid:
        appid_conductor.add_appid(args.appid)

    return input_file, outdir, threads, appid_conductor.get_appid
