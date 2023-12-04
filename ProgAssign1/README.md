# Program Assignment 1 Status 

Team members include: Adam Gibbons, Marcus Hilliard, and David Maples.

## Milestone 1: ZeroMQ with Flatbuffers

Requirements:

1. Extend the message formats as required by the writeup
   * Completed
2. Define Flatbuffer schema and generated serialization code for the schema
   * Completed
3. ZeroMQ client and server code that can talk to each other using the serialization/deserialization code
   * Completed
4. Test code locally
   * successful tested using local host
   * median latency times are presented in the table below after 100 observations

| Server  | Process | Median Latency Time |
| ------------- | ------------- | ----- |
| Health  | Serialization  | 0.496 msec  |
| Order  | Serialization  | 1.602 msec  |
| Health  | Deserialization  | 1.004 sec  |
| Order  | Deserialization  | 1.006 sec  |

5. Test code on Mininet topologies
   * Successful test using three hosts and one switch
     * median latency times are presented in the table below after 100 observations

| Server  | Process | Median Latency Time |
| ------------- | ------------- | ----- |
| Health  | Serialization  | 0.357 msec  |
| Order  | Serialization  | 1.096 msec  |
| Health  | Deserialization  | 1.045 sec  |
| Order  | Deserialization  | 1.046 sec  |

   * Successful test using three hosts and three switches
      * median latency times are presented in the table below after 100 observations

| Server  | Process | Median Latency Time |
| ------------- | ------------- | ----- |
| Health  | Serialization  | 0.533 msec  |
| Order  | Serialization  | 1.739 msec  |
| Health  | Deserialization  | 1.087 sec  |
| Order  | Deserialization  | 1.068 sec  |

   * Successful test using 27 hosts and 13 switches
     * median latency times are presented in the table below after 100 observations

| Server  | Process | Median Latency Time |
| ------------- | ------------- | ----- |
| Health  | Serialization  | 0.574 msec  |
| Order  | Serialization  | 1.572 msec  |
| Health  | Deserialization  | 1.132 sec  |
| Order  | Deserialization  | 1.135 sec  |

## Milestone 2: gRPC with ProtoBuff

Requirements:

1. Extend the message formats as required by the writeup
   * Completed
2. Define Protobuf schema and generated serialization code for the schema
   * Completed
3. gRPC client and server code that can talk to each other using the serialization code
   * Completed
4. Test code locally
   * successful tested using local host
   * median latency times are presented in the table below after 100 observations

| Server  | Process | Median Latency Time |
| ------------- | ------------- | ----- |
| Health  | Serialization  | 0.507 msec  |
| Order  | Serialization  | 0.809 msec  |

5. Test code on Mininet topologies
   * Successful test using three hosts and one switch
     * median latency times are presented in the table below after 100 observations

| Server  | Process | Median Latency Time |
| ------------- | ------------- | ----- |
| Health  | Serialization  | 42.072 msec  |
| Order  | Serialization  | 129.791 msec  |

   * Successful test using three hosts and three switches
      * median latency times are presented in the table below after 100 observations

| Server  | Process | Median Latency Time |
| ------------- | ------------- | ----- |
| Health  | Serialization  | 83.269 msec  |
| Order  | Serialization  | 196.685 msec  |

   * Successful test using 27 hosts and 13 switches
     * median latency times are presented in the table below after 100 observations

| Server  | Process | Median Latency Time |
| ------------- | ------------- | ----- |
| Health  | Serialization  | 126.0 msec  |
| Order  | Serialization  | 396.762 msec  |

## Milestone 3: Cloud Based Deployment

### How to run the code

To run the code locally on a Kubernets single cluster:
1. Run the start script which should be located in the home directory

```
./start_k8s.sh
```

2. Then, go to the directory where you files are located

```
kubectl apply -f namespace.yml
kubectl -n cluster1-ol-team2 apply -f zeromq-health-svr-svc.yml
kubectl -n cluster1-ol-team2 apply -f zeromq-health-svr-deploy.yml
kubectl -n cluster1-ol-team2 apply -f zeromq-order-svr-svc.yml
kubectl -n cluster1-ol-team2 apply -f zeromq-order-svr-deploy.yml
kubectl -n cluster1-ol-team2 apply -f zeromq-client.yml
```

4. Verify that the client, health, and order servers were created. Note the name of the client server.

```
kubectl get pods -A
```

4. Grab the ip address of the health server and order server using the following:

```
kubectl get services -A
```

6. Then log into the client server

```
kubectl exec -it -n cluster1-ol-team2 zeromq-client-txh59 /bin/bash
```

7. Then start the client

```
python3 tcp_client.py --addrHealth 10.98.7.83 --addrOrder 10.105.14.71 --iterLoop 100 --portHealth 5555 --portOrder 5556 --fileName k8s_healthOrderTime
```

8. once the loop is done, check to make sure the latency file was created:

```
ls -l
```

8. To save the latency file outside of the cluster

```
kubectl cp -n cluster1-ol-team2 zeromq-client-txh59:k8s_healthOrderTime.txt ./k8s_healthOrderTime.txt
```

10. Then once you are done, you can delete all of ther services using the following:

```
kubectl delete deployment --all -n cluster1-ol-team2
kubectl delete service --all -n cluster1-ol-team2
kubectl delete job --all -n cluster1-ol-team2
kubectl delete pods --all -n cluster1-ol-team2
```

### ZeroMQ with Flatbuffers

1. Test ZeroMQ with Flatbuffers code on local Kubernets cluster
   * successful tested using local host
   * median latency times are presented in the table below after 100 observations

| Server  | Process | Median Latency Time |
| ------------- | ------------- | ----- |
| Health  | Serialization  | 0.565 msec  |
| Order  | Serialization  | 1.454 msec  |
| Health  | Deserialization  | 1.004 sec  |
| Order  | Deserialization  | 1.005 sec  |

#### Latency Plots

<img src="https://github.com/VUComputerNetworks/ol_team2/blob/main/ProgAssign1/Latency%20Data/K8s_ZeroMQ_FB/Serialization_Latency_Time_ZeroMQ_Flatbuffers.png" width=400>

<img src="https://github.com/VUComputerNetworks/ol_team2/blob/main/ProgAssign1/Latency%20Data/K8s_ZeroMQ_FB/Deserialization_Latency_Time_ZeroMQ_Flatbuffers.png" width=400>

#### Demo Movie

[<img src="https://github.com/VUComputerNetworks/ol_team2/blob/main/ProgAssign1/Demo%20Recordings/zeroMQ_FB_thumbnail.png" width="600" height="300"
/>](https://youtu.be/e33MvbZjeYo)

### gRPC with ProtoBuff

2. Test gRPC with ProtoBuff code on local Kubernets cluster
   * successful tested using local host
   * median latency times are presented in the table below after 100 observations

| Server  | Process | Median Latency Time |
| ------------- | ------------- | ----- |
| Health  | Serialization  | 7.73 msec  |
| Order  | Serialization  | 18.3 msec  |

#### Latency Plots

<img src="https://github.com/VUComputerNetworks/ol_team2/blob/main/ProgAssign1/Latency%20Data/K8s_grpc_Protobuf/Serialization_Latency_Time_gRPC_ProtoBuff.png" width=400>

#### Demo Movie

[<img src="https://github.com/VUComputerNetworks/ol_team2/blob/main/ProgAssign1/Demo%20Recordings/grpc_PB_thumbnail.png" width="600" height="300"
/>](https://youtu.be/E1Y__w_WhJc)
