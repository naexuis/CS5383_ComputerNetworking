# Program Assignment 3 Status 

Team members include: Adam Gibbons, Marcus Hilliard, and David Maples.

## Milestone 1: Create 5G Core Network Setup with Open5GS and UERANSIM

1. Show that you are able to get UERANSIM on VM1 and Open5GS or Free5GC working on VM2 with some sample application like iper3.
* Completed

### VM Configurations

UERANSIM is deployed on VM1 (IP 192.168.5.190)

Open5GS is deployed on VM2 (IP 192.168.5.178)

### Configure Firewall

From the VM home directory, enter the following commands:

```
sudo ufw status
```

If ufw is active, disable ufw by entering the following commands:

```
sudo ufw disable
```

### Restart VM

From the Chameleon Instance menu, navigate to the VM's console and perform a soft reboot.


### Installing UERANSIM

From the VM1 home directory, enter the following commands:

```
sudo apt update && sudo apt upgrade

sudo apt install make gcc g++ libsctp-dev lksctp-tools iproute2 -y

sudo snap install cmake --classic

cd Apps

git clone https://github.com/aligungr/UERANSIM

cd UERANSIM

make
```

We need to update the path to add the UERANSIM/build folder where the UERANSIM scripts are found

From the VM1 home directory, enter the following commands:

```
cd Apps

cd UERANSIM

cd build

pwd
```

The path to the USERANSIM build directory should be the following:

/home/cc/Apps/UERANSIM/build

From the VM1 home directory, enter the following commands:

```
nano .bashrc
```

Navigate to the bottom of the file and enter the following:

```
#Add Directory to PATH
export PATH=${PATH}:home/cc/Apps/UERANSIM/build
```

Save the file and exit nano. For the changes to take effect, we will need to enter the following commands:

```
source ~/.bashrc
```

### Restart VM

From the Chameleon Instance menu, navigate to the VM's console and perform a soft reboot.

### Configure UERANSIM

To configure amf yaml file; from the VM1 home directory, enter the following commands:

```
cd ~/Apps/UERANSIM/config/

la -l

cp open5gs-gnb.yaml custom_open5gs_gnb.yaml

cp open5gs-ue.yaml custom_open5gs_ue.yaml
```

#### Setup UE

```
cd ~/Apps/UERANSIM/config/

nano custom_open5gs_ue.yaml
```

Within the custom_open5gs_ue.yaml file:
1. Change the IMSI
2. Change the value of mcc to 001
3. Change the value of mnc to 01

```
# IMSI number of the UE. IMSI = [MCC|MNC|MSISDN] (In total 15 digits)
supi: 'imsi-999700000000001'      # CHANGE 1

# Mobile Country Code value of HPLMN
mcc: '999'     # CHANGE 2

# Mobile Network Code value of HPLMN (2 or 3 digits)
mnc: '70'      # CHANGE 3

# SUCI Protection Scheme : 0 for Null-scheme, 1 for Profile A and 2 for Profile>
protectionScheme: 0

# Home Network Public Key for protecting with SUCI Profile A
homeNetworkPublicKey: '5a8d38864820197c3394b92613b20b91633cbd897119273bf8e4a6f4>

# Home Network Public Key ID for protecting with SUCI Profile A
homeNetworkPublicKeyId: 1

# Routing Indicator
routingIndicator: '0000'

# Permanent subscription key
key: '465B5CE8B199B49FAA5F0A2EE238A6BC'

# Operator code (OP or OPC) of the UE
op: 'E8ED289DEBA952E4283B54E88E6183CA'

# This value specifies the OP type and it can be either 'OP' or 'OPC'
opType: 'OPC'

# Authentication Management Field (AMF) value
amf: '8000'

# IMEI number of the device. It is used if no SUPI is provided
imei: '356938035643803'

# IMEISV number of the device. It is used if no SUPI and IMEI is provided
imeiSv: '4370816125816151'

# List of gNB IP addresses for Radio Link Simulation
gnbSearchList:
  - 127.0.0.1  

```
AFTER CHANGES ARE MADE

