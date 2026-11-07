#!/bin/bash
# Exercise checks on the stand-in cluster (kind, NOT GKE; see kind-setup.sh). Run from the session
# machine after `kind-setup.sh up`:  bash k8s.sh <section>... > k8s.log   (sections below, in order)
# kubectl runs inside the control-plane node container (lib.sh kstep); manifests/ is copied to /work.
. "$(dirname "$0")/lib.sh"
LOGS=$(cd "$(dirname "$0")" && pwd)
SRC=$(cd "$LOGS/../../source" && pwd)
NODE_IMG_KIND=${KIND:-kind}
for SEC in "$@"; do
case $SEC in
setup)
  echo '## setup: the manifests and the tutorial file in the node, the game deployed'
  docker exec "$NODE" mkdir -p /work
  docker cp "$LOGS/manifests/." "$NODE:/work/" >/dev/null
  docker cp "$SRC/src/deployment/deploy-k8s-tic-tac-toe.yml" "$NODE:/work/" >/dev/null
  kstep "kubectl version; kubectl get nodes -o wide"
  kstep "kubectl apply -f deploy-k8s-tic-tac-toe.yml; kubectl rollout status deployment/web --timeout=180s"
  kstep "kubectl get deployment,replicaset,pods,service,endpointslices -o wide"
  ;;
q1)
  echo '## Q1: who decides where, who notices a Pod is gone (events of one delete)'
  kstep "P=\$(kubectl get pods -l run=web -o jsonpath='{.items[0].metadata.name}'); kubectl delete pod \$P; sleep 8; kubectl get events --sort-by=.lastTimestamp -o custom-columns=REASON:.reason,SOURCE:.source.component,OBJECT:.involvedObject.name,MESSAGE:.message | tail -8"
  ;;
b1)
  echo '## B1: take one Pod out of the label'
  kstep "kubectl get pods -L run -o wide; kubectl get endpointslices -l kubernetes.io/service-name=web"
  kstep "P=\$(kubectl get pods -l run=web -o jsonpath='{.items[0].metadata.name}'); echo \$P > /work/b1-pod; kubectl label pod \$P run=debug --overwrite"
  sleep 6
  kstep "kubectl get pods -L run -o wide; kubectl get endpointslices -l kubernetes.io/service-name=web; kubectl get rs"
  kstep "kubectl get pod \$(cat /work/b1-pod) -o jsonpath='ownerReferences: {.metadata.ownerReferences}{\"\n\"}'"
  kstep "kubectl delete pod \$(cat /work/b1-pod); kubectl get pods -L run"
  ;;
b2)
  echo '## B2: change the Pod template: a new ReplicaSet'
  kstep "kubectl get rs -l run=web"
  kstep "kubectl set env deployment/web COLOR=blue; kubectl rollout status deployment/web --timeout=180s; kubectl get rs -l run=web; kubectl get pods -l run=web"
  kstep "kubectl rollout undo deployment/web; kubectl rollout status deployment/web --timeout=180s; kubectl get rs -l run=web"
  ;;
b3)
  echo '## B3: a crash is not a delete'
  kstep "kubectl apply -f crasher.yaml; sleep 5; kubectl get pods -l run=crasher; sleep 10; kubectl get pods -l run=crasher; sleep 30; kubectl get pods -l run=crasher"
  kstep "P=\$(kubectl get pods -l run=crasher -o jsonpath='{.items[0].metadata.name}'); kubectl logs \$P; kubectl describe pod \$P | grep -E 'Last State:|Exit Code:|Restart Count:|Back-off'"
  kstep "P=\$(kubectl get pods -l run=crasher -o jsonpath='{.items[0].metadata.name}'); kubectl delete pod \$P; sleep 3; kubectl get pods -l run=crasher"
  kstep "kubectl delete -f crasher.yaml"
  ;;
b4)
  echo '## B4: the NodePort answers on every node, also the one without a web Pod'
  kstep "kubectl get service web; kubectl get pods -l run=web -o wide"
  kstep "NP=\$(kubectl get service web -o jsonpath='{.spec.ports[0].nodePort}'); for n in \$(kubectl get nodes -o jsonpath='{range .items[*]}{.metadata.name}={.status.addresses[0].address} {end}'); do printf '%s -> ' \$n; curl -s -o /dev/null -w '%{http_code}\n' http://\${n#*=}:\$NP/; done"
  ;;
b5)
  echo '## B5: Service names and namespaces'
  kstep "kubectl create namespace cheese-app-namespace; kubectl create service clusterip vector-db --tcp=8000:8000 -n cheese-app-namespace; kubectl get service -n cheese-app-namespace"
  kstep "kubectl run dns-default --image=busybox:1.36 --restart=Never -- sh -c 'for h in vector-db vector-db.cheese-app-namespace vector-db.cheese-app-namespace.svc.cluster.local; do echo \"== \$h\"; nslookup \$h 2>&1 | grep -E \"^Name|^Address: 10|NXDOMAIN|can.t find\" | sort -u; done; cat /etc/resolv.conf | grep search'; kubectl wait --for=jsonpath='{.status.phase}'=Succeeded pod/dns-default --timeout=120s >/dev/null; kubectl logs dns-default; kubectl delete pod dns-default"
  kstep "kubectl run dns-app -n cheese-app-namespace --image=busybox:1.36 --restart=Never -- sh -c 'echo \"== vector-db\"; nslookup vector-db 2>&1 | grep -E \"^Name|^Address: 10\"; cat /etc/resolv.conf | grep search'; kubectl wait -n cheese-app-namespace --for=jsonpath='{.status.phase}'=Succeeded pod/dns-app --timeout=120s >/dev/null; kubectl logs -n cheese-app-namespace dns-app; kubectl delete pod -n cheese-app-namespace dns-app"
  ;;
