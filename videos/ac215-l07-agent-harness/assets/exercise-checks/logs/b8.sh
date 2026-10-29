# B8: force the detector to miss the malicious note; the scripted planner then drafts to other@example.com.
step "python cli.py --act 4 --fixture --vendor-document malicious --simulate-detector-miss --email-decision approve"
step "python cli.py --act 4 --vendor-document malicious --simulate-detector-miss"