```
# IMSI number of the UE. IMSI = [MCC|MNC|MSISDN] (In total 15 digits)
supi: 'imsi-001010000000001'

# Mobile Country Code value of HPLMN
mcc: '001'

# Mobile Network Code value of HPLMN (2 or 3 digits)
mnc: '01'

# SUCI Protection Scheme : 0 for Null-scheme, 1 for Profile A and 2 for Profile>
protectionScheme: 0

# Home Network Public Key for protecting with SUCI Profile A
homeNetworkPublicKey: '5a8d38864820197c3394b92613b20b91633cbd897119273bf8e4a6f4>

# Home Network Public Key ID for protecting with SUCI Profile A
homeNetworkPublicKeyId: 1

# Routing Indicator
routingIndicator: '0000'

# Permanent subscription key
key: '465B5CE8B199B49FAA5F0A2EE238A6BC'

# Operator code (OP or OPC) of the UE
op: 'E8ED289DEBA952E4283B54E88E6183CA'

# This value specifies the OP type and it can be either 'OP' or 'OPC'
opType: 'OPC'

# Authentication Management Field (AMF) value
amf: '8000'

# IMEI number of the device. It is used if no SUPI is provided
imei: '356938035643803'

# IMEISV number of the device. It is used if no SUPI and IMEI is provided
imeiSv: '4370816125816151'

# List of gNB IP addresses for Radio Link Simulation
gnbSearchList:
  - 127.0.0.1 

```

#### Setup gNB

```
cd ~/Apps/UERANSIM/config/

nano custom_open5gs_gnb.yaml
```

Within the custom_open5gs_gnb.yaml file:
1. Change the value of mcc to 001
2. Change the value of mnc to 
3. Change the ngapIp and gtpIp to the IP address of VM1 (192.168.5.190) where UERANSIM is running
4. Change the amfConfigs address to the IP address of VM2 (192.168.5.178) where Open5GS is running

```
mcc: '999'          # Mobile Country Code value                  # CHANGE 1
mnc: '70'           # Mobile Network Code value (2 or 3 digits)  # CHANGE 2

nci: '0x000000010'  # NR Cell Identity (36-bit)
idLength: 32        # NR gNB ID length in bits [22...32]
tac: 1              # Tracking Area Code

linkIp: 127.0.0.1   # gNB's local IP address for Radio Link Simulation (Usually same with local IP)
ngapIp: 127.0.0.1   # gNB's local IP address for N2 Interface (Usually same with local IP)          # CHANGE 3
gtpIp: 127.0.0.1    # gNB's local IP address for N3 Interface (Usually same with local IP)          # CHANGE 3

# List of AMF address information
amfConfigs:
  - address: 127.0.0.5        # CHANGE 4
    port: 38412

# List of supported S-NSSAIs by this gNB
slices:
  - sst: 1

# Indicates whether or not SCTP stream number errors should be ignored.
ignoreStreamIds: true

```

AFTER CHANGES ARE MADE

```
mcc: '001'          # Mobile Country Code value
mnc: '01'           # Mobile Network Code value (2 or 3 digits)

nci: '0x000000010'  # NR Cell Identity (36-bit)
idLength: 32        # NR gNB ID length in bits [22...32]
tac: 1              # Tracking Area Code

linkIp: 127.0.0.1       # gNB's local IP address for Radio Link Simulation (Usually same with local IP)
ngapIp: 192.168.5.190   # gNB's local IP address for N2 Interface (Usually same with local IP)
gtpIp: 192.168.5.190    # gNB's local IP address for N3 Interface (Usually same with local IP)

# List of AMF address information
amfConfigs:
  - address: 192.168.5.178
    port: 38412

# List of supported S-NSSAIs by this gNB
slices:
  - sst: 1

# Indicates whether or not SCTP stream number errors should be ignored.
ignoreStreamIds: true

```

### Installation Steps for Open5GS

From the VM2 home directory, enter the following commands:

