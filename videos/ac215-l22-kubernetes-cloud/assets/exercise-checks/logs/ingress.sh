#!/bin/bash
# B8 / Q4 / C8 on the stand-in (kind, NOT GKE): the F5 NGINX Ingress Controller from the same Helm chart
# and version as setup_loadbalancer.py:11-46 (nginx-ingress 2.3.1 from https://helm.nginx.com/stable,
# installed with Helm v3.22.1, the toolbox's version), the repo's Ingress rule, and two whoami stand-ins.
# Requests are sent with curl from the control-plane node to the controller's NodePort, with the Host
# header the browser would send. Run after kind-setup.sh up and k8s.sh b5 (namespace cheese-app-namespace).
. "$(dirname "$0")/lib.sh"
LOGS=$(cd "$(dirname "$0")" && pwd)
HELM=${HELM:?set HELM to a helm v3.22.1 linux-amd64 binary}
docker cp "$HELM" "$NODE:/usr/local/bin/helm" >/dev/null
docker cp "$LOGS/manifests/." "$NODE:/work/" >/dev/null
echo '## B8 setup: the controller (Helm), two stand-ins, the Ingress'
kstep "kubectl get namespace cheese-app-namespace >/dev/null 2>&1 || kubectl create namespace cheese-app-namespace; helm version --short; helm install nginx-f5 nginx-ingress --repo https://helm.nginx.com/stable --version 2.3.1 -n cheese-app-namespace -f nginx-f5-values.yaml --wait --timeout 5m | head -8"
kstep "kubectl apply -f ingress-backends.yaml && kubectl -n cheese-app-namespace rollout status deployment/api --timeout=180s && kubectl -n cheese-app-namespace rollout status deployment/frontend --timeout=180s"
kstep "kubectl get service -n cheese-app-namespace"
kstep "IP=\$(kubectl get pod -n cheese-app-namespace -l app.kubernetes.io/name=nginx-ingress -o jsonpath='{.items[0].status.hostIP}'); sed \"s/HOST_PLACEHOLDER/\$IP.sslip.io/\" cheese-app-ingress.yaml | kubectl apply -f - && sleep 5 && kubectl get ingress -n cheese-app-namespace"
echo '## B8 / Q4: one request per line; [Host header] path -> who answered, what it received'
for spec in "sslip /" "sslip /api-service/status" "sslip /api-service" "sslip /api-service/" "sslip /api-servicex/status" "sslip /status" "bare /" "bare /api-service/status"; do
  set -- $spec
  kstep "IP=\$(kubectl get pod -n cheese-app-namespace -l app.kubernetes.io/name=nginx-ingress -o jsonpath='{.items[0].status.hostIP}'); NP=\$(kubectl get service -n cheese-app-namespace nginx-f5-nginx-ingress-controller -o jsonpath='{.spec.ports[?(@.name==\"http\")].nodePort}'); H=\$IP$([ $1 = sslip ] && echo .sslip.io); echo \"Host: \$H  GET $2\"; curl -s -H \"Host: \$H\" -w '-> HTTP %{http_code}\n' http://\$IP:\$NP$2 | grep -E '^Hostname|^GET|^Host:|<title>|^-> HTTP'"
done
echo '## cleanup'
kstep "kubectl delete -f ingress-backends.yaml; kubectl delete ingress -n cheese-app-namespace cheese-app-ingress; helm uninstall nginx-f5 -n cheese-app-namespace"
