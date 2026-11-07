# Stand-in for deploy_single_vm: a StackReference to the images stack (setup_containers.py:27), one
# container through the Docker provider (as setup_containers.py / setup_webserver.py do, here on the
# local daemon instead of ssh://), and one remote.Command over SSH (as provision_instance.py does, here
# against a disposable sshd container on 127.0.0.1:12222). No cloud resource anywhere.
import pulumi
import pulumi_docker as docker
from pulumi_command import remote

images_stack = pulumi.StackReference("organization/l20ex-images/dev")
frontend_tag = images_stack.get_output("cheese-app-frontend-react-tags")

web = docker.Container(
    "deploy-frontend-container",
    name="l20ex-web",
    image="nginx:stable",          # stands in for the registry image; the tag travels as a label
    labels=[docker.ContainerLabelArgs(label="image-tag", value=frontend_tag.apply(lambda t: t[0]))],
    ports=[docker.ContainerPortArgs(internal=80, external=18081)],
)

def conn(key_file):
    return remote.ConnectionArgs(host="127.0.0.1", port=12222, user="student",
                                 private_key=open(key_file).read())

marker = remote.Command(
    "format-persistent-disk",
    connection=conn("/work/keys/ssh-key-deployment"),
    create="touch /home/student/created-by-pulumi && echo created marker",
)

if pulumi.Config().get_bool("try_passphrase_key"):
    remote.Command("with-passphrase-key", connection=conn("/work/keys/ssh-key-with-passphrase"), create="echo hello")

pulumi.export("container_name", web.name)