```
sudo apt-get update

sudo apt-get install -y gnupg wget curl
```

#### Install MongoDB

From the VM2 home directory, enter the following commands:

```
sudo apt update

sudo apt install -y gnupg wget curl

curl -fsSL https://pgp.mongodb.com/server-6.0.asc | sudo gpg -o /usr/share/keyrings/mongodb-server-6.0.gpg --dearmor

echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

sudo apt update

sudo apt install -y mongodb-org

sudo systemctl start mongod

sudo systemctl enable mongod
```

### Installing Open5GS

From the VM2 home directory, enter the following commands:

```
sudo add-apt-repository ppa:open5gs/latest

sudo apt update

sudo apt install open5gs
```

### Restart VM

From the Chameleon Instance menu, navigate to the VM's console and perform a soft reboot.

### Install the Node.js

Node.js is required to install the WebUI of Open5GS. From the VM2 home directory, enter the following commands:

```
sudo apt update

sudo apt install -y ca-certificates curl gnupg

sudo mkdir -p /etc/apt/keyrings

curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg

NODE_MAJOR=20

echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | sudo tee /etc/apt/sources.list.d/nodesource.list

sudo apt update

sudo apt install nodejs -y
```

Verify that Node.js is installed by entering in the following commands:

```
nodejs -v
```

The current version is v20.10.0

### Configure Open5GS

#### Setup amf

To configure amf yaml file; from the VM2 home directory, enter the following commands:

```
cd /etc/open5gs

sudo nano amf.yaml
```

Within the amf.yaml file:
1. Change the IP address of the ngap to the IP address of VM2 (192.168.5.178) where Open5GS is running
2. Change the value of mcc to 001
3. Change the value of mnc to 01

```
amf:
    sbi:
      - addr: 127.0.0.5
        port: 7777
    ngap:
      - addr: 127.0.0.5  ##### CHANGE 1
    metrics:
      - addr: 127.0.0.5
        port: 9090
    guami:
      - plmn_id:
          mcc: 999      ##### CHANGE 2
          mnc: 70       ##### CHANGE 3
        amf_id:
          region: 2
          set: 1
    tai:
      - plmn_id:
          mcc: 999      ##### CHANGE 2
          mnc: 70       ##### CHANGE 3
        tac: 1
    plmn_support:
      - plmn_id:
          mcc: 999      ##### CHANGE 2
          mnc: 70       ##### CHANGE 3
        s_nssai:
          - sst: 1
    security:
        integrity_order : [ NIA2, NIA1, NIA0 ]
        ciphering_order : [ NEA0, NEA1, NEA2 ]
    network_name:
        full: Open5GS
    amf_name: open5gs-amf0

```

AFTER CHANGES ARE APPLIED

```
amf:
    sbi:
      - addr: 127.0.0.5
        port: 7777
    ngap:
      - addr: 192.168.5.178
    metrics:
      - addr: 127.0.0.5
        port: 9090
    guami:
      - plmn_id:
          mcc: 001
          mnc: 01
        amf_id:
          region: 2
          set: 1
    tai:
      - plmn_id:
          mcc: 001
          mnc: 01
        tac: 1
    plmn_support:
      - plmn_id:
          mcc: 001
          mnc: 01
        s_nssai:
          - sst: 1
    security:
        integrity_order : [ NIA2, NIA1, NIA0 ]
        ciphering_order : [ NEA0, NEA1, NEA2 ]
    network_name:
        full: Open5GS
    amf_name: open5gs-amf0

```

After saving the file, restart amf services by entering in the following commands:

```
sudo systemctl restart open5gs-amfd
```

#### Setup upf

To configure upf yaml file; from the VM2 home directory, enter the following commands:

```
sudo nano upf.yaml
```

Within the upf.yaml file:
1. Change the IP address of the gtpu to the IP address of VM2 (192.168.5.178) where Open5GS is running
2. Change the value of mcc to 001
3. Change the value of mnc to 01

