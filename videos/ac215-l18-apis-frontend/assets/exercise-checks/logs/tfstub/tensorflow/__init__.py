# Check-only stand-in for TensorFlow (NOT the real library): lets api/utils/llm_cnn_utils.py's
# load_cnn_model() run to its last line without the 2 GB wheel. load_model returns a placeholder,
# so /readyz can move on to its Chroma check. Nothing here predicts anything.
class keras:
    class models:
        @staticmethod
        def load_model(path):
            print(f"[tf stand-in] load_model({path!r})", flush=True)
            return object()
