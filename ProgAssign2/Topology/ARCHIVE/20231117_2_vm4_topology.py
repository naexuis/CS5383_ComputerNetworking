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
        router1 = self.addNode('r1', cls=LinuxRouter, ip='10.0.40.1/24')

        switch1 = self.addSwitch('s1')
        
        host1 = self.addHost('h1', ip='10.0.40.254/24', defaultRoute='via 10.0.40.1')
        
        self.addLink(host1, switch1)
        
        self.addLink(switch1, router1,
                intfName2='r1-s1-eth', params2={'ip':'10.0.40.1/24'})

        #################################################################################
        #### Block 2 ####
        switch2 = self.addSwitch('s2')

        host2 = self.addHost('h2', ip='10.0.43.254/24', defaultRoute='via 10.0.43.1')

        self.addLink(host2, switch2)

        self.addLink(switch2, router1,
                intfName2='r1-s2-eth', params2={'ip':'10.0.43.1/24'})

        #################################################################################
        #### Block 3 ####
        router3 = self.addNode('r3', cls=LinuxRouter, ip='10.0.45.1/24')

        switch3 = self.addSwitch('s3')
        
        host3 = self.addHost('h3', ip='10.0.45.254/24', defaultRoute='via 10.0.45.1')
        
        self.addLink(host3, switch3)
        
        self.addLink(switch3, router3,
                intfName2='r3-s3-eth', params2={'ip':'10.0.45.1/24'})

        #################################################################################
        #### LINK Block 3 to Block 1 ####
        self.addLink(router3, router1,
                intfName1='r3-r1-eth', params1={'ip':'10.0.44.1/24'},
                intfName2='r1-r3-eth', params2={'ip':'10.0.44.2/24'})

        #################################################################################
        #### Block 4 ####
        router4 = self.addNode('r4', cls=LinuxRouter, ip='10.0.47.1/24')

        switch4 = self.addSwitch('s4')
        
        host4 = self.addHost('h4', ip='10.0.47.254/24', defaultRoute='via 10.0.47.1')
        
        self.addLink(host4, switch4)
        
        self.addLink(switch4, router4,
                intfName2='r4-s4-eth', params2={'ip':'10.0.47.1/24'})

        #################################################################################
        #### LINK Block 4 to Block 3 ####
        self.addLink(router4, router3,
                intfName1='r4-r3-eth', params1={'ip':'10.0.46.1/24'},
                intfName2='r3-r4-eth', params2={'ip':'10.0.46.2/24'})

        #################################################################################
        #### Block 5 ####
        router5 = self.addNode('r5', cls=LinuxRouter, ip='10.0.49.1/24')

        switch5 = self.addSwitch('s5')
        
        host5 = self.addHost('h5', ip='10.0.49.254/24', defaultRoute='via 10.0.49.1')
        
        self.addLink(host5, switch5)
        
        self.addLink(switch5, router5,
                intfName2='r5-s5-eth', params2={'ip':'10.0.49.1/24'})

        #################################################################################
        #### LINK Block 5 to Block 4 ####
        self.addLink(router5, router4,
                intfName1='r5-r4-eth', params1={'ip':'10.0.48.1/24'},
                intfName2='r4-r5-eth', params2={'ip':'10.0.48.2/24'})

        #################################################################################
        #### Block 6 ####
        router6 = self.addNode('r6', cls=LinuxRouter, ip='10.0.51.1/24')

        switch6 = self.addSwitch('s6')
        
        host6 = self.addHost('h6', ip='10.0.51.254/24', defaultRoute='via 10.0.51.1')
        
        self.addLink(host6, switch6)
        
        self.addLink(switch6, router6,
                intfName2='r6-s6-eth', params2={'ip':'10.0.51.1/24'})

        #################################################################################
        #### LINK Block 6 to Block 5 ####
        self.addLink(router6, router5,
                intfName1='r6-r5-eth', params1={'ip':'10.0.50.1/24'},
                intfName2='r5-r6-eth', params2={'ip':'10.0.50.2/24'})

        #################################################################################
        #### LINK Block 6 to Block 3 ####
        self.addLink(router6, router3,
                intfName1='r6-r3-eth', params1={'ip':'10.0.52.1/24'},
                intfName2='r3-r6-eth', params2={'ip':'10.0.52.2/24'})

        #################################################################################
        #### Block 7 ####
        router7 = self.addNode('r7', cls=LinuxRouter, ip='10.0.53.1/24')

        switch7 = self.addSwitch('s7')
        
        host7 = self.addHost('h7', ip='10.0.53.254/24', defaultRoute='via 10.0.53.1')
        
        self.addLink(host7, switch7)
        
        self.addLink(switch7, router7,
                intfName2='r7-s7-eth', params2={'ip':'10.0.53.1/24'})

        #################################################################################
        #### LINK Block 7 to Block 5 ####
        self.addLink(router7, router5,
                intfName1='r7-r5-eth', params1={'ip':'10.0.59.1/24'},
                intfName2='r5-r7-eth', params2={'ip':'10.0.59.2/24'})

        #################################################################################
        #### LINK Block 7 to Block 4 ####
        self.addLink(router7, router4,
                intfName1='r7-r4-eth', params1={'ip':'10.0.58.1/24'},
                intfName2='r4-r7-eth', params2={'ip':'10.0.58.2/24'})

        #################################################################################
        #### Block 8 ####
        router8 = self.addNode('r8', cls=LinuxRouter, ip='10.0.55.1/24')

        switch8 = self.addSwitch('s8')
        
        host8 = self.addHost('h8', ip='10.0.55.254/24', defaultRoute='via 10.0.55.1')
        
        self.addLink(host8, switch8)
        
        self.addLink(switch8, router8,
                intfName2='r8-s8-eth', params2={'ip':'10.0.55.1/24'})

        #################################################################################
        #### LINK Block 7 to Block 8 ####
        self.addLink(router7, router8,
                intfName1='r7-r8-eth', params1={'ip':'10.0.54.1/24'},
                intfName2='r8-r7-eth', params2={'ip':'10.0.54.2/24'})

        #################################################################################
        #### LINK Block 8 to Block 4 ####
        self.addLink(router8, router4,
                intfName1='r8-r4-eth', params1={'ip':'10.0.57.1/24'},
                intfName2='r4-r8-eth', params2={'ip':'10.0.57.2/24'})

        #################################################################################
        #### LINK Block 8 to Block 1 ####
        self.addLink(router8, router1,
                intfName1='r8-r1-eth', params1={'ip':'10.0.56.1/24'},
                intfName2='r1-r8-eth', params2={'ip':'10.0.56.2/24'})


