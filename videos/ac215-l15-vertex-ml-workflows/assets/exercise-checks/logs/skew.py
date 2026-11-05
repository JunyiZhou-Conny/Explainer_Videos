"""Check-only helper (NOT part of the tutorial). D4: three ways this tutorial turns one JPEG into
224x224x3 floats in [0, 1]. Each path runs the repo's own lines:
  client   model-deployment-aws/cli.py:221-223 (Pillow: RGB, resize, /255)   -> Part A's request
  records  ml-workflow-aws/src/data-processor/tfrecords.py create_tf_example (decode, resize, cast to
           uint8) then task.py's parse + normalize (/255)                       -> what training sees
  serving  task.py:277-281 preprocess_image (decode, convert_image_dtype, resize) -> Part B's signature
and compares them, value by value."""
import ast
import os
import sys
import textwrap

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
sys.path.insert(0, "/checks")
import numpy as np  # noqa: E402
import tensorflow as tf  # noqa: E402
from PIL import Image  # noqa: E402
import stubs  # noqa: E402

stubs.install()  # after TensorFlow: dask and sklearn are not installed; tfrecords.py imports them, create_tf_example does not use them

sys.path.insert(0, "/src/data-processor")
import tfrecords  # noqa: E402

task = open("/src/model-training/package/trainer/task.py").read()
fn = next(n for n in ast.parse(task).body if isinstance(n, ast.FunctionDef) and n.name == "preprocess_image")
ns = {"tf": tf}
exec(ast.unparse(fn), ns)
preprocess_image = ns["preprocess_image"]
md = open("/md/cli.py").read().splitlines(keepends=True)
client_lines = textwrap.dedent("".join(md[220:223]))

for img_path in sys.argv[1:]:
    c = {"Image": Image, "np": np, "img_path": img_path}
    exec(client_lines, c)
    client = c["arr"]
    ex = tfrecords.create_tf_example(("brie cheese", img_path))
    raw = ex.features.feature["image"].bytes_list.value[0]
    records = np.frombuffer(raw, np.uint8).reshape(224, 224, 3).astype(np.float32) / 255
    serving = preprocess_image(tf.io.read_file(img_path)).numpy()
    print(img_path, "shapes", client.shape, records.shape, serving.shape)
    for a, b, an, bn in ((records, serving, "records", "serving"), (client, serving, "client", "serving"),
                         (client, records, "client", "records")):
        d = np.abs(a - b)
        print(f"  {an:>7} vs {bn:<7}: mean |diff| {d.mean():.4f}, max |diff| {d.max():.4f} "
              f"(1/255 = {1 / 255:.4f}), share of values off by more than 1/255: {(d > 1 / 255 + 1e-6).mean():.1%}")
