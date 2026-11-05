"""Check-only helper (NOT part of the tutorial). B5: labels come from folder names.
(a) The processor's own data_details (src/data-processor/tfrecords.py:10-23, read with ast, nothing
else of the module runs) and the lookup create_tf_example does (tfrecords.py:36) for each query.
(b) What task.py:68's num_classes = 3 does to the four labels: its own tf.one_hot call
(task.py:137) and Keras's categorical_crossentropy (task.py:255) on one made-up prediction."""
import ast

src = open("/src/data-processor/tfrecords.py").read()
node = next(n for n in ast.parse(src).body if isinstance(n, ast.Assign) and n.targets[0].id == "data_details")
data_details = ast.literal_eval(node.value)
for query in ["brie cheese", "gouda cheese", "gruyere cheese", "parmigiano cheese", "cheddar cheese", "Brie cheese"]:
    try:
        print(f"label folder {query!r:22} -> label {data_details['label_folders'][query]}")
    except KeyError as e:
        print(f"label folder {query!r:22} -> KeyError: {e}")

import os  # noqa: E402
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import tensorflow as tf  # noqa: E402
from tensorflow import keras  # noqa: E402

print("tensorflow", tf.__version__, "keras", keras.__version__)
for num_classes in (3, 4):
    onehot = tf.one_hot(tf.constant([0, 1, 2, 3]), num_classes).numpy().astype(int).tolist()
    print(f"num_classes = {num_classes}: tf.one_hot(labels 0,1,2,3) = {onehot}")
    pred = tf.constant([[0.2, 0.3, 0.5] if num_classes == 3 else [0.1, 0.2, 0.3, 0.4]])
    loss = keras.losses.categorical_crossentropy(tf.constant([onehot[3]], tf.float32), pred).numpy()[0] + 0.0
    print(f"  cross-entropy of a gouda photo (label 3) for prediction {pred.numpy()[0].tolist()}: {loss:.4f}")
