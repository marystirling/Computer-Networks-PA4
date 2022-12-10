#!/bin/bash

tc qdisc del dev eth0 root
tc qdisc del dev eth1 root
tc qdisc del dev eth2 root

# client -> router1
tc qdisc add dev eth0 root netem delay 10ms

# client -> router2
tc qdisc add dev eth1 root netem delay 5ms

# client -> router3 
tc qdisc add dev eth2 root netem delay 50ms

