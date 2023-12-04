# Program Assignment 2 Status 

Team members include: Adam Gibbons, Marcus Hilliard, and David Maples.

## Milestone 1: Create VxLAN on Chameleon and Demonstrate Simple Mininet Communication

1. Show that you are able to create the VxLAN and demonstrate communication between two simple Mininet topologies (2 hosts per mininet).
* Completed
2. Add the commands used, status update of progress made and contributions by the team in your repository.
* Completed

### Creating Chameleon SSH Key

From the Chameleon Dashboard

Click on Experiment > select KVM@TACC

Click on Key Pairs

Click on Create Key Pair > input name for the key and select SSH Key under Key Type

Save the file to local directory

### Creating the VM Instance

From the Chameleon Dashboard

Click on Experiment > select KVM@TACC

Click on Instances

Click on Launch Instance

In the Launch Instance Menu:

In the Details menu > Instance Name > input name

Click Next

In the Source menu > Select Boot Source > select Image

In the Source menu > in the search bar under Available, enter ubuntu22, then click the up arrow for CC-Ubuntu22.04

Click Next

In the Flavor menu > click the up arrow for m1.medium

Click Next

In the Networks menu > click the up arrow for CH-822922-net

Click Next

Click Next

In the Security Groups menu > click the up arrow for ENABLE_SSH and ENABLE_ICMP

In the Key Pair > click the up arrow for the key pair that was created

Click Launch


### Copying the Permission file to the SHH Directory

From the home directory

```
ls -la
```

You should see a directory called .ssh/

Copy the pem key to the directory using the following commands

```
cp online_team2_key.pem .ssh/
```

Change the permissions for the pem file using the following commands

```
cd .ssh/

ls -l

chmod go-r *.pem
```


### Creating SSH Configuration File

From the home directory, open text editor and copy the following text into the file:

```
# Bastion used as the jump host
Host bastion
   User cc
   Hostname 129.114.25.15
   Port 22
   IdentityFile ~/.ssh/F23_4383_5383.pem
   StrictHostKeyChecking no

# Online Team2 VM1
Host vm1
   ProxyJump bastion
   Hostname 192.168.5.249
   User cc
   Port 22
   IdentityFile ~/.ssh/online_team2_key.pem
   StrictHostKeyChecking no

# Online Team2 VM2
Host vm2
   ProxyJump bastion
   Hostname 192.168.5.139
   User cc
   Port 22
   IdentityFile ~/.ssh/online_team2_key.pem
   StrictHostKeyChecking no
```

Save the file and name it pa_ol_team2_config

From the home directory, copy the file to the ssh directory and rename it config using the following commands:

```
cp pa_ol_team2_config .ssh/config

cd .ssh/

ls -l
```

Verify that the config file was copied into the directory by using the following command:

```
nano config
```

Exit out of nano

From the shh directory, you need to remove the file known_hosts by using the following command:

```
rm known_hosts

ls -l
```

Verify that the known_hosts file was removed

From the home directory, now ssh into the VM1 using the following commands:

```
ssh vm1
```

### Installing Basic Software

From the VM1 home directory, you are now able to setup the VM using the following commands:

```
sudo apt update && sudo apt install cmake git gcc g++ clang default-jdk python3-dev python3-pip wget net-tools dnsutils iputils-ping iputils-tracepath iputils-arping iputils-clockdiff inetutils-traceroute emacs vim libzmq3-dev -y

sudo -H python3 -m pip install --upgrade pyzmq grpcio grpcio-tools

sudo apt update && sudo apt install protobuf-compiler -y
```


### Installing Flatbuffers

From the VM1 home directory, instal flatbuffers using the following commands:

```
mkdir Apps

cd Apps

git clone https://github.com/google/flatbuffers

cd flatbuffers

cmake -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release

make

sudo make install

sudo -H python3 -m pip install --upgrade flatbuffers
```

From the home directory, verify that flatbuffers were installed by using the following commands:

```
cd

which flatc
```


### Installing Mininet

From the home directory, install mininet by using the following commands:

```
cd Apps

git clone https://github.com/mininet/mininet

cd mininet

./util/install.sh -a
```

From the home directory, verify that mininet were installed by using the following commands:

```
sudo mn

quit
```

### Creating the VxLAN Tunnel

* IP ADDRESS FOR VM1: 192.168.5.249
* IP ADDRESS FOR VM2: 192.168.5.139

From VM1 enter the following commands:

```
sudo ip link add vxlan0 type vxlan id 100 local 192.168.5.249 remote 192.168.5.139 dev ens3 dstport 4789

sudo ip addr add 192.168.100.2/24 dev vxlan0

sudo ip link set vxlan0 up
```

