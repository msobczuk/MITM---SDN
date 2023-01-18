"""
author: Sean Choi
email: yo2seol@stanford.edu
"""

import os
from mininet.net import Mininet
from mininet.node import Node, Controller, RemoteController
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.topo import Topo
from mininet.util import quietRun
from mininet.moduledeps import pathCheck

CURR_PATH = os.getcwd()
DECODED = CURR_PATH +  "/decoded.log"
LOG_FILE= CURR_PATH + "/logfile.log"

class LinuxRouter( Node ):
    "A Node with IP forwarding enabled."

    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd("sysctl -w net.ipv4.ip_forward=1")
        self.cmd("sysctl -p /etc/sysctl.conf")

    def terminate( self ):
        self.cmd("sysctl -w net.ipv4.ip_forward=0")
        self.cmd("sysctl -p /etc/sysctl.conf")
        super( LinuxRouter, self ).terminate()

class AttackTopo( Topo ):
    "Our Topology"

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        pc1 = self.addHost( 'pc1', ip='192.168.1.1/24',
            mac='00:00:00:00:00:01')
        pc2 = self.addHost( 'pc2', ip='192.168.1.2/24',
            mac='00:00:00:00:00:02')
        #attacker_host = self.addHost( 'h3', ip='192.168.0.5/24',
        #    mac='00:00:00:00:00:03')
        mitm_pc1 = self.addNode( 'mitm_pc1', cls=LinuxRouter, ip='192.168.1.3/24', mac='00:00:00:00:00:03')
	mitm_pc2 = self.addNode( 'mitm_pc2', cls=LinuxRouter, ip='192.168.1.4/24', mac='00:00:00:00:00:04')
        s1 = self.addSwitch( 's1' )
	s2 = self.addSwitch( 's2' )
        
        # Add links from the hosts to this single switch
        self.addLink( pc1, s1 )
        self.addLink( pc2, s2 )
        self.addLink( mitm_pc1, s1 )
	self.addLink( mitm_pc2, s2)
	self.addLink( s1, s2 )

#uncomment then typpe sudo mn --custom sshmitm.py --topo attacktopo --controller=remote
topos = { 'attacktopo': ( lambda: AttackTopo() ) }

def start_sshd( host ):
    "Start sshd on host"
    stop_sshd()
    info( '*** Starting sshd in %s\n' % host.name )
    name, intf, ip = host.name, host.defaultIntf(), host.IP()
    banner = '/tmp/%s.banner' % name
    host.cmd( 'echo "Welcome to %s at %s" >  %s' % ( name, ip, banner ) )
    host.cmd( '/usr/sbin/sshd -o Banner=%s -o UseDNS=no' % banner)
    info( '***', host.name, 'is running sshd on', intf, 'at', ip, '\n' )

def stop_sshd():
    "Stop *all* sshd processes with a custom banner"
    info( '*** Shutting down stale sshd/Banner processes ',
          quietRun( "pkill -9 -f Banner" ), '\n' )

def create_attack_log(host):
    host.cmd("chmod 666 %s>>!#:2" % DECODED)
    host.cmd("chmod 666 %s>>!#:2" % LOG_FILE)

def delete_attack_log(host):
    host.cmd("rm %s" % DECODED)
    host.cmd("rm %s" % LOG_FILE)

def main():
    topo = AttackTopo()
    #info( '*** Creating network\n' )
    net = Mininet(topo=topo)
    net.start()

    # Print the elements of the network
    for item in net.items():
        print item

    print "Encoded log file at %s" % LOG_FILE 
    print "Decoded log file at %s" % DECODED 
    pc1, pc2, mitm_pc1, mitm_pc2, s1, s2 = net.get('pc1', 'pc2', 'mitm_pc1', 'mitm_pc2', 's1', 's2')
    # Start a ssh server on host 2
    start_sshd(pc2)
    create_attack_log(mitm_pc2)
    CLI(net)
    stop_sshd()
    delete_attack_log(mitm_pc2)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    main()
