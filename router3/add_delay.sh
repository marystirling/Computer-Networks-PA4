#!/bin/bash

tc qdisc del dev eth1 root
tc qdisc del dev eth2 root
tc qdisc del dev eth3 root

# router3 -> client
# DO NOT CHANGE - router1 will never map back to client
tc qdisc add dev eth1 root netem delay 0ms

# router3 -> router2
tc qdisc add dev eth2 root netem delay 30ms

# router3 -> router5
tc qdisc add dev eth3 root netem delay 80ms

