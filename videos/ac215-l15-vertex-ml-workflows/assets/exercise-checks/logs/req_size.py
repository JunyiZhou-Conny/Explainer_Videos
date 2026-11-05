"""Check-only helper (NOT part of the tutorial). B1: how big is the request --predict sends for one
photo? Runs model-deployment-aws/cli.py's own lines 221-225 (open, RGB, resize 224x224, /255, the
{"instances": [...]} payload) on a sample photo, then serializes it the way the SDK's
JSONSerializer does for a dict (json.dumps). Also: the JPEG itself, and the JPEG base64-encoded
(what a bytes-in signature request would carry)."""
import base64
import json
import sys
import textwrap

import numpy as np  # noqa: F401  (used by the exec'd lines)
from PIL import Image  # noqa: F401

lines = open("/md/cli.py").read().splitlines(keepends=True)
snippet = textwrap.dedent("".join(lines[220:225]))
print("cli.py:221-225 as run:\n" + textwrap.indent(snippet.rstrip(), "  | "))
for img_path in sys.argv[1:]:
    ns = {"Image": Image, "np": np, "img_path": img_path}
    exec(snippet, ns)
    arr, payload = ns["arr"], ns["payload"]
    body = json.dumps(payload)
    jpeg = open(img_path, "rb").read()
    print(f"{img_path}: arr {arr.shape} {arr.dtype}, {arr.size:,} numbers; "
          f"JSON body {len(body):,} bytes ({len(body) / arr.size:.1f} bytes per number); "
          f"first numbers {body[15:60]}...")
    print(f"  the JPEG itself {len(jpeg):,} bytes; base64 {len(base64.b64encode(jpeg)):,} bytes; "
          f"JSON / JPEG = {len(body) / len(jpeg):,.0f}x")