Then verify creation of the tunnel using the following command on both VMs using the following command

```
ifconfig
```

<img src="https://github.com/VUComputerNetworks/ol_team2/blob/main/ProgAssign2/Images/PA2_MS1_1.png" width=400>

From VM2 enter the following commands:

```
sudo ip link add vxlan0 type vxlan id 100 local 192.168.5.139 remote 192.168.5.249 dev ens3 dstport 4789

sudo ip addr add 192.168.100.3/24 dev vxlan0

sudo ip link set vxlan0 up
```

Then verify creation of the tunnel using the following command on both VMs using the following command

```
ifconfig
```

<img src="https://github.com/VUComputerNetworks/ol_team2/blob/main/ProgAssign2/Images/PA2_MS1_2.png" width=400>


### Demonstrate Simple Mininet Communication

On VM1, enter the following commands:

```
sudo mn --nat -i 10.10.1.0/24
```

Open a second terminal window and verify that the mininet subnet has been added to the routing table

```
route -n
```

<img src="https://github.com/VUComputerNetworks/ol_team2/blob/main/ProgAssign2/Images/PA2_MS1_3.png" width=400>

VM1 route table, you are ADDing the VM2 mininet and VM2 VxLAN ip address

```
sudo ip route add 10.10.2.0/24 via 192.168.100.3 dev vxlan0
```


Using the following command you can verify that the new route was added:

```
route -n
```

<img src="https://github.com/VUComputerNetworks/ol_team2/blob/main/ProgAssign2/Images/PA2_MS1_4.png" width=400>

On VM2, enter the following commands:

```
sudo mn --nat -i 10.10.2.0/24
```

Open a second terminal window and verify that the mininet subnet has been added to the routing table

```
route -n
```

<img src="https://github.com/VUComputerNetworks/ol_team2/blob/main/ProgAssign2/Images/PA2_MS1_5.png" width=400>

VM2 route table, you are ADDing the VM1 minitnet and the VM1 VxLAN ip address

```
sudo ip route add 10.10.1.0/24 via 192.168.100.2 dev vxlan0
```

Using the following command you can verify that the new route was added:

```
route -n
```

<img src="https://github.com/VUComputerNetworks/ol_team2/blob/main/ProgAssign2/Images/PA2_MS1_6.png" width=400>

On VM1 enter the following commands:

```
h1 ping 10.10.2.1
```

The above command will send a ping to VM2 using the VxLAN, and then you will see the return information

<img src="https://github.com/VUComputerNetworks/ol_team2/blob/main/ProgAssign2/Images/PA2_MS1_7.png" width=400>

On VM2 enter the following commands:

```
h1 ping 10.10.1.1
```

The above command will send a ping to VM1 using the VxLAN and you will see the return information

<img src="https://github.com/VUComputerNetworks/ol_team2/blob/main/ProgAssign2/Images/PA2_MS1_8.png" width=400>

## Milestone 2: Create Mininet Topologies and Demonstrate Communication using Client/Health/Order Clients

1. Programmatically create the topologies using Mininet APIs. When adding links, play with bandwidths and delays and losses properties as these can give you different latency results.
   * Completed
2. Hardcode the routing paths in each router. For the right-hand side topology, use your solution from HW1 Prob 5.
   * Completed
3. Show end to end communication
   * Completed
4. Add status update of progress made and contributions by the team in your repository.
   * Completed


### Creating Topologies

Using the Mininet API, we programmatically created the following topologies on two virtual machines (i.e. VM1 and VM2). For VM2, the default path is provided in red.

<img src="https://github.com/VUComputerNetworks/ol_team2/blob/main/ProgAssign2/Images/PA2_Network_Topology.png" width=1200>

### Creating the VxLAN Tunnel

* IP ADDRESS FOR VM1: 192.168.5.249
* IP ADDRESS FOR VM2: 192.168.5.139

From VM1 enter the following commands:

```
sudo ip link add vxlan0 type vxlan id 100 local 192.168.5.249 remote 192.168.5.139 dev ens3 dstport 4789

sudo ip addr add 192.168.100.2/24 dev vxlan0

sudo ip link set vxlan0 up

## connection for h1 on vm2
sudo ip route add 10.0.40.0/24 via 192.168.100.3 dev vxlan0

## connection for h2 on vm2
sudo ip route add 10.0.43.0/24 via 192.168.100.3 dev vxlan0

## connection for h3 on vm2
sudo ip route add 10.0.45.0/24 via 192.168.100.3 dev vxlan0

## connection for h4 on vm2
sudo ip route add 10.0.47.0/24 via 192.168.100.3 dev vxlan0

## connection for h5 on vm2
sudo ip route add 10.0.49.0/24 via 192.168.100.3 dev vxlan0

## connection for h6 on vm2
sudo ip route add 10.0.51.0/24 via 192.168.100.3 dev vxlan0

## connection for h7 on vm2
sudo ip route add 10.0.53.0/24 via 192.168.100.3 dev vxlan0

## connection for h8 on vm2
sudo ip route add 10.0.55.0/24 via 192.168.100.3 dev vxlan0
```