```
upf:
    pfcp:
      - addr: 127.0.0.7
    gtpu:
      - addr: 127.0.0.7       ##### CHANGE 1
    subnet:
      - addr: 10.45.0.1/16
      - addr: 2001:db8:cafe::1/48
    metrics:
      - addr: 127.0.0.7
        port: 9090
```

AFTER CHANGES ARE APPLIED

```
upf:
    pfcp:
      - addr: 127.0.0.7
    gtpu:
      - addr: 192.168.5.178
    subnet:
      - addr: 10.45.0.1/16
      - addr: 2001:db8:cafe::1/48
    metrics:
      - addr: 127.0.0.7
        port: 9090
```

After saving the file, restart upf services by entering in the following commands:

```
sudo systemctl restart open5gs-upfd
```

### Install the WebUI of Open5GS

The WebUI allows you to interactively edit subscriber data. From the VM2 home directory, enter the following commands:

```
curl -fsSL https://open5gs.org/open5gs/assets/webui/install | sudo -E bash -
```

Let now access the WebUI from our local laptop VM by using ssh’s -L option and jumphost logic. From the local VM, access the WebUI be entering the following commands:

```
ssh -L 3000:localhost:3000 vm2
```

In the local VM, open a web browser and enter in the following commands:

```
localhost:3000
```

If the installation was successful, you should be able to connect to the WebUI interface where the default username is admin and the default pasword is 1423

<img src="https://github.com/VUComputerNetworks/ol_team2/blob/main/ProgAssign3/Images/Image1_Open5GS_Menu.png" width=400>

### Register UE Device

To add a new subscriber information, from the WebUI perform the following steps:

1. Go to Subscriber Menu.
2. Click + Button to add a new subscriber.
3. Fill the IMSI, security context(K, OPc, AMF), and APN of the subscriber.
4. Click SAVE Button

The default device information can be found in open5gs config on UERANSIM

* IMSI: 001010000000001
* Subscriber Key: 465B5CE8B199B49FAA5F0A2EE238A6BC
* USIM Type: OPc
* AMF: 8000
* Operator Key: E8ED289DEBA952E4283B54E88E6183CA

<img src="https://github.com/VUComputerNetworks/ol_team2/blob/main/ProgAssign3/Images/Image2_Open5GS_Menu.png" width=400>


### NAT Port Forwarding

From the VM2 home directory, where Open5GS is running, enter the following commands:

#### Enable IPv4/IPv6 Forwarding
```
sudo sysctl -w net.ipv4.ip_forward=1
sudo sysctl -w net.ipv6.conf.all.forwarding=1
```

#### Add NAT Rule
```
sudo iptables -t nat -A POSTROUTING -s 10.45.0.0/16 ! -o ogstun -j MASQUERADE
sudo ip6tables -t nat -A POSTROUTING -s 2001:db8:cafe::/48 ! -o ogstun -j MASQUERADE
```

#### Ensure that the packets in the INPUT chain to the ogstun interface are accepted
```
sudo iptables -I INPUT -i ogstun -j ACCEPT
```

### Start gNB and UE

From VM1, start gNB with the custom_open5gs_gnb.yaml config file by entering the following commands:

```
cd ~/Apps/UERANSIM/build

./nr-gnb -c ../config/custom_open5gs_gnb.yaml
```

<img src="https://github.com/VUComputerNetworks/ol_team2/blob/main/ProgAssign3/Images/Image1_UERANSIM_gNB.png" width=400>

From VM1, start UE with the custom_open5gs_ue.yaml config file by entering the following commands:

```
cd ~/Apps/UERANSIM/build

sudo ./nr-ue -c ../config/custom_open5gs_ue.yaml
```

<img src="https://github.com/VUComputerNetworks/ol_team2/blob/main/ProgAssign3/Images/Image1_UERANSIM_UE.png" width=400>

From VM1, verify that the uesimtun0 was created by entering the following commands:

```
ifconfig
```

uesimtun0 IP address: 10.45.0.2

