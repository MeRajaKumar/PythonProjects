import heapq
import matplotlib.pyplot as plt
import networkx as nx
import tkinter as tk
from tkinter import messagebox, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Dijkstra's algorithm to calculate the shortest path
def dijkstra(graph, start):
    queue = [(0, start)]
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    previous_nodes = {node: None for node in graph}

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))

    return distances, previous_nodes

# Function to calculate the shortest path between two cities
def shortest_path(graph, start, end):
    distances, previous_nodes = dijkstra(graph, start)
    path = []
    step = end

    while step:
        path.append(step)
        step = previous_nodes[step]

    path.reverse()
    return path, distances[end]

# Function to handle the button click for the shortest path calculation
def calculate_shortest_path():
    if start_city.get() == "Select Start City" or end_city.get() == "Select End City":
        messagebox.showerror("Invalid Input", "Please select both start and end cities.")
        return

    start = start_city.get()
    end = end_city.get()

    path, cost = shortest_path(graph, start, end)
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, f"Shortest path from {start} to {end}:\n")
    result_text.insert(tk.END, " → ".join(path) + "\n")
    result_text.insert(tk.END, f"Total cost: {cost}")
    result_text.config(state=tk.DISABLED)

    visualize_path(start, end, path)

def visualize_path(start, end, path):
    for widget in graph_frame.winfo_children():
        widget.destroy()

    G = nx.Graph()
    for node in graph:
        for neighbor, weight in graph[node].items():
            G.add_edge(node, neighbor, weight=weight)

    fig = plt.figure(figsize=(8, 6), dpi=100)
    ax = fig.add_subplot(111)
    pos = nx.spring_layout(G, k=0.5, iterations=50)

    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=800, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=10, ax=ax)
    nx.draw_networkx_edges(G, pos, edge_color='gray', width=1, ax=ax)

    path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
    nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='orange', node_size=800, ax=ax)
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3, ax=ax)

    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, ax=ax)
    ax.set_title(f"GPS Navigation Tracker: {start} to {end}", fontsize=12)
    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

def clear_selections():
    start_city.set("Select Start City")
    end_city.set("Select End City")
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    result_text.config(state=tk.DISABLED)
    for widget in graph_frame.winfo_children():
        widget.destroy()

# Example graph with Indian cities
graph = {
    'Delhi': {'Jaipur': 280, 'Lucknow': 500, 'Agra': 230, 'Chandigarh': 250},
    'Jaipur': {'Delhi': 280, 'Ahmedabad': 660, 'Indore': 620},
    'Lucknow': {'Delhi': 500, 'Varanasi': 320, 'Patna': 520},
    'Agra': {'Delhi': 230, 'Kanpur': 300, 'Bhopal': 600},
    'Chandigarh': {'Delhi': 250, 'Amritsar': 230, 'Shimla': 120},
    'Ahmedabad': {'Jaipur': 660, 'Mumbai': 530},
    'Indore': {'Jaipur': 620, 'Bhopal': 190},
    'Mumbai': {'Ahmedabad': 530, 'Pune': 150, 'Nagpur': 840},
    'Bhopal': {'Agra': 600, 'Indore': 190, 'Nagpur': 360},
    'Patna': {'Lucknow': 520, 'Kolkata': 600},
    'Varanasi': {'Lucknow': 320, 'Patna': 240},
    'Kanpur': {'Agra': 300, 'Lucknow': 90},
    'Pune': {'Mumbai': 150, 'Hyderabad': 560},
    'Nagpur': {'Mumbai': 840, 'Bhopal': 360, 'Hyderabad': 500},
    'Hyderabad': {'Nagpur': 500, 'Pune': 560, 'Bangalore': 570},
    'Bangalore': {'Hyderabad': 570, 'Chennai': 350},
    'Chennai': {'Bangalore': 350, 'Kolkata': 1360},
    'Kolkata': {'Patna': 600, 'Chennai': 1360},
    'Amritsar': {'Chandigarh': 230},
    'Shimla': {'Chandigarh': 120}
}

# GUI setup
root = tk.Tk()
root.title("GPS Navigation Tracker")
root.geometry("1000x800")
root.configure(bg='#e0f7fa')

style = ttk.Style()
style.theme_use('clam')
style.configure('TFrame', background='#e0f7fa')
style.configure('TLabel', background='#e0f7fa', font=('Arial', 11))
style.configure('TButton', font=('Arial', 10, 'bold'), padding=8, background='#00b4d8', foreground='white')
style.map('TButton', background=[('active', '#0077b6')])
style.configure('TCombobox', font=('Arial', 10), padding=6)

result_text_bg = '#f1f1f1'

main_frame = ttk.Frame(root, style='TFrame')
main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

control_frame = ttk.Frame(main_frame, style='TFrame')
control_frame.pack(fill=tk.X, pady=10)

cities = sorted(graph.keys())
start_city = tk.StringVar(value="Select Start City")
end_city = tk.StringVar(value="Select End City")

start_label = ttk.Label(control_frame, text="Departure City:")
start_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
start_menu = ttk.Combobox(control_frame, textvariable=start_city, values=cities, state="readonly")
start_menu.grid(row=0, column=1, padx=5, pady=5)

end_label = ttk.Label(control_frame, text="Destination City:")
end_label.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
end_menu = ttk.Combobox(control_frame, textvariable=end_city, values=cities, state="readonly")
end_menu.grid(row=0, column=3, padx=5, pady=5)

button_frame = ttk.Frame(control_frame)
button_frame.grid(row=0, column=4, padx=10)
calculate_btn = ttk.Button(button_frame, text="Find Route", command=calculate_shortest_path)
calculate_btn.pack(side=tk.LEFT, padx=5)
clear_btn = ttk.Button(button_frame, text="Clear", command=clear_selections)
clear_btn.pack(side=tk.LEFT, padx=5)

result_frame = ttk.Frame(main_frame, style='TFrame')
result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
result_label = ttk.Label(result_frame, text="Route Information:", font=('Arial', 11, 'bold'))
result_label.pack(anchor=tk.W)
result_text = tk.Text(result_frame, height=4, width=80, wrap=tk.WORD, font=('Arial', 10), bg=result_text_bg)
result_text.pack(fill=tk.BOTH, expand=True, pady=5)
result_text.config(state=tk.DISABLED)

graph_frame = ttk.Frame(main_frame, style='TFrame')
graph_frame.pack(fill=tk.BOTH, expand=True)
graph_label = ttk.Label(graph_frame, text="Route Visualization:", font=('Arial', 11, 'bold'))
graph_label.pack(anchor=tk.W)

fig = plt.figure(figsize=(8, 6), dpi=100)
ax = fig.add_subplot(111)
ax.text(0.5, 0.5, "Select cities and click 'Find Route' to visualize the path", ha='center', va='center', fontsize=12, color='gray')
ax.axis('off')
plt.tight_layout()

canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

root.mainloop()
