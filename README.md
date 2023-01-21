# MITM - SDN

In this project we demostrate a mechanism to detect a Man-In-The-Middle attack in a Software Defined Network. For the purpose of this project, we used:
- Mininet, as the network simulator
- POX, as the SDN controller
- Python, as our main programming language here, to generate our topology, traffic and detection system

To start the topology Mininet is required. Please refer to the *launch.txt* file for further instructions how to start the topology. The file *run_ettercap.sh* is used to start the "ettercap" sniffing tool - launch it on one of the MITM hosts.

<p align="center">
  <img src="https://github.com/msobczuk/MITM---SDN/blob/main/topology.PNG">
</p>
