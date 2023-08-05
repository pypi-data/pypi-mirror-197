#!/usr/bin/env python3
import os
import subprocess

from siriushlacon.agilent4uhv.consts import AGILENT_OVERVIEW

os.environ["PYDM_DEFAULT_PROTOCOL"] = "ca://"
macros = (
    '\'{"device": "UHV", "TYPE": "SI", "FORMAT": "EXP", '
    ' "TITLE": "ION Pump Agilent 4UHV - SI"}\''
)

subprocess.Popen(
    "pydm --hide-nav-bar -m " + macros + " " + AGILENT_OVERVIEW, shell=True
)
