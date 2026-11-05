"""Capture-only helper for the L15 recording, NOT part of the tutorial.

Runs model-deployment-aws/cli.py's own predict() against a LOCAL stand-in for the SageMaker
endpoint: the tensorflow/serving container (SageMaker's TensorFlow serving image runs TensorFlow
Serving too) serving the SavedModel that prepare() exported. Only sagemaker.Predictor and
sagemaker.Session are replaced; the images, the payload {"instances": [...]}, the argmax and the
label lookup are cli.py's own code.
Usage: python predict_local.py http://localhost:8501/v1/models/cheese:predict
"""
import sys

sys.path.insert(0, "/app")
import numpy as np  # noqa: E402
import requests  # noqa: E402
import sagemaker  # noqa: E402

URL = sys.argv[1]


class LocalServingPredictor:
    def __init__(self, endpoint_name, **kwargs):
        print(f"[capture stand-in] endpoint '{endpoint_name}' -> local TensorFlow Serving at {URL}")

    def predict(self, payload):
        r = requests.post(URL, json=payload, timeout=120)
        r.raise_for_status()
        return r.json()


sagemaker.Predictor = LocalServingPredictor
sagemaker.Session = lambda *a, **k: None
np.random.seed(15)  # cli.py samples 5 images at random; seeded so a re-capture picks the same ones
import cli  # noqa: E402

print("Predict using endpoint")  # the line cli.main() prints first (cli.py:326)
cli.predict()
