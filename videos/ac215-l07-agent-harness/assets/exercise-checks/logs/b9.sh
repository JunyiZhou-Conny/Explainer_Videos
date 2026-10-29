# B9: a link in the skill's email template (a copy: this container's /app), then the scripted Act 5 path.
step "sed -i 's|<body>|<body><p><a href=\"https://example.com\">link</a></p>|' skills/vendor-outreach/assets/email-template.html && grep -n 'href' skills/vendor-outreach/assets/email-template.html"
step "python cli.py --act 5 --fixture --email-decision approve > /tmp/b9.txt 2>&1; echo \"cli.py exit status: \$?\"; grep -E 'Skill loaded|Skills available|Run stopped|Inspect|HARNESS|HTML file|^Traceback|Error' /tmp/b9.txt | cut -c1-160"
step "find outputs -name '*.html' | wc -l"