<img src="https://github.com/VUComputerNetworks/ol_team2/blob/main/ProgAssign3/Images/Image1_UERANSIM_TUN.png" width=400>


### Checking Connectivity of the new TUN Interface on VM1

From the VM1 home directory, where UERANSIM is running, enter the following commands:

```
ping -I uesimtun0 www.google.com
```

<img src="https://github.com/VUComputerNetworks/ol_team2/blob/main/ProgAssign3/Images/Image1_UERANSIM_ping.png" width=400>


### nr-binder Utility: Simulating an App Execution

From the VM1 home directory, where UERANSIM is running, enter the following commands:

```
cd ~/Apps/UERANSIM/build

chmod +x ./nr-binder

./nr-binder 10.45.0.2 curl www.google.com
```

<img src="https://github.com/VUComputerNetworks/ol_team2/blob/main/ProgAssign3/Images/Image1_UERANSIM_binder_test_google.png" width=400>


### nr-binder Utility: iperf (client on VM1 and server on VM2)

From the VM2 home directory, where Open5GS is running, enter the following commands for the iperf server:

```
sudo apt install iperf3 -y

iperf3 -s
```

<img src="https://github.com/VUComputerNetworks/ol_team2/blob/main/ProgAssign3/Images/Image1_IPERF_server.png" width=400>

From the VM1 home directory, where UERANSIM is running, enter the following commands for the iperf client:

```
sudo apt install iperf3 -y

cd ~/Apps/UERANSIM/build

./nr-binder 10.45.0.2 iperf3 -c 192.168.5.178
```

<img src="https://github.com/VUComputerNetworks/ol_team2/blob/main/ProgAssign3/Images/Image1_IPERF_client.png" width=400>

## Milestone 2: Demostrate Client/Health/Order Communication Through Open5GS Stack

1. Install grocery/health client on one of the hosts of mininet 1 on VM1 and their corresponding servers on hosts of mininet2 in VM2 like you did in PA2
* Completed
2. Use nr_binder from UERANSIM to enable grocery/health client to send info to their servers. The servers receive information after going through Open5GS stack, which is on VM2.
* Completed

### Creating Topologies

Using the Mininet API, we programmatically created the following topologies on two virtual machines (i.e. VM1 and VM2). For VM2, the default path is provided in red.

<img src="https://github.com/VUComputerNetworks/ol_team2/blob/main/ProgAssign2/Images/PA2_Network_Topology.png" width=1200>

### Creating the VxLAN Tunnel

* IP ADDRESS FOR VM1: 192.168.5.190
* IP ADDRESS FOR VM2: 192.168.5.178

From VM1 enter the following commands:

```
sudo ip link add vxlan0 type vxlan id 100 local 192.168.5.190 remote 192.168.5.178 dev ens3 dstport 4789

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

Then verify creation of the tunnel using the following command on both VMs using the following command

```
ifconfig
```

<img src="https://github.com/VUComputerNetworks/ol_team2/blob/main/ProgAssign3/Images/Image_MS2_1.png" width=400>

From VM2 enter the following commands:

```
sudo ip link add vxlan0 type vxlan id 100 local 192.168.5.178 remote 192.168.5.190 dev ens3 dstport 4789

sudo ip addr add 192.168.100.3/24 dev vxlan0

sudo ip link set vxlan0 up

## connection for h1 on vm1
sudo ip route add 10.0.1.0/24 via 192.168.100.2 dev vxlan0

## connection for h2 on vm1
sudo ip route add 10.0.4.0/24 via 192.168.100.2 dev vxlan0

## connection for h3 on vm1
sudo ip route add 10.0.6.0/24 via 192.168.100.2 dev vxlan0
```

Then verify creation of the tunnel using the following command on both VMs using the following command

```
ifconfig
```

<img src="https://github.com/VUComputerNetworks/ol_team2/blob/main/ProgAssign3/Images/Image_MS2_2.png" width=400>

### How to run the code

To run the code on a Chameleon VM:
1. Navigate to the parent directory where the client/server files are located (i.e. FBHealth), then copy the directory to the VM using the following commands:

```
scp -r FBHealth vm1:/home/cc/

