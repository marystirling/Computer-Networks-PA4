#!/bin/bash

tc qdisc del dev eth0 root
tc qdisc del dev eth1 root
tc qdisc del dev eth2 root

# router1 -> client
# DO NOT CHANGE - router1 will never map back to client
tc qdisc add dev eth0 root netem delay 0ms

# router1 -> router2
tc qdisc add dev eth1 root netem delay 30ms

# router1 -> router4
tc qdisc add dev eth2 root netem delay 100ms

