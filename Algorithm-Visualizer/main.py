import matplotlib.pyplot as plt
import numpy as np
import heapq
import time
import tkinter as tk
from tkinter import ttk

# 冒泡排序可视化
def bubble_sort_visualize(arr):
    arr = arr.copy()
    n = len(arr)
    plt.ion()
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(range(n), arr, color='blue')
    ax.set_title("Bubble Sort Visualization", fontsize=14)

    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                for bar, height in zip(bars, arr):
                    bar.set_height(height)
                fig.canvas.draw()
                fig.canvas.flush_events()
                time.sleep(0.1)
    plt.ioff()
    plt.show()
    return arr

# Dijkstra 最短路径可视化
class DijkstraVisual:
    def __init__(self):
        plt.ion()
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.graph = {}
        self.nodes = {}
        self.node_color = {}
        self.step_text = ""

    def init_graph(self):
        self.graph = {
            'A': [('B', 2), ('C', 5)],
            'B': [('A', 2), ('D', 1), ('C', 3)],
            'C': [('A', 5), ('B', 3), ('D', 2)],
            'D': [('B', 1), ('C', 2)]
        }
        self.nodes = {
            'A': (0, 3), 'B': (2, 3),
            'C': (0, 0), 'D': (2, 0)
        }
        for n in self.nodes:
            self.node_color[n] = "lightgray"
        self.draw_graph()

    def draw_graph(self):
        self.ax.clear()
        for u in self.graph:
            x1, y1 = self.nodes[u]
            for v, w in self.graph[u]:
                x2, y2 = self.nodes[v]
                self.ax.plot([x1, x2], [y1, y2], 'gray', linestyle='-')
                self.ax.text((x1 + x2) / 2, (y1 + y2) / 2, str(w), fontsize=10)
        for node, (x, y) in self.nodes.items():
            self.ax.scatter(x, y, s=800, c=self.node_color[node])
            self.ax.text(x, y, node, ha='center', va='center', fontsize=12)
        self.ax.set_title(f"Dijkstra 最短路径 | {self.step_text}", fontsize=12)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def dijkstra_run(self, start):
        INF = float('inf')
        dist = {n: INF for n in self.graph}
        dist[start] = 0
        heap = []
        heapq.heappush(heap, (0, start))
        visited = set()

        while heap:
            current_dist, u = heapq.heappop(heap)
            if u in visited:
                continue
            visited.add(u)
            self.node_color[u] = "orange"
            self.step_text = f"访问节点 {u}，当前最短距离: {current_dist}"
            self.draw_graph()
            time.sleep(0.8)
            for v, w in self.graph[u]:
                if dist[v] > dist[u] + w:
                    dist[v] = dist[u] + w
                    heapq.heappush(heap, (dist[v], v))
                    self.node_color[v] = "yellow"
                    self.step_text = f"更新节点 {v} 距离: {dist[v]}"
                    self.draw_graph()
                    time.sleep(0.8)
            self.node_color[u] = "green"
        self.step_text = f"执行完成，最终距离：{dist}"
        self.draw_graph()
        plt.ioff()

# GUI 面板
def run_bubble():
    data = [64, 34, 25, 12, 22, 11, 90]
    bubble_sort_visualize(data)

def run_dijkstra():
    dv = DijkstraVisual()
    dv.init_graph()
    dv.dijkstra_run("A")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("算法可视化控制台")
    root.geometry("320x180")
    ttk.Label(root, text="算法可视化工具", font=("Arial", 14)).pack(pady=15)
    ttk.Button(root, text="冒泡排序演示", command=run_bubble, width=20).pack(pady=5)
    ttk.Button(root, text="Dijkstra 最短路径", command=run_dijkstra, width=20).pack(pady=5)
    root.mainloop