# Sourced by every check script. step "<command>" runs it with sh and prints it the way
# assets/terminal/run_steps.sh does: "$ command", its output (stderr joined), "[exit N]".
step() {
  printf '$ %s\n' "$1"
  sh -c "$1" 2>&1
  printf '[exit %s]\n\n' "$?"
}
IMAGE=cgumb/ac215-translation-demo:lecture14-agent-platform-20261022
DIGEST_REF=cgumb/ac215-translation-demo@sha256:c17b6db09f7402febb582bf327920ec9ca4eee113f5ddefa38e9da5619dbe72e
