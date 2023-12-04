# ol_team2 

# Load Balancer Experiment Documentation

## Introduction
This document outlines the steps and observations from our final project to test the performance and functionality of a load balancer in a kubernetes setup using our previous health server code from Program Assignment 1.

## Experiment 1

### Objective
The primary objective of this experiment is to evaluate the load balancer's ability to distribute incoming traffic evenly across multiple servers while maintaining high availability and scalability.

## Cases

1. Case one will be a simple one client to one server so no load balancer will be used. This will be the base case that we will try to become faster than.
2. Case two will have 5 servers and we will use the default kubernetes load balancer.
3. Case three will have 5 servers but will use the linkerd load balancer to hopefully reduce latency to as low as possible.


## How to run the code

1. Run the start script which should be located in the home directory

```
./start_k8s.sh
```

2. Go into `ol_team2\FinalProject\Protobuf_k8s\protobuf-health-svr-deploy.yml` and change the number of `replicas` to how many servers you want to run based on the case you want to run. 

3. Start all the pods and services from programming assignment 1. You can run the following commands:
```
kubectl apply -f namespace.yml
kubectl apply -f protobuf-client.yml -n cluster1-ol-team2
kubectl apply -f protobuf-health-svr-deploy.yml -n cluster1-ol-team2
kubectl apply -f protobuf-health-svr-svc.yml -n cluster1-ol-team2
kubectl apply -f protobuf-order-svr-deploy.yml -n cluster1-ol-team2
kubectl apply -f protobuf-order-svr-svc.yml -n cluster1-ol-team2
```

4. Verify that the client, health, and order servers were created. Note the name of the client server.

```
kubectl get pods -A
```

5. Grab the ip address of the health server and order server using the following:

```
kubectl get services -A
```

6. If you are using the linkerd load balancer you will need to run the following.
```
curl --proto '=https' --tlsv1.2 -sSfL https://run.linkerd.io/install | sh
export PATH=$HOME/.linkerd2/bin:$PATH
linkerd install --crds | kubectl apply -f -
linkerd install | kubectl apply -f -
linkerd viz install | kubectl apply -f -

# then to inject the load balancer sidecar into the deployments run 
kubectl get -n cluster1-ol-team2 deploy -o yaml | linkerd inject - | kubectl apply -f -
```

7. Then log into the client server

```
kubectl exec -it -n cluster1-ol-team2 protobuf-client-txh59 /bin/bash
```

8. Then start the client
```
python3 protobufdemo_grpc_client.py --addrHealth 10.103.160.215 --addrOrder 10.101.149.163 --iters 1000 --portHealth 5577 --portOrder 5578 --fileName NOLoadBalancer
```

9. Then once you are done, you can delete all of ther services using the following:

```
kubectl delete deployment --all -n cluster1-ol-team2
kubectl delete service --all -n cluster1-ol-team2
kubectl delete job --all -n cluster1-ol-team2
kubectl delete pods --all -n cluster1-ol-team2
```

## Experiment 2
## Cases

1. Case one will have 5 clients spamming 1 server with messages, no load balancer will be used. This will be the base case that we will try to become faster than.
2. Case two will the same 5 spamming clients, 5 servers, and we will use the default kubernetes load balancer.
3. Case three will have 5 spamming clients and 5 servers, but will use the linkerd load balancer to hopefully reduce latency to as low as possible.


## How to run the code

1. Run the start script which should be located in the home directory

```
./start_k8s.sh
```

2. Go into `ol_team2\FinalProject\Protobuf_k8s\protobuf-health-svr-deploy.yml` and change the number of `replicas` to how many servers you want to run based on the case you want to run. 

3. Start all the pods and services from programming assignment 1 along with starting the spammer job. You can run the following commands:
```
kubectl apply -f namespace.yml
kubectl apply -f protobuf-client.yml -n cluster1-ol-team2
kubectl apply -f protobuf-health-svr-deploy.yml -n cluster1-ol-team2
kubectl apply -f protobuf-health-svr-svc.yml -n cluster1-ol-team2
kubectl apply -f protobuf-order-svr-deploy.yml -n cluster1-ol-team2
kubectl apply -f protobuf-order-svr-svc.yml -n cluster1-ol-team2
kubectl apply -f protobuf-noise.yml -n cluster1-ol-team2
```

4. Verify that the client, health, and order servers were created. Note the name of the client server.

```
kubectl get pods -A
```

5. Grab the ip address of the health server and order server using the following:

```
kubectl get services -A
```

6. If you are using the linkerd load balancer you will need to run the following.
```
curl --proto '=https' --tlsv1.2 -sSfL https://run.linkerd.io/install | sh
export PATH=$HOME/.linkerd2/bin:$PATH
linkerd install --crds | kubectl apply -f -
linkerd install | kubectl apply -f -
linkerd viz install | kubectl apply -f -

# then to inject the load balancer sidecar into the deployments run 
kubectl get -n cluster1-ol-team2 deploy -o yaml | linkerd inject - | kubectl apply -f -
```

7. Then log into the noise job

```
kubectl exec -it -n cluster1-ol-team2 protobuf-noise-txh59 /bin/bash
```

8. Start 5 instances of the noise client using the following command:

```
python3 protobufdemo_grpc_noise.py --addrHealth 10.103.160.215 --addrOrder 10.101.149.163 --iters 1000 --portHealth 5577 --portOrder 5578 --fileName NOLoadBalancer2Client.txt > /dev/null &
```

9. In another terminal log into the client server

```
kubectl exec -it -n cluster1-ol-team2 protobuf-client-txh59 /bin/bash
```

10. Then start the client
```
python3 protobufdemo_grpc_client.py --addrHealth 10.103.160.215 --addrOrder 10.101.149.163 --iters 1000 --portHealth 5577 --portOrder 5578 --fileName NOLoadBalancer
```

11. Then once you are done, you can delete all of ther services using the following:

```
kubectl delete deployment --all -n cluster1-ol-team2
kubectl delete service --all -n cluster1-ol-team2
kubectl delete job --all -n cluster1-ol-team2
kubectl delete pods --all -n cluster1-ol-team2
```

## Results and Observations

The results can be found under `ol_team2\FinalProject\Latency Data` and the outcome is surprising. We  see that if we only have one client the latency gets worse if we add a load balancer. Due to the small nature of the assignment this makes sense because the messages are being processed fast enough by the single server. We are adding a small bit of latency when we include a load balancer and it has to decide what server to send the messages to. The next step will be to see what happens when we have more clients that are spamming the server.
