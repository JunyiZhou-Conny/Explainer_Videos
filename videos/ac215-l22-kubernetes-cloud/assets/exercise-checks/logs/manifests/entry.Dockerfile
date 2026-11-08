# C4: an image shaped like src/vector-db/Dockerfile:51 (ENTRYPOINT runs a script that receives the args)
FROM busybox:1.36
COPY entry.sh /entry.sh
ENTRYPOINT ["/bin/sh", "/entry.sh"]
