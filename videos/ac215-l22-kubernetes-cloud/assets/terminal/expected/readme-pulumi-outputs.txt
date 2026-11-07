# expected (recorded in the tutorial): README.md:497-506 at dlops-io/cheese-app-v3@3ecef56, the 'Outputs:' block the README shows after `pulumi up --stack dev --refresh -y` (README.md:454). Unchanged except the README's three sample IP addresses, replaced by <IP> / <control-plane IP> (series rule). Older than the code: __main__.py:43-49 exports ip_address (not nginx_ingress_ip) and setup_loadbalancer.py:65 names the Ingress cheese-app-ingress (not nginx-ingress); see ASSETS.md.
Outputs:
    app_url         : "http://<IP>.sslip.io"
    cluster_endpoint: "<control-plane IP>"
    cluster_name    : "cheese-app-cluster"
    ingress_name    : "nginx-ingress"
    kubeconfig      : [secret]
    namespace       : "cheese-app-namespace"
    nginx_ingress_ip: "<IP>"
