#!/bin/bash

tc qdisc del dev eth1 root
tc qdisc del dev eth2 root



# router4 -> router1
tc qdisc add dev eth1 root netem delay 80ms

# router4 -> server
tc qdisc add dev eth2 root netem delay 5ms

