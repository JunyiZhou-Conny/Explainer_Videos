# C: debugging checks.
# C1: /bin/sh in this Debian image is dash (as on Debian, Ubuntu and WSL). Nothing reaches docker: the script stops at source.
for d in dataset-creator gemini-finetuner; do
  cd /repo/$d
  step 'readlink -f /bin/sh; sh docker-shell.sh; echo "status: $?"'
  step 'bash docker-shell.sh 2>&1 | head -3; grep -n "^source\|^\. " docker-shell.sh'
done
# C6: an empty batch file, and what writes one: open(file, "w") runs before write(None) fails.
cd /repo/dataset-creator
mkdir -p data && cp /repo/scripted/cheese_qa_*.txt data/
step 'python -c "
from google.genai import types
r = types.GenerateContentResponse(candidates=[types.Candidate(content=types.Content(role=\"model\", parts=[]), finish_reason=\"MAX_TOKENS\")])
print(\"response.text:\", r.text, \"| no candidates:\", types.GenerateContentResponse(candidates=[]).text)
try:
    with open(\"data/cheese_qa_4.txt\", \"w\") as file:
        file.write(r.text)
except Exception as e:
    print(f\"Error occurred while generating content: {e}\")
"'
step 'wc -c data/cheese_qa_4.txt; python cli.py --prepare | sed -n 8,10p'
# B8: the tuning job states google-genai 1.39.1 knows, and which ones the loop at gemini-finetuner/cli.py:78-84 stops on.
step 'python -c "
from google.genai import types
print([s.value for s in types.JobState])
done = {\"JOB_STATE_SUCCEEDED\", \"JOB_STATE_FAILED\", \"JOB_STATE_CANCELLED\"}
print(\"never leaves the loop:\", [s.value for s in types.JobState if s not in done and s.value not in (\"JOB_STATE_UNSPECIFIED\",)])
print(\"RUNNING in done?\", types.JobState.JOB_STATE_RUNNING in done, \"| SUCCEEDED in done?\", types.JobState.JOB_STATE_SUCCEEDED in done)
print(\"has_ended:\", hasattr(types.TuningJob, \"has_ended\"))
for s in (\"JOB_STATE_PAUSED\", \"JOB_STATE_EXPIRED\", \"JOB_STATE_SUCCEEDED\"):
    print(s, types.TuningJob(state=s).has_ended)
"'
