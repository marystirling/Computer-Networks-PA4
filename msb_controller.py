import json
import zmq
import docker
import sys
import subprocess
import os
import random
from subprocess import Popen, PIPE
import pty
import time

# 1: smallest hop count
# 2: shortest end to end delay
shortest_path_approach = 2

networks_list = ["overlay_nw1", "overlay_nw2", "overlay_nw3", "overlay_nw4", "ovrlay_nw5", "overlay_nw6", "overlay_nw7", "overlay_nw8", "overlay_nw9", "overlay_nw10"]
services_list = ["msb_client", "msb_server", "msb_router1", "msb_router2", "msb_router3", "msb_router4", "msb_router5"]
workers_list = ["compnw-worker1", "compnw-worker2", "compnw-worker3", "compnw-worker4", "compnw-worker5", "compnw-worker6", "compnw-worker7", "compnw-worker8", "compnw-worker9", "compnw-worker10"]
containers_list = {
    "msb_router1.1.k3ekxvwq4gemlzghi0aiint76": "caa14a2659b6",
    "msb_router2.1.ouexlo2orlix6hlxmm30g57gf": "3e37d6559657",
    "msb_router3.1.nwxbpjwn8dnno0zoagx1xayr9": "35d3a5fc6341",
    "msb_router4.1.88tnc432hlz4pm72rgfrd8wo9": "cfa662ad7a4a",
    "msb_router5.1.aj9mg58pdrq4kzebifwxga40z": "86ab9c4764c9",
    "msb_client.1.2hz1nsuxjktt2r0shb5lohxzk": "3859e5adbd9c",
    "msb_server.1.b1s7bn1prok2huwbkjgaljgew": "7fa8f23c80e0"
}



ssh_list = ["cc@129.114.25.161", "cc@129.114.26.157", "cc@129.114.27.51", "cc@129.114.27.88","cc@129.114.27.146","cc@129.114.27.148","cc@129.114.27.158"]


weights = []
# client_weights = r1, r2, r3
client_weights = [10, 5, 50]
weights.append(client_weights)
# r1_weights = client, r1, r4
r1_weights = [0, 30, 100]
weights.append(r1_weights)
# r2_weights = client, r1, r3, server
r2_weights = [0, 45, 75, 35]
weights.append(r2_weights)
# r3_weights = client, r2, r5
r3_weights = [0, 30, 80]
weights.append(r3_weights)
# r4_weights = r1, server
r4_weights = [80, 5]
weights.append(r4_weights)
# r5_weights = r1, server
r5_weights = [15, 200]
weights.append(r5_weights)
# server_weights = r2, r4, r5 -> no weights since at server
server_weights = [0, 0, 0]
weights.append(server_weights)



def get_information():

    f = open("container_info.json")
    all_info = json.load(f)
    f.close()

    return all_info

def get_edges(services):
    edges = []
    i = 0
    for s1 in services:
        j = 0
        for s2 in services:
            name1 = s1["Name"]
            name2 = s2["Name"]
            port1 = s1["Port"]
            port2 = s2["Port"]
            if name1 == name2:
                pass
            
            else:
                for container_ip1 in s1["ContainerIPs"]:
                    for container_ip2 in s2["ContainerIPs"]:
                        if container_ip1["NetworkID"] != "e138ukhtp4xtkcq8u8l9v7t9v" and container_ip2["NetworkID"] != "e138ukhtp4xtkcq8u8l9v7t9v":
                            if container_ip1["NetworkID"] == container_ip2["NetworkID"]:
                                ip1 = container_ip1["Addr"]
                                ip2 = container_ip2["Addr"]
                                if shortest_path_approach == 1:
                                    weight_value = 1
                                elif shortest_path_approach == 2:
                                    weight_value = weights[i][j]
                                dict_item = {name1: (ip1, port1), name2: (ip2, port2), "weight": weight_value}
                                edges.append(dict_item)
                                j += 1
        i += 1

    return edges



def get_outgoing_edges(edges, current_min_node):
    outgoing_edges = []
    for edge in edges:
        key = list(edge)
        if key[0] == current_min_node:
            outgoing_edges.append(edge)
    return outgoing_edges


def dikstra(edges, start_node):
    # implemented from https://www.udacity.com/blog/2021/10/implementing-dijkstras-algorithm-in-python.html
    
    unvisited_nodes = services_list
    shortest_path = {}
    previous_nodes = {}
    max_value = sys.maxsize # this initializes the "infinity" value of the unvisited node
    for node in unvisited_nodes:
        shortest_path[node] = max_value
    shortest_path[start_node] = 0

    while unvisited_nodes:
        current_min_node = None
        for node in unvisited_nodes:
            if current_min_node == None:
                current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node
        neighbors = get_outgoing_edges(edges, current_min_node)
        for neighbor in neighbors:
            tentative_value = shortest_path[current_min_node] + neighbor["weight"]
            if tentative_value < shortest_path[list(neighbor)[1]]:
                shortest_path[list(neighbor)[1]] = tentative_value
                previous_nodes[list(neighbor)[1]] = current_min_node
        unvisited_nodes.remove(current_min_node)
    return previous_nodes, shortest_path
     

def get_dikstra_result(previous_nodes, shortest_path, start_node, target_node):
    path = []
    node = target_node

    while node != start_node:
        path.append(node)
        node = previous_nodes[node]

    path.append(start_node)
    if shortest_path_approach == 1:
        print(f"best path with a value of {client_weights[1] + r2_weights[3]}")
        print(" -> ".join(reversed(path)))
      
    elif shortest_path_approach == 2:
        print(f"best path with a value of {shortest_path[target_node]}")

    return list(reversed(path))


def create_routing_table(edges, route):
    routing_table = {}
    iter = len(route) - 1
    i = 0
    connecting_ip = None
    while i < iter:
        curr_node = route[i]
        next_node = route[i + 1]
        for edge in edges:
            this_edge = list(edge)
            
            if this_edge[0] == curr_node and this_edge[1] == next_node:
                routing_table[curr_node] = [connecting_ip, this_edge[1], edge[next_node]]
                connecting_ip = edge[next_node]
        i += 1
    print(routing_table)
    json_format = json.dumps(routing_table, indent = 2, separators = (", ", ": "))
    file = open("./routing_table.json", "w")
    json.dump (routing_table, file, indent = 2, separators = (", ", ": "))
    file.close
        
# sends routing table to all containers on different worker nodes
def send_routing_table():
    j = 0
    for container in containers_list:
        ssh_path = ssh_list[j]
        cmd = "docker cp /home/cc/marystirling/routing_table.json " + containers_list[container] + ":/NWClass_msb"
        scp_cmd = "scp -i ~/.ssh/cs4283_5283.pem routing_table.json " + ssh_path +":/home/cc/marystirling"
        os.system(scp_cmd)
        cp_cmd = "docker cp /home/cc/marystirling/routing_table.json " + containers_list[container] + ":/NWClass_msb"
        process = subprocess.Popen(["ssh", "-T", "-i", "~/.ssh/cs4283_5283.pem", ssh_path, cp_cmd])
        process.wait()
        j += 1





if __name__ == '__main__':
    all_info = get_information()

    edges = get_edges(all_info)
    start_node = "msb_client"
    target_node = "msb_server"

    previous_nodes, shortest_path = dikstra(edges, start_node)
    route = get_dikstra_result(previous_nodes, shortest_path, start_node, target_node)
    
    create_routing_table(edges, route)
    print(f"Routing table created with route {route}")

    send_routing_table()