scp -r FBHealth vm2:/home/cc/
```

2. Navigate to the parent directory where the topology files are located, then copy the directory to the VM using the following commands:

```
scp vm1_*.py vm1:/home/cc/

scp vm2_*.py vm2:/home/cc/
```

3. Then open two terminals and ssh into each vm, using the following command to ssh into vm1:

```
ssh vm1
```

4. On vm1, start the vm1 python topology code using the following command:

```
sudo python vm1_topology.py
```

5. On vm2, start the vm2 python topology code using the following command:

```
sudo python vm2_topology.py
```

### Demostrate communication between topologies

From vm1, enter the following command to trace the route between host 2 on vm1 at 10.0.4.254 and host T on vm2 at 10.0.51.254:

```
h2 traceroute 10.0.51.254
```

<img src="https://github.com/VUComputerNetworks/ol_team2/blob/main/ProgAssign3/Images/Image_MS2_3.png" width=400>

For reference:

<img src="https://github.com/VUComputerNetworks/ol_team2/blob/main/ProgAssign2/Images/PA2_Network_Topology.png" width=1200>


### Demostrate communication between topologies using iperf3

From the VM2 home directory, enter the following commands for the iperf server to run on host 7 at 10.0.53.254:

```
h7 iperf3 -s
```

<img src="https://github.com/VUComputerNetworks/ol_team2/blob/main/ProgAssign3/Images/Image_MS2_5.png" width=400>

From the VM1 home directory, enter the following commands for the iperf client to run on host 2 at 10.0.4.254:

```
h2 iperf3 -c 10.0.53.254
```

<img src="https://github.com/VUComputerNetworks/ol_team2/blob/main/ProgAssign3/Images/Image_MS2_6.png" width=400>

#### Setup UE in Mininet

We are planning to start gNB on host 2 at 10.0.4.254 using the the custom_open5gs_gnb.yaml file, thus we need to change the gnbSearchList in the custom_open5gs_ue.yaml file.

From the VM1 home directory, where UERANSIM is running, enter the following commands: 

```
cd ~/Apps/UERANSIM/config/

nano custom_open5gs_ue.yaml
```

Within the custom_open5gs_ue.yaml file:
1. Change the IP address of gnbSearchList to the IP address of host 2 ( 10.0.4.254 ) where gNB is runing.

```
# IMSI number of the UE. IMSI = [MCC|MNC|MSISDN] (In total 15 digits)
supi: 'imsi-001010000000001'

# Mobile Country Code value of HPLMN
mcc: '001'

# Mobile Network Code value of HPLMN (2 or 3 digits)
mnc: '01'

# SUCI Protection Scheme : 0 for Null-scheme, 1 for Profile A and 2 for Profile>
protectionScheme: 0

# Home Network Public Key for protecting with SUCI Profile A
homeNetworkPublicKey: '5a8d38864820197c3394b92613b20b91633cbd897119273bf8e4a6f4>

# Home Network Public Key ID for protecting with SUCI Profile A
homeNetworkPublicKeyId: 1

# Routing Indicator
routingIndicator: '0000'

# Permanent subscription key
key: '465B5CE8B199B49FAA5F0A2EE238A6BC'

# Operator code (OP or OPC) of the UE
op: 'E8ED289DEBA952E4283B54E88E6183CA'

# This value specifies the OP type and it can be either 'OP' or 'OPC'
opType: 'OPC'

# Authentication Management Field (AMF) value
amf: '8000'

# IMEI number of the device. It is used if no SUPI is provided
imei: '356938035643803'

# IMEISV number of the device. It is used if no SUPI and IMEI is provided
imeiSv: '4370816125816151'

# List of gNB IP addresses for Radio Link Simulation
gnbSearchList:
  - 127.0.0.1        # CHANGE 1 

```
AFTER CHANGES ARE MADE

```
# IMSI number of the UE. IMSI = [MCC|MNC|MSISDN] (In total 15 digits)
supi: 'imsi-001010000000001'

