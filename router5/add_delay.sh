#!/bin/bash

tc qdisc del dev eth1 root
tc qdisc del dev eth2 root


# router5 -> server
tc qdisc add dev eth1 root netem delay 15
ms

# router5 -> router3
tc qdisc add dev eth2 root netem delay 200ms

