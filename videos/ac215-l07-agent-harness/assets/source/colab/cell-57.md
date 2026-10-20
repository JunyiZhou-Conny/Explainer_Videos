**2. Run the selected cases**

Each execution gets a new experiment label, so rerunning the cell preserves the previous
batch. The runner uses the real act implementations and the same checks as the CLI.

It records successful runs, failed checks, execution errors, and any missing scheduled
runs. After three consecutive execution errors it stops the batch; missing runs still
count in the pass-rate denominator. Manager-review cases also report whether review
was actually reached—a cheap cart can bypass that branch without testing it.
