# Stand-in for deploy_images/__main__.py: the same timestamp tag (line 13) and the same export name
# (lines 54-55 of the real file), but the "build" is a local echo: nothing is built or pushed.
import datetime
import pulumi
from pulumi_command import local

timestamp_tag = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
tag_value = pulumi.Config().get("fixed_tag") or timestamp_tag  # exercise D2: a tag that only changes with the code
registry_url = "us-docker.pkg.dev/your-gcp-project/cheese-app-repository"
tag = f"{registry_url}/cheese-app-frontend-react:{tag_value}"

build = local.Command("build-cheese-app-frontend-react", create=f"echo would build and push {tag}", triggers=[tag])
pulumi.export("cheese-app-frontend-react-tags", [tag])