# Mobile Country Code value of HPLMN
mcc: '001'

# Mobile Network Code value of HPLMN (2 or 3 digits)
mnc: '01'

# SUCI Protection Scheme : 0 for Null-scheme, 1 for Profile A and 2 for Profile>
protectionScheme: 0

# Home Network Public Key for protecting with SUCI Profile A
homeNetworkPublicKey: '5a8d38864820197c3394b92613b20b91633cbd897119273bf8e4a6f4>

# Home Network Public Key ID for protecting with SUCI Profile A
homeNetworkPublicKeyId: 1

# Routing Indicator
routingIndicator: '0000'

# Permanent subscription key
key: '465B5CE8B199B49FAA5F0A2EE238A6BC'

# Operator code (OP or OPC) of the UE
op: 'E8ED289DEBA952E4283B54E88E6183CA'

# This value specifies the OP type and it can be either 'OP' or 'OPC'
opType: 'OPC'

# Authentication Management Field (AMF) value
amf: '8000'

# IMEI number of the device. It is used if no SUPI is provided
imei: '356938035643803'

# IMEISV number of the device. It is used if no SUPI and IMEI is provided
imeiSv: '4370816125816151'

# List of gNB IP addresses for Radio Link Simulation
gnbSearchList:
  - 10.0.4.254

```

#### Setup gNB in Mininet

We are planning to start gNB on host 2 at 10.0.4.254 using the the custom_open5gs_gnb.yaml file, thus we need to change the linkIp in the custom_open5gs_gnb.yaml file.

From the VM1 home directory, where UERANSIM is running, enter the following commands: 

```
cd ~/Apps/UERANSIM/config/

nano custom_open5gs_gnb.yaml
```

Within the custom_open5gs_gnb.yaml file:
1. Change the linkIp, ngapIp, and gtpIp  to the IP address of host 2 ( 10.0.4.254 ) where gNB is runing.

```
mcc: '001'          # Mobile Country Code value
mnc: '01'           # Mobile Network Code value (2 or 3 digits)

nci: '0x000000010'  # NR Cell Identity (36-bit)
idLength: 32        # NR gNB ID length in bits [22...32]
tac: 1              # Tracking Area Code

linkIp: 127.0.0.1       # gNB's local IP address for Radio Link Simulation (Usually same with local IP)     # CHANGE 1
ngapIp: 192.168.5.190   # gNB's local IP address for N2 Interface (Usually same with local IP)              # CHANGE 1
gtpIp:  192.168.5.190    # gNB's local IP address for N3 Interface (Usually same with local IP)              # CHANGE 1

# List of AMF address information
amfConfigs:
  - address: 192.168.5.178
    port: 38412

# List of supported S-NSSAIs by this gNB
slices:
  - sst: 1

# Indicates whether or not SCTP stream number errors should be ignored.
ignoreStreamIds: true

```

AFTER CHANGES ARE MADE

```
mcc: '001'          # Mobile Country Code value
mnc: '01'           # Mobile Network Code value (2 or 3 digits)

nci: '0x000000010'  # NR Cell Identity (36-bit)
idLength: 32        # NR gNB ID length in bits [22...32]
tac: 1              # Tracking Area Code

linkIp: 10.0.4.254       # gNB's local IP address for Radio Link Simulation (Usually same with local IP)
ngapIp: 10.0.4.254   # gNB's local IP address for N2 Interface (Usually same with local IP)
gtpIp:  10.0.4.254    # gNB's local IP address for N3 Interface (Usually same with local IP)

# List of AMF address information
amfConfigs:
  - address: 192.168.5.178
    port: 38412

# List of supported S-NSSAIs by this gNB
slices:
  - sst: 1

# Indicates whether or not SCTP stream number errors should be ignored.
ignoreStreamIds: true

```


### Start gNB and UE

From VM1, start gNB on host 2 at 10.0.4.254 with the custom_open5gs_gnb.yaml config file by entering the following commands:

```
h2 ls
h2 cd Apps
h2 cd UERANSIM
h2 cd build
h2 ls

