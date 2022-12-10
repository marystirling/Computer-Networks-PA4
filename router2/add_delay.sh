#!/bin/bash

tc qdisc del dev eth0 root
tc qdisc del dev eth1 root
tc qdisc del dev eth2 root
tc qdisc del dev eth3 root
tc qdisc del dev eth4 root

# router2 -> client
# DO NOT CHANGE - router1 will never map back to client
tc qdisc add dev eth1 root netem delay 0ms

# router2 -> router1
tc qdisc add dev eth2 root netem delay 45ms

# router2 -> router3
tc qdisc add dev eth3 root netem delay 75ms

# router2 -> server
tc qdisc add dev eth4 root netem delay 35ms

