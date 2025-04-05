import tkinter as tk
from tkinter import messagebox
import heapq
import math

class NetworkSimulator:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master, width=600, height=400, bg="white")
        self.canvas.pack()

        self.nodes = []
        self.switches = []
        self.connections = {}
        self.graph = {}

        self.node1_entry = tk.Entry(master)
        self.node1_entry.pack()
        self.node2_entry = tk.Entry(master)
        self.node2_entry.pack()

        self.canvas.bind("<Button-1>", self.create_node)
        self.create_switch_button = tk.Button(master, text="Create Switch", command=self.create_switch)
        self.create_switch_button.pack()
        self.connect_button = tk.Button(master, text="Connect", command=self.connect_components)
        self.connect_button.pack()
        self.shortest_path_button = tk.Button(master, text="Find Shortest Path", command=self.find_shortest_path)
        self.shortest_path_button.pack()

        self.node_counter = 0
        self.switch_counter = 0
        self.conversion_factor = 10

    def create_node(self, event):
        self.node_counter += 1
        node = self.canvas.create_oval(event.x - 10, event.y - 10, event.x + 10, event.y + 10, fill="blue")
        self.nodes.append(node)
        self.graph[node] = {}
        self.canvas.create_text(event.x, event.y, text=str(self.node_counter))

    def create_switch(self):
        self.switch_counter += 1
        switch = self.canvas.create_rectangle(100 + (self.switch_counter - 1) * 150, 150,
                                              150 + (self.switch_counter - 1) * 150, 200, fill="green")
        self.switches.append(switch)
        self.graph[switch] = {}
        self.canvas.create_text(125 + (self.switch_counter - 1) * 150, 175, text="Switch " + str(self.switch_counter))

    def connect_components(self):
        for i in range(len(self.switches) - 1):
            switch1 = self.switches[i]
            switch2 = self.switches[i + 1]
            self.add_edge(switch1, switch2, 1)

        for node in self.nodes:
            nearest_switch = min(self.switches, key=lambda switch: self.distance(node, switch), default=None)
            if nearest_switch:
                self.add_edge(node, nearest_switch, self.distance(node, nearest_switch))

    def add_edge(self, node1, node2, weight):
        line = self.canvas.create_line(self.canvas.coords(node1)[0] + 10, self.canvas.coords(node1)[1] + 10,
                                       self.canvas.coords(node2)[0] + 10, self.canvas.coords(node2)[1] + 10,
                                       fill="black")
        self.connections[(node1, node2)] = line
        self.graph[node1][node2] = weight
        self.graph[node2][node1] = weight

    def distance(self, node1, node2):
        x1, y1 = self.canvas.coords(node1)[:2]
        x2, y2 = self.canvas.coords(node2)[:2]
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def find_shortest_path(self):
        try:
            node1_number = int(self.node1_entry.get())
            node2_number = int(self.node2_entry.get())
            start = self.nodes[node1_number - 1]
            end = self.nodes[node2_number - 1]
            self.show_shortest_path(start, end)
        except (ValueError, IndexError):
            messagebox.showwarning("Warning", "Invalid node numbers.")

    def show_shortest_path(self, start, end):
        distances = {node: float('inf') for node in self.graph}
        distances[start] = 0
        previous = {}
        priority_queue = [(0, start)]

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)
            if current_node == end:
                path = []
                while current_node:
                    path.append(current_node)
                    current_node = previous.get(current_node)
                path.reverse()
                for i in range(len(path) - 1):
                    self.highlight_connection(path[i], path[i + 1])
                return

            if current_distance > distances[current_node]:
                continue

            for neighbor, weight in self.graph[current_node].items():
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_node
                    heapq.heappush(priority_queue, (distance, neighbor))

    def highlight_connection(self, node1, node2):
        connection = self.connections.get((node1, node2)) or self.connections.get((node2, node1))
        if connection:
            self.canvas.itemconfig(connection, fill="red", dash=(4, 2))


def main():
    root = tk.Tk()
    root.title("Network Simulator")
    app = NetworkSimulator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
