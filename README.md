# Computer-Networks-PA4

For this assignement, we are measuring the computing the shortest path using Dikstra's algorithm for two computation methods: (1) hop count and (2) smallest delay. 

* For the worker nodes, the following containers are placed:

  * CompNW-worker1: msb_router1 

  * CompNW-worker2: msb_router2  
  
  * CompNW-worker3: msb_router3  
  
  * CompNW-worker4: msb_router4 
  
  * CompNW-worker5: msb_router5 
  
  * CompNW-worker6: msb_client 
  
  * CompNW-worker7: msb_server 
  
We also have the master node.

We now want to ssh into these nodes. Open 8 terminal windows and issue one of the following commands on each one.

```
# master node
ssh -i ~/.ssh/cs4283_5283.pem cc@129.114.25.220
```
```
# worker 1 node
ssh -i ~/.ssh/cs4283_5283.pem cc@129.114.26.161
```
```
# worker 2 node
ssh -i ~/.ssh/cs4283_5283.pem cc@129.114.26.157
```
```
# worker 3 node
ssh -i ~/.ssh/cs4283_5283.pem cc@129.114.27.51
```
```
# worker 4 node
ssh -i ~/.ssh/cs4283_5283.pem cc@129.114.27.88
```
```
# worker 5 node
ssh -i ~/.ssh/cs4283_5283.pem cc@129.114.27.146
```
```
# worker 6 node
ssh -i ~/.ssh/cs4283_5283.pem cc@129.114.27.148
```
```
# worker 7 node
ssh -i ~/.ssh/cs4283_5283.pem cc@129.114.27.158
```

In the master node, go to the marystirling directory, collect container info, and  run msb_controller.py. 
```
cd marystirling
```
```
sh set_containers.py
```
```
python3 msb_controller.py
```

In this msb_controller.py, we can switch the computation methods for shortest path by changing the value of the variable shortest_method_approach. The value should be 1 for smallest hop count, and 2 for smallest delay.

Now, go back to the 7 worker node terminals and run the container for each respective one:


```
# worker 1 node
docker exec -it msb_router1.1.k3ekxvwq4gemlzghi0aiint76 /bin/bash
```
```
# worker 2 node
docker exec -it msb_router2.1.ouexlo2orlix6hlxmm30g57gf /bin/bash
```
```
# worker 3 node
docker exec -it msb_router3.1.nwxbpjwn8dnno0zoagx1xayr9 /bin/bash
```
```
# worker 4 node
docker exec -it msb_router4.1.88tnc432hlz4pm72rgfrd8wo9 /bin/bash
```
```
# worker 5 node
docker exec -it msb_router5.1.aj9mg58pdrq4kzebifwxga40z /bin/bash
```
```
# worker 6 node
docker exec -it msb_client.1.2hz1nsuxjktt2r0shb5lohxzk /bin/bash
```
```
# worker 7 node
docker exec -it msb_server.1.b1s7bn1prok2huwbkjgaljgew /bin/bash
```

Except for the server since its the targest destination, we can change the delays of the overlays by changing the values in add_delay.sh in each of these containers. We then run this by:
```
sh add_delays.sh
```

For the containers with router logic, run:
```
python3 test_router.py
```

For the container with the client, run:
```
python3 test_client.py
```

For the container with the server, run:
```
python3 test_server.py
```
