# recorded (the tutorial's screenshot): the run graph in assets/pipline.png at dlops-io/cheese-app-ci-cd b8458ff (committed in 3dea317), transcribed 2026-11-06. The image itself is not copied into this repository.
# It is an all-green run of an EARLIER code state (see ASSETS.md); a push of b8458ff today has a red Lint and Format Check (runner/run1).
title: ci.yml
trigger: on: push
Build Docker Image      success  54s
Unit Tests              success  18s
Integration Tests       success  20s
System Tests            success  39s
Lint and Format Check   success  22s
Test Summary            success   4s
edges: Build Docker Image -> {Unit Tests, Integration Tests, System Tests} -> Test Summary; Build Docker Image -> Lint and Format Check (no edge to Test Summary)
