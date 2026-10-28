# b11_adk_git.sh: where do adk web's sessions go, and would git pick them up? Run from the repo root.
source /checks/web.sh
start_web /tmp/web.log
echo '$ curl -s -X POST http://localhost:8000/apps/baseline/users/student/sessions; echo'
curl -s -X POST http://localhost:8000/apps/baseline/users/student/sessions; echo
stop_web
grep -E 'local session service|New session' /tmp/web.log | cut -c1-200
echo '$ ls -a baseline/.adk'; ls -a baseline/.adk
echo '$ git status --short --untracked-files=all | grep -v "^ D"'; git status --short --untracked-files=all | grep -v '^ D'
echo '$ git add --all --dry-run | grep -v "^remove"'; git add --all --dry-run | grep -v '^remove'
echo '$ echo ".adk/" >> .gitignore; git check-ignore -v baseline/.adk/session.db'
echo ".adk/" >> .gitignore; git check-ignore -v baseline/.adk/session.db
echo '$ git add --all --dry-run | grep -v "^remove"'; git add --all --dry-run | grep -v '^remove'
echo '$ git checkout .gitignore   # (undo, for the next checks)'; git checkout .gitignore
