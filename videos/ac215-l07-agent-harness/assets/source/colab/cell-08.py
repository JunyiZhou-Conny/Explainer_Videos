# @title Install Dependencies
import tomllib

if sys.version_info < (3, 13):
    raise RuntimeError("Select a Python 3.13+ notebook kernel before continuing.")
project = tomllib.loads(Path("pyproject.toml").read_text())
subprocess.run([sys.executable, "-m", "pip", "install", *project["project"]["dependencies"]], check=True)
subprocess.run([sys.executable, "-m", "scripts.check_sdk"], check=True)
