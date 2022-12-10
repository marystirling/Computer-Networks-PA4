#!/bin/bash


docker service rm msb_client
docker service rm msb_server
docker service rm msb_router1
docker service rm msb_router2
docker service rm msb_router3
docker service rm msb_router4
docker service rm msb_router5

# create client
docker service create --name msb_client --cap-add NET_ADMIN --constraint node.hostname==compnw-worker6 --network overlay_nw1 192.168.2.61:5000/msb_image
docker service update --network-add overlay_nw2 msb_client
docker service update --network-add overlay_nw3 msb_client

# create router1
docker service create --name msb_router1 --cap-add NET_ADMIN --constraint node.hostname==compnw-worker1 --network overlay_nw1 --publish published=31010,target=4444 192.168.2.61:5000/msb_image
docker service update --network-add overlay_nw4 msb_router1
docker service update --network-add overlay_nw6 msb_router1

# create router2
docker service create --name msb_router2 --cap-add NET_ADMIN --constraint node.hostname==compnw-worker2 --network overlay_nw2 --publish published=31011,target=4444 192.168.2.61:5000/msb_image
docker service update --network-add overlay_nw4 msb_router2
docker service update --network-add overlay_nw5 msb_router2
docker service update --network-add overlay_nw7 msb_router2

# create router3
docker service create --name msb_router3 --cap-add NET_ADMIN --constraint node.hostname==compnw-worker3 --network overlay_nw3 --publish published=31012,target=4444 192.168.2.61:5000/msb_image
docker service update --network-add overlay_nw5 msb_router3
docker service update --network-add overlay_nw8 msb_router3

# create router4
docker service create --name msb_router4 --cap-add NET_ADMIN --constraint node.hostname==compnw-worker4 --network overlay_nw6 --publish published=31013,target=4444 192.168.2.61:5000/msb_image
docker service update --network-add overlay_nw9 msb_router4

# create router5
docker service create --name msb_router5 --cap-add NET_ADMIN --constraint node.hostname==compnw-worker5 --network overlay_nw8 --publish published=31014,target=4444 192.168.2.61:5000/msb_image
docker service update --network-add overlay_nw10 msb_router5

# create server
docker service create --name msb_server --cap-add NET_ADMIN --constraint node.hostname==compnw-worker7 --network overlay_nw7 --publish published=30005,target=5555,mode=host 192.168.2.61:5000/msb_image
docker service update --network-add overlay_nw9 msb_server
docker service update --network-add overlay_nw10 msb_server




