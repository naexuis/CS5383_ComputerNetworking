#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI

class LinuxRouter (Node):
    def config (self, **params):
        super (LinuxRouter, self).config (**params)
        self.cmd ('sysctl net.ipv4.ip_forward=1')

    def terminate (self):
        self.cmd ('sysctl net.ipv4.ip_forward=0')
        super (LinuxRouter, self).terminate ()


class NetworkTopo (Topo):

    def build(self, **_opts):

        #################################################################################
        #### Block 1 ####
        router1 = self.addNode('r1', cls=LinuxRouter, ip='10.0.1.1/24')

        switch1 = self.addSwitch('s1')

        host1 = self.addHost('h1', ip='10.0.1.254/24', defaultRoute='via 10.0.1.1')

        self.addLink(host1, switch1)

        self.addLink(switch1, router1,
                intfName2='r1-s1-eth', params2={'ip':'10.0.1.1/24'})

        #################################################################################
        #### Block 2 ####
        router2 = self.addNode('r2', cls=LinuxRouter, ip='10.0.4.1/24')

        switch2 = self.addSwitch('s2')

        host2 = self.addHost('h2', ip='10.0.4.254/24', defaultRoute='via 10.0.4.1')

        self.addLink(host2, switch2)

        self.addLink(switch2, router2,
                intfName2='r2-s2-eth', params2={'ip':'10.0.4.1/24'})

        #################################################################################
        #### LINK Block 2 to Block 1 ####
        self.addLink(router2, router1,
                intfName1='r2-r1-eth', params1={'ip':'10.0.5.1/24'},
                intfName2='r1-r2-eth', params2={'ip':'10.0.5.2/24'})

        #################################################################################
        #### Block 3 ####
        router3 = self.addNode('r3', cls=LinuxRouter, ip='10.0.6.1/24')

        switch3 = self.addSwitch('s3')

        host3 = self.addHost('h3', ip='10.0.6.254/24', defaultRoute='via 10.0.6.1')

        self.addLink(host3, switch3)

        self.addLink(switch3, router3,
                intfName2='r3-s3-eth', params2={'ip':'10.0.6.1/24'})

        #################################################################################
        #### LINK Block 3 to Block 2 ####
        self.addLink(router3, router2,
                intfName1='r3-r2-eth', params1={'ip':'10.0.7.1/24'},
                intfName2='r2-r3-eth', params2={'ip':'10.0.7.2/24'})

        #################################################################################
        #### LINK Block 3 to Block 1 ####
        self.addLink(router3, router1,
                intfName1='r3-r1-eth', params1={'ip':'10.0.8.1/24'},
                intfName2='r1-r3-eth', params2={'ip':'10.0.8.2/24'})


def run():
    # Then create the network object from this topology
    net = Mininet(topo=NetworkTopo())

    net.addNAT(name='nat1', ip='10.0.3.1').configDefault()

    net.addLink(net['r1'], net['nat1'],
                intfName1='r1-nat-eth', params1={'ip':'10.0.2.1/24'},
                intfName2='nat-r1-eth', params2={'ip':'10.0.2.2/24'})

    #####################################################################################
    #####################################################################################

    # CONNECTING ROUTES
    # add {destination} via {other side intf ip} dev {this side intf name}
    # if I need to reach a destination (ip add) - what is the direct next step (via ... dev ...)

    ## CONNECTION NAT TO HOSTS
    # connecting host1 via r1-nat-eth to nat
    info(net['nat1'].cmd('ip route add 10.0.1.0/24 via 10.0.2.1 dev nat-r1-eth'))
    # connecting host2 via r1-nat-eth to nat
    info(net['nat1'].cmd('ip route add 10.0.4.0/24 via 10.0.2.1 dev nat-r1-eth'))
    # connecting host3 via r1-nat-eth to nat
    info(net['nat1'].cmd('ip route add 10.0.6.0/24 via 10.0.2.1 dev nat-r1-eth'))

    ## CONNECTION NAT TO ROUTERS
    # connecting nat via nat-r1-eth to r1
    info(net['r1'].cmd('ip route add 10.0.3.0/24 via 10.0.2.2 dev r1-nat-eth'))
    # connecting nat via r2-r1-eth to r2
    info(net['r2'].cmd('ip route add 10.0.3.0/24 via 10.0.5.2 dev r2-r1-eth'))
    # connecting nat via r3-r1-eth to r3
    info(net['r3'].cmd('ip route add 10.0.3.0/24 via 10.0.8.2 dev r3-r1-eth'))

    #####################################################################################
    
    ## ROUTER 1 CONNECTIONS
    info(net['r1'].cmd('ip route add default via 10.0.2.2 dev r1-nat-eth'))
    # connection host2 via r2-r1-eth to r1
    info(net['r1'].cmd('ip route add 10.0.4.0/24 via 10.0.5.1 dev r1-r2-eth'))
    # connection host3 via r3-r1-eth to r1
    info(net['r1'].cmd('ip route add 10.0.6.0/24 via 10.0.8.1 dev r1-r3-eth'))

    ## ROUTER 2 CONNECTIONS
    info(net['r2'].cmd('ip route add default via 10.0.5.2 dev r2-r1-eth'))
    # connection host1 via r1-r2-eth to r2
    info(net['r2'].cmd('ip route add 10.0.1.0/24 via 10.0.5.2 dev r2-r1-eth'))
    # connection host3 via r3-r1-eth to r2
    info(net['r2'].cmd('ip route add 10.0.6.0/24 via 10.0.7.1 dev r2-r3-eth'))

    ## ROUTER 3 CONNECTIONS
    info(net['r3'].cmd('ip route add default via 10.0.8.2 dev r3-r1-eth'))
    # connection host1 via r1-r3-eth to r3
    info(net['r3'].cmd('ip route add 10.0.1.0/24 via 10.0.8.2 dev r3-r1-eth'))
    # connection host2 via r1-r3-eth to r3
    info(net['r3'].cmd('ip route add 10.0.4.0/24 via 10.0.7.2 dev r3-r2-eth'))

    #####################################################################################

    # DEFAULT HOST ROUTES
    info(net['h1'].cmd('ip route add default via 10.0.1.1'))
    info(net['h2'].cmd('ip route add default via 10.0.4.1'))
    info(net['h3'].cmd('ip route add default via 10.0.6.1'))

    #####################################################################################
    #####################################################################################

    ## DEFAULT NAT ROUTE
    info(net['nat1'].cmd('ip route add default via 192.168.100.3 dev vxlan0'))

    ## IPTABLE
    info(net['nat1'].cmd('iptables -D FORWARD -i nat1-eth0 -d 10.0.0.0/8 -j DROP'))

    info( '*** Starting network\n')
    net.start ()  # this method must be invoked to start the mininet

    
    info( '*** Running CLI\n' )
    CLI (net)   # this gives us mininet prompt

    info( '*** Stopping network' )
    net.stop ()  # this cleans up the network


if __name__ == '__main__':
    setLogLevel('info')
    run()