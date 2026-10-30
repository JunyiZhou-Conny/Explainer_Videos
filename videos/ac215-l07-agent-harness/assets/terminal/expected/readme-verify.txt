# expected (README text, not program output): dlops-io/agent-harness, main @ e25dfe9615d78b78e0764a636cc2462f530a1402, README.md:118-133 (Verify the environment: the test suite should finish with OK), unchanged.
### Verify the environment

These commands are **offline**:

```bash
python -m scripts.check_sdk
python -m tests
```

The SDK check prints installed versions and available capabilities. The test suite should finish with `OK`. It exercises local scripted model responses, validation, approvals, isolation, and failure handling; it does not establish live model quality.

Passing-test output is buffered by default. To inspect all diagnostic output, including deliberate failure tests:

```bash
python -m tests --show-logs
```