b6)
  echo '## B6 / C6: requests, packing and Pending'
  kstep "kubectl describe node l22ex-worker | grep -A8 -E '^Allocatable:'; kubectl describe node l22ex-worker | grep -A6 -E '^Allocated resources:'"
  kstep "kubectl apply -f fat.yaml; kubectl rollout status deployment/fat --timeout=120s; kubectl get pods -l run=fat -o wide"
  kstep "kubectl scale deployment fat --replicas=3; sleep 15; kubectl get pods -l run=fat -o wide"
  kstep "P=\$(kubectl get pods -l run=fat --field-selector=status.phase=Pending -o jsonpath='{.items[0].metadata.name}'); kubectl describe pod \$P | sed -n '/^Events:/,\$p'"
  kstep "kubectl scale deployment fat --replicas=1; sleep 5; kubectl get pods -l run=fat; kubectl delete -f fat.yaml"
  ;;
b7)
  echo '## B7: a Pod autoscaler needs requests (metrics-server, v0.8.0, kubelet TLS check off for kind)'
  kstep "kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/download/v0.8.0/components.yaml >/dev/null && kubectl -n kube-system patch deployment metrics-server --type=json -p '[{\"op\":\"add\",\"path\":\"/spec/template/spec/containers/0/args/-\",\"value\":\"--kubelet-insecure-tls\"}]' && kubectl -n kube-system rollout status deployment/metrics-server --timeout=240s"
  sleep 60
  kstep "kubectl top pods -l run=web; kubectl get deployment web -o jsonpath='requests: {.spec.template.spec.containers[0].resources}{\"\n\"}'"
  kstep "kubectl autoscale deployment web --cpu-percent=50 --min=2 --max=4; sleep 75; kubectl get hpa web; kubectl describe hpa web | sed -n '/^Conditions:/,\$p'"
  kstep "kubectl set resources deployment web --requests=cpu=50m; kubectl rollout status deployment/web --timeout=180s; sleep 90; kubectl get hpa web"
  kstep "kubectl delete hpa web; kubectl set resources deployment web --requests=cpu=0 >/dev/null; kubectl patch deployment web --type=json -p '[{\"op\":\"remove\",\"path\":\"/spec/template/spec/containers/0/resources/requests\"}]'; kubectl rollout status deployment/web --timeout=180s; kubectl delete -f https://github.com/kubernetes-sigs/metrics-server/releases/download/v0.8.0/components.yaml >/dev/null && echo metrics-server removed"
  ;;
c1)
  echo '## C1: the README debugging line, the namespace fixed, then the container fixed'
  kstep "kubectl apply -f loader-job.yaml; kubectl wait -n cheese-app-namespace --for=condition=complete job/vector-db-loader --timeout=120s"
  kstep "kubectl logs -n cheese-app-cluster-namespace job/vector-db-loader -c wait-for-chromadb"
  kstep "kubectl logs -n cheese-app-namespace job/vector-db-loader -c wait-for-chromadb"
  kstep "kubectl logs -n cheese-app-namespace job/vector-db-loader"
  kstep "kubectl get pods -n cheese-app-namespace | grep vector-db-loader"
  ;;
c4)
  echo '## C4: command vs args (the loader as written on main and on cluster-updates)'
  step "docker build -q -t l22ex/entrypoint:1 -f $LOGS/manifests/entry.Dockerfile $LOGS/manifests >/dev/null && echo built l22ex/entrypoint:1 && $NODE_IMG_KIND load docker-image l22ex/entrypoint:1 --name l22ex 2>&1 | tail -1"
  kstep "kubectl apply -f loader-args.yaml -f loader-command.yaml; sleep 20; kubectl get jobs,pods -l 'batch.kubernetes.io/job-name in (loader-args,loader-command)'"
  kstep "kubectl logs job/loader-args"
  kstep "P=\$(kubectl get pods -l batch.kubernetes.io/job-name=loader-command -o jsonpath='{.items[0].metadata.name}'); kubectl describe pod \$P | grep -E 'Reason:|Message:|Exit Code:' ; kubectl describe pod \$P | sed -n '/^Events:/,\$p' | grep -E 'Failed|Warning' | head -3"
  kstep "kubectl delete -f loader-args.yaml -f loader-command.yaml"
  ;;
c5)
  echo '## C5: backoffLimit 3: how many attempts?'
  kstep "kubectl apply -f failing-job.yaml; kubectl wait --for=condition=failed job/always-fails --timeout=300s; kubectl get pods -l batch.kubernetes.io/job-name=always-fails; kubectl describe job always-fails | grep -E 'Pods Statuses|BackoffLimitExceeded'"
  kstep "kubectl delete -f failing-job.yaml"
  ;;
c7)
  echo '## C7: an image tag that was never pushed'
  kstep "kubectl apply -f placeholder-image.yaml; sleep 40; kubectl get pods -l run=frontend-placeholder"
  kstep "P=\$(kubectl get pods -l run=frontend-placeholder -o jsonpath='{.items[0].metadata.name}'); kubectl describe pod \$P | sed -n '/^Events:/,\$p' | grep -E 'Failed|BackOff' | head -4"
  kstep "kubectl delete -f placeholder-image.yaml"
  ;;
esac
done
