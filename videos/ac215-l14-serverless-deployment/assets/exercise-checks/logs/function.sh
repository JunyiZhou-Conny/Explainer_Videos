# Function checks (B6, C1, C2), run inside python:3.12-slim-bookworm with tutorial/function at 46cc62f mounted
# read-only at /fn. Network only for pip (through the session proxy); nothing calls the translation provider:
# B6 replaces googletrans with a stand-in module that echoes what the handler passes it.
. /checks/lib.sh
cd /tmp
step 'python --version; python -m venv /venv && /venv/bin/pip install -q -r /fn/requirements.txt && /venv/bin/pip list 2>/dev/null | grep -iE "^(functions-framework|googletrans|flask|gunicorn|httpx) "'
# C1: the wrong entry point, as Cloud Run's start-up would hit it
step 'cd /fn && timeout 20 /venv/bin/functions-framework --target translate 2>&1 | tail -1'
# C2: googletrans 4.0.0rc1 (the pin) vs 4.0.2 (newer): the signature, and what .text does on the newer one
step '/venv/bin/python -c "import inspect, googletrans; from googletrans import Translator; print(googletrans.__version__, Translator.translate.__qualname__ + str(inspect.signature(Translator.translate)), \"coroutine function:\", inspect.iscoroutinefunction(Translator.translate))"'
step 'python -m venv /venv2 && /venv2/bin/pip install -q functions-framework==3.10.2 googletrans==4.0.2 && /venv2/bin/python -c "
import inspect, googletrans
from googletrans import Translator
print(googletrans.__version__, Translator.translate.__qualname__ + str(inspect.signature(Translator.translate)), \"coroutine function:\", inspect.iscoroutinefunction(Translator.translate))
result = Translator().translate(\"Good afternoon everyone\", src=\"en\", dest=\"fr\")
print(type(result).__name__)
try:
    print(result.text)
except AttributeError as e:
    print(\"AttributeError:\", e)
finally:
    result.close()
"'
# B6: what the query string becomes inside hello_http (googletrans replaced by an echo stand-in)
cat > /tmp/echo_check.py <<'PY'
import sys, types
fake = types.ModuleType("googletrans")
class Translator:
    def translate(self, text, src="auto", dest="en"):
        return types.SimpleNamespace(text=f"text={text!r} src={src!r} dest={dest!r}")
fake.Translator = Translator
sys.modules["googletrans"] = fake
import functions_framework
app = functions_framework.create_app(target="hello_http", source="/fn/main.py")
client = app.test_client()
for q in sys.argv[1:]:
    r = client.get("/" + q)
    print(f"GET /{q} -> {r.status_code} {r.get_data(as_text=True)}")
PY
step '/venv/bin/python /tmp/echo_check.py "" "?text=Good%20afternoon%20everyone&src=en&dest=fr" "?text=Good afternoon everyone&dest=fr" "?text=Good+afternoon&dest=el" "?text=Tom%20%26%20Jerry&dest=fr" "?text=Tom & Jerry&dest=fr" "?dest=zh-cn&text=Hi&src=en" "?Dest=fr&text=Hi"'
