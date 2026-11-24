"""vend-1125: vending machine pickup line; gate 200 chars."""

import json
import os
import pathlib
import sys

CAP = 200


def stock_shelf():
    kiosk = pathlib.Path(__file__).resolve().parent
    tray = (kiosk / "entry.txt").read_text(encoding="utf-8")
    return kiosk, [g for g in (row.strip() for row in tray.splitlines()) if g]


def dispense(line):
    if not line:
        sys.exit("vend error: empty tray")
    if len(line) > CAP:
        sys.exit("vend error: %d chars jam slot (cap %d)" % (len(line), CAP))
    return line


def vend_out(kiosk, line):
    lane = pathlib.Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or kiosk)
    lane.mkdir(parents=True, exist_ok=True)
    drop = lane / "entry.txt"
    drop.write_text(line + "\n", encoding="utf-8", newline="\n")
    return drop


kiosk, tray = stock_shelf()
line = dispense(tray[0] if tray else "")
drop = vend_out(kiosk, line)
print(json.dumps({"slot": drop.as_posix(), "chars": len(line), "jam": len(line) > CAP, "mode": "pickup", "dispensed": True}))