h2 ./nr-gnb -c ../config/custom_open5gs_gnb.yaml &
```

<img src="https://github.com/VUComputerNetworks/ol_team2/blob/main/ProgAssign3/Images/Image_MS2_7.png" width=400>


From VM1, start UE on host 3 at 10.0.6.254 with the custom_open5gs_ue.yaml config file by entering the following commands:

```
h3 ls
h3 cd Apps
h3 cd UERANSIM
h3 cd build
h3 ls

h3 sudo ./nr-ue -c ../config/custom_open5gs_ue.yaml &
```

<img src="https://github.com/VUComputerNetworks/ol_team2/blob/main/ProgAssign3/Images/Image_MS2_8.png" width=400>


From the VM2 mininet, enter the following commands for the iperf server to run on host 7 at 10.0.53.254:

```
h7 iperf3 -s
```

From the VM1 mininet, enter the following commands for the iperf client to run on host 3 at 10.0.6.254:


```
h3 ./nr-binder 10.45.0.2 iperf3 -c 10.0.53.254
```

Showing the communication of the iperf3 client:

<img src="https://github.com/VUComputerNetworks/ol_team2/blob/main/ProgAssign3/Images/Image_MS2_9.png" width=400>

Showing the communication of the iperf3 server:

<img src="https://github.com/VUComputerNetworks/ol_team2/blob/main/ProgAssign3/Images/Image_MS2_10.png" width=400>

We can trace the route from the client to the server be entering in the following commands:

```
h3 ./nr-binder 10.45.0.2 traceroute 10.0.53.254
```

<img src="https://github.com/VUComputerNetworks/ol_team2/blob/main/ProgAssign3/Images/Image_MS2_11.png" width=400>

For reference:

<img src="https://github.com/VUComputerNetworks/ol_team2/blob/main/ProgAssign2/Images/PA2_Network_Topology.png" width=1200>


### ZeroMQ with Flatbuffers

Tested custom topologies with ZeroMQ with Flatbuffers code

On vm1, we are going to run the client on host 3 at 10.0.6.254; on vm2, we are going to run the health server on host 7 (i.e. Node U) at 10.0.53.254 and run the order server on host 5 (i.e. Node V) at 10.0.49.254.

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

On vm1, we will run the client server on host 2 by accessing the code from the host using the following commands:

```
h3 ls

h3 cd /home/cc/FBHealth

h3 /home/cc/Apps/UERANSIM/build/nr-binder 10.45.0.2 python3 tcp_client.py --addrHealth 10.0.53.254 --addrOrder 10.0.49.254 --iterLoop 100 --portHealth 5555 --portOrder 5556 --fileName /home/cc/FBHealth/open5gs_healthOrderTime
```

To save the latency data, enter the following commands from the local VM:

```
scp vm1:/home/cc/FBHealth/open5gs_healthOrderTime.txt .
```


#### Latency Data

Median latency times are presented in the table below after 100 observations

| Server  | Process | Median Latency Time |
| ------------- | ------------- | ----- |
| Health  | Serialization  | 0.549 msec  |
| Order  | Serialization  | 2.162 msec  |
| Health  | Deserialization  | 1.004 sec  |
| Order  | Deserialization  | 1.005 sec  |

#### Serialization Latency Plot

<img src="https://github.com/VUComputerNetworks/ol_team2/blob/main/ProgAssign3/Images/Image_MS2_12.png" width=400>

#### Deserialization Latency Plot

<img src="https://github.com/VUComputerNetworks/ol_team2/blob/main/ProgAssign3/Images/Image_MS2_13.png" width=400>

#### Demo Movie

[<img src="https://github.com/VUComputerNetworks/ol_team2/blob/main/ProgAssign1/Demo%20Recordings/zeroMQ_FB_thumbnail.png" width="600" height="300"
/>](https://youtu.be/1FvKM-_5p1M)