From VM2 enter the following commands:

```
sudo ip link add vxlan0 type vxlan id 100 local 192.168.5.139 remote 192.168.5.249 dev ens3 dstport 4789

sudo ip addr add 192.168.100.3/24 dev vxlan0

sudo ip link set vxlan0 up

## connection for h1 on vm1
sudo ip route add 10.0.1.0/24 via 192.168.100.2 dev vxlan0

## connection for h2 on vm1
sudo ip route add 10.0.4.0/24 via 192.168.100.2 dev vxlan0

## connection for h3 on vm1
sudo ip route add 10.0.6.0/24 via 192.168.100.2 dev vxlan0
```

### How to run the code

To run the code on a Chameleon VM:
1. Navigate to the parent directory where the files are located (i.e. FBHealth), then copy the directory to the VM using the following commands:

```
scp -r FBHealth vm1:/home/cc/

scp -r FBHealth vm2:/home/cc/
```

2. Then open two terminals and ssh into each vm, using the following command to ssh into vm1:

```
ssh vm1
```

3. On vm1, start the vm1 python topology code using the following command:

```
sudo python vm1_topology.py
```

4. On vm2, start the vm2 python topology code using the following command:

```
sudo python vm2_topology.py
```

### To demostrate communication between topologies

From vm1, enter the following command to trace the route between host 2 on vm1 at 10.0.4.254 and host T on vm2 at 10.0.51.254:

```
h2 traceroute 10.0.51.254
```

<img src="https://github.com/VUComputerNetworks/ol_team2/blob/main/ProgAssign2/Images/PA2_MS2_Demo_Communication_traceroute.png" width=400>

<img src="https://github.com/VUComputerNetworks/ol_team2/blob/main/ProgAssign2/Images/PA2_MS2_Demo_Communication_ping.png" width=400>

### ZeroMQ with Flatbuffers

Tested custom topologies with ZeroMQ with Flatbuffers code

On vm1, we are going to run the client on host 2 at 10.0.4.254; on vm2, we are going to run the health server on host 7 (i.e. Node U) at 10.0.53.254 and run the order server on host 5 (i.e. Node V) at 10.0.49.254.

On vm1, we will run the client server on host 2 by accessing the code from the host using the following commands:

```
h2 ls

h2 cd /home/cc/FBHealth

h2 python3 tcp_client.py --addrHealth 10.0.53.254 --addrOrder 10.0.49.254 --iterLoop 100 --portHealth 5555 --portOrder 5556 --fileName k8s_healthOrderTime
```

On vm2, we will run the order server on host 5 by accessing the code from the host using the following commands:

```
h5 ls

h5 cd /home/cc/FBHealth

h5 python3 tcp_server_order.py &
```

Please note, by using the "&" at the end of the command, will allow the code to run in the background, while the user is able to continue with the additional commands to run the health server.

On vm2, we will run the health server on host 7 by accessing the code from the host using the following commands:

```
h7 ls

h7 cd /home/cc/FBHealth

h7 python3 tcp_server_health.py
```

#### Latency Data

Median latency times are presented in the table below after 100 observations

| Server  | Process | Median Latency Time |
| ------------- | ------------- | ----- |
| Health  | Serialization  | 0.394 msec  |
| Order  | Serialization  | 2.087 msec  |
| Health  | Deserialization  | 1.003 sec  |
| Order  | Deserialization  | 1.005 sec  |

#### Serialization Latency Plot

<img src="https://github.com/VUComputerNetworks/ol_team2/blob/main/ProgAssign2/Images/PA2_MS2_Serilization.png" width=400>

#### Deserialization Latency Plot

<img src="https://github.com/VUComputerNetworks/ol_team2/blob/main/ProgAssign2/Images/PA2_MS2_Deserilization.png" width=400>

#### Demo Movie

[<img src="https://github.com/VUComputerNetworks/ol_team2/blob/main/ProgAssign1/Demo%20Recordings/zeroMQ_FB_thumbnail.png" width="600" height="300"
/>](https://youtu.be/BKBp_3lV7lo)
