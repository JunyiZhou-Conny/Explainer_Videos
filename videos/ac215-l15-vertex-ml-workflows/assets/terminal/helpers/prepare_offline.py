"""Capture-only helper for the L15 recording, NOT part of the tutorial.

Runs model-deployment-aws/cli.py's own prepare() with the S3 client replaced by a stub, because the
recording sandbox has no AWS account. Everything prepare() does on the laptop is real (download the
release zip, load the .keras model, export the SavedModel into version folder 1, write
model.tar.gz); the two cloud calls are visibly NOT sent: create_bucket prints a stub line, and
upload_file raises, so cli.py never reaches its "Model uploaded successfully" line.
Usage (inside the tutorial's own image, /app = the clone): python prepare_offline.py
"""
import sys

sys.path.insert(0, "/app")
import boto3  # noqa: E402


class NoAccountS3:
    class exceptions:  # the two names cli.py catches around create_bucket
        class BucketAlreadyExists(Exception):
            pass

        class BucketAlreadyOwnedByYou(Exception):
            pass

    def create_bucket(self, **kwargs):
        print(f"[capture stub] create_bucket({kwargs}) NOT sent: no AWS account in this recording")

    def upload_file(self, *args):
        raise RuntimeError(f"[capture stub] upload_file{args} NOT sent: no AWS account in this recording")


boto3.client = lambda *a, **k: NoAccountS3()
import cli  # noqa: E402

print("Prepare model and save model to GCS Bucket")  # the line cli.main() prints first (cli.py:318)
cli.prepare()
