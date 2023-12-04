kubectl apply -f namespace.yml
kubectl apply -f protobuf-client.yml -n cluster1-ol-team2
kubectl apply -f protobuf-health-svr-deploy.yml -n cluster1-ol-team2
kubectl apply -f protobuf-health-svr-svc.yml -n cluster1-ol-team2
kubectl apply -f protobuf-order-svr-deploy.yml -n cluster1-ol-team2
kubectl apply -f protobuf-order-svr-svc.yml -n cluster1-ol-team2