def run():
    # Then create the network object from this topology
    net = Mininet(topo=NetworkTopo())

    net.addNAT(name='nat1', ip='10.0.42.1').configDefault()

    net.addLink(net['r1'], net['nat1'],
                intfName1='r1-nat-eth', params1={'ip':'10.0.41.1/24'},
                intfName2='nat-r1-eth', params2={'ip':'10.0.41.2/24'})

    #####################################################################################
    #####################################################################################

    # CONNECTING ROUTES
    # add {destination} via {other side intf ip} dev {this side intf name}
    # if I need to reach a destination (ip add) - what is the direct next step (via ... dev ...)
    
    ## CONNECTION NAT TO HOSTS
    # connecting host 1 to nat
    info(net['nat1'].cmd('ip route add 10.0.40.0/24 via 10.0.41.1 dev nat-r1-eth'))
    # connecting host 2 to nat
    info(net['nat1'].cmd('ip route add 10.0.43.0/24 via 10.0.41.1 dev nat-r1-eth'))
    # connecting host 3 to nat
    info(net['nat1'].cmd('ip route add 10.0.45.0/24 via 10.0.41.1 dev nat-r1-eth'))
    # connecting host 4 to nat
    info(net['nat1'].cmd('ip route add 10.0.47.0/24 via 10.0.41.1 dev nat-r1-eth'))
    # connecting host 5 to nat
    info(net['nat1'].cmd('ip route add 10.0.49.0/24 via 10.0.41.1 dev nat-r1-eth'))
    # connecting host 6 to nat
    info(net['nat1'].cmd('ip route add 10.0.51.0/24 via 10.0.41.1 dev nat-r1-eth'))
    # connecting host 7 to nat
    info(net['nat1'].cmd('ip route add 10.0.53.0/24 via 10.0.41.1 dev nat-r1-eth'))
    # connecting host 8 to nat
    info(net['nat1'].cmd('ip route add 10.0.55.0/24 via 10.0.41.1 dev nat-r1-eth'))

    ## CONNECTION NAT TO ROUTERS
    # connecting nat to r1
    info(net['r1'].cmd('ip route add 10.0.42.0/24 via 10.0.41.2 dev r1-nat-eth')) 
    # connecting nat to r3
    info(net['r3'].cmd('ip route add 10.0.42.0/24 via 10.0.44.2 dev r3-r1-eth'))  
    # connecting nat to r4
    info(net['r4'].cmd('ip route add 10.0.42.0/24 via 10.0.46.2 dev r4-r3-eth'))  
    # connecting nat to r5
    info(net['r5'].cmd('ip route add 10.0.42.0/24 via 10.0.48.2 dev r5-r4-eth'))  
    # connecting nat to r6
    info(net['r6'].cmd('ip route add 10.0.42.0/24 via 10.0.50.2 dev r6-r5-eth'))  
    # connecting nat to r7
    info(net['r7'].cmd('ip route add 10.0.42.0/24 via 10.0.54.2 dev r7-r8-eth'))  
    # connecting nat to r8
    info(net['r8'].cmd('ip route add 10.0.42.0/24 via 10.0.56.2 dev r8-r1-eth'))  

    #####################################################################################


    ## ROUTER 1 CONNECTIONS
    info(net['r1'].cmd('ip route add default via 10.0.41.2 dev r1-nat-eth'))
    # connection host3 to r1
    info(net['r1'].cmd('ip route add 10.0.45.0/24 via 10.0.44.1 dev r1-r3-eth'))
    # connection host4 to r1
    info(net['r1'].cmd('ip route add 10.0.47.0/24 via 10.0.44.1 dev r1-r3-eth'))
    # connection host5 to r1
    info(net['r1'].cmd('ip route add 10.0.49.0/24 via 10.0.44.1 dev r1-r3-eth'))
    # connection host6 to r1
    info(net['r1'].cmd('ip route add 10.0.51.0/24 via 10.0.44.1 dev r1-r3-eth'))
    # connection host7 to r1
    info(net['r1'].cmd('ip route add 10.0.53.0/24 via 10.0.44.1 dev r1-r3-eth'))
    # connection host8 to r1
    info(net['r1'].cmd('ip route add 10.0.55.0/24 via 10.0.44.1 dev r1-r3-eth'))


    ## ROUTER 2 CONNECTIONS ---> NONE


    ## ROUTER 3 CONNECTIONS
    info(net['r3'].cmd('ip route add default via 10.0.44.2 dev r3-r1-eth'))
    # connection host1 to r3
    info(net['r3'].cmd('ip route add 10.0.40.0/24 via 10.0.44.2 dev r3-r1-eth'))
    # connection host2 to r3
    info(net['r3'].cmd('ip route add 10.0.43.0/24 via 10.0.44.2 dev r3-r1-eth'))
    # connection host4 to r3
    info(net['r3'].cmd('ip route add 10.0.47.0/24 via 10.0.46.1 dev r3-r4-eth'))
    # connection host5 to r3
    info(net['r3'].cmd('ip route add 10.0.49.0/24 via 10.0.46.1 dev r3-r4-eth'))
    # connection host6 to r3
    info(net['r3'].cmd('ip route add 10.0.51.0/24 via 10.0.46.1 dev r3-r4-eth'))
    # connection host7 to r3
    info(net['r3'].cmd('ip route add 10.0.53.0/24 via 10.0.46.1 dev r3-r4-eth'))
    # connection host8 to r3
    info(net['r3'].cmd('ip route add 10.0.55.0/24 via 10.0.46.1 dev r3-r4-eth'))



    ## ROUTER 4 CONNECTIONS
    info(net['r4'].cmd('ip route add default via 10.0.46.2 dev r4-r3-eth'))
    # connection host1 to r4
    info(net['r4'].cmd('ip route add 10.0.40.0/24 via 10.0.46.2 dev r4-r3-eth'))
    # connection host2 to r4
    info(net['r4'].cmd('ip route add 10.0.43.0/24 via 10.0.46.2 dev r4-r3-eth'))
    # connection host3 to r4
    info(net['r4'].cmd('ip route add 10.0.45.0/24 via 10.0.46.2 dev r4-r3-eth'))
    # connection host5 to r4
    info(net['r4'].cmd('ip route add 10.0.49.0/24 via 10.0.48.1 dev r4-r5-eth'))
    # connection host6 to r4
    info(net['r4'].cmd('ip route add 10.0.51.0/24 via 10.0.48.1 dev r4-r5-eth'))
    # connection host7 to r4
    info(net['r4'].cmd('ip route add 10.0.53.0/24 via 10.0.48.1 dev r4-r5-eth'))
    # connection host8 to r4
    info(net['r4'].cmd('ip route add 10.0.55.0/24 via 10.0.57.1 dev r4-r8-eth'))


    ## ROUTER 5 CONNECTIONS
    info(net['r5'].cmd('ip route add default via 10.0.48.2 dev r5-r4-eth'))
    # connection host1 to r5
    info(net['r5'].cmd('ip route add 10.0.40.0/24 via 10.0.48.2 dev r5-r4-eth'))
    # connection host2 to r5
    info(net['r5'].cmd('ip route add 10.0.43.0/24 via 10.0.48.2 dev r5-r4-eth'))
    # connection host3 to r5
    info(net['r5'].cmd('ip route add 10.0.45.0/24 via 10.0.48.2 dev r5-r4-eth'))
    # connection host4 to r5
    info(net['r5'].cmd('ip route add 10.0.47.0/24 via 10.0.48.2 dev r5-r4-eth'))
    # connection host6 to r5
    info(net['r5'].cmd('ip route add 10.0.51.0/24 via 10.0.50.1 dev r5-r6-eth'))
    # connection host7 to r5
    info(net['r5'].cmd('ip route add 10.0.53.0/24 via 10.0.59.1 dev r5-r7-eth'))
    # connection host8 to r5
    info(net['r5'].cmd('ip route add 10.0.55.0/24 via 10.0.59.1 dev r5-r7-eth'))



    ## ROUTER 6 CONNECTIONS
    info(net['r6'].cmd('ip route add default via 10.0.50.2 dev r6-r5-eth'))
    # connection host1 to r6
    info(net['r6'].cmd('ip route add 10.0.40.0/24 via 10.0.50.2 dev r6-r5-eth'))
    # connection host2 to r6
    info(net['r6'].cmd('ip route add 10.0.43.0/24 via 10.0.50.2 dev r6-r5-eth'))
    # connection host3 to r6
    info(net['r6'].cmd('ip route add 10.0.45.0/24 via 10.0.50.2 dev r6-r5-eth'))
    # connection host4 to r6
    info(net['r6'].cmd('ip route add 10.0.47.0/24 via 10.0.50.2 dev r6-r5-eth'))
    # connection host5 to r6
    info(net['r6'].cmd('ip route add 10.0.49.0/24 via 10.0.50.2 dev r6-r5-eth'))
    # connection host7 to r6
    info(net['r6'].cmd('ip route add 10.0.53.0/24 via 10.0.50.2 dev r6-r5-eth'))
    # connection host8 to r6
    info(net['r6'].cmd('ip route add 10.0.55.0/24 via 10.0.50.2 dev r6-r5-eth'))



    ## ROUTER 7 CONNECTIONS
    info(net['r7'].cmd('ip route add default via 10.0.54.2 dev r7-r8-eth'))
    # connection host1 to r7
    info(net['r7'].cmd('ip route add 10.0.40.0/24 via 10.0.54.2 dev r7-r8-eth'))
    # connection host2 to r7
    info(net['r7'].cmd('ip route add 10.0.43.0/24 via 10.0.54.2 dev r7-r8-eth'))
    # connection host3 to r7
    info(net['r7'].cmd('ip route add 10.0.45.0/24 via 10.0.54.2 dev r7-r8-eth'))
    # connection host4 to r7
    info(net['r7'].cmd('ip route add 10.0.47.0/24 via 10.0.58.2 dev r7-r4-eth'))
    # connection host5 to r7
    info(net['r7'].cmd('ip route add 10.0.49.0/24 via 10.0.59.2 dev r7-r5-eth'))
    # connection host6 to r7
    info(net['r7'].cmd('ip route add 10.0.51.0/24 via 10.0.54.2 dev r7-r8-eth'))
    # connection host8 to r7
    info(net['r7'].cmd('ip route add 10.0.55.0/24 via 10.0.54.2 dev r7-r8-eth'))



    ## ROUTER 8 CONNECTIONS
    info(net['r8'].cmd('ip route add default via 10.0.56.2 dev r8-r1-eth'))
    # connection host1 to r8
    info(net['r8'].cmd('ip route add 10.0.40.0/24 via 10.0.56.2 dev r8-r1-eth'))
    # connection host2 to r8
    info(net['r8'].cmd('ip route add 10.0.43.0/24 via 10.0.56.2 dev r8-r1-eth'))
    # connection host3 to r8
    info(net['r8'].cmd('ip route add 10.0.45.0/24 via 10.0.56.2 dev r8-r1-eth'))
    # connection host4 to r8
    info(net['r8'].cmd('ip route add 10.0.47.0/24 via 10.0.56.2 dev r8-r1-eth'))
    # connection host5 to r8
    info(net['r8'].cmd('ip route add 10.0.49.0/24 via 10.0.56.2 dev r8-r1-eth'))
    # connection host6 to r8
    info(net['r8'].cmd('ip route add 10.0.51.0/24 via 10.0.56.2 dev r8-r1-eth'))
    # connection host7 to r8
    info(net['r8'].cmd('ip route add 10.0.53.0/24 via 10.0.54.1 dev r8-r7-eth'))




    ## DEFAULT HOST ROUTES
    info(net['h1'].cmd('ip route add default via 10.0.40.1'))
    info(net['h2'].cmd('ip route add default via 10.0.43.1'))
    info(net['h3'].cmd('ip route add default via 10.0.45.1'))
    info(net['h4'].cmd('ip route add default via 10.0.47.1'))
    info(net['h5'].cmd('ip route add default via 10.0.49.1'))
    info(net['h6'].cmd('ip route add default via 10.0.51.1'))
    info(net['h7'].cmd('ip route add default via 10.0.53.1'))
    info(net['h8'].cmd('ip route add default via 10.0.55.1'))


    #####################################################################################
    #####################################################################################


    ## DEFAULT NAT ROUTE
    info(net['nat1'].cmd('ip route add default via 192.168.100.2 dev vxlan0'))

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