# B5 and C8 in the l08ex-peft venv (see setup-peft.sh).
step 'python /checks/snippets/peft_meta.py 2>&1 | grep -v "^ *warnings.warn"'
step 'python -c "import inspect, peft.utils.other as o; src = inspect.getsource(o.prepare_model_for_kbit_training); print(chr(10).join(l for l in src.splitlines() if \"float32\" in l or \"param.requires_grad = False\" in l))"'
