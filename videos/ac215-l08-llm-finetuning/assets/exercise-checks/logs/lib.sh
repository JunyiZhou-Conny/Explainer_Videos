# Sourced inside the check container. step "<command>" runs it in the current folder and prints it the way
# assets/terminal/run_steps.sh does: "$ command", its output (stderr joined), "[exit N]".
step() {
  printf '$ %s\n' "$1"
  sh -c "$1" 2>&1
  printf '[exit %s]\n\n' "$?"
}
