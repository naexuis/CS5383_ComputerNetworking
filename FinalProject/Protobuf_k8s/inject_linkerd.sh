kubectl get -n cluster1-ol-team2 deploy -o yaml | linkerd inject - | kubectl apply -f -
