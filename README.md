# Algorithm Visualizer + Time-Series Simulation + FastAPI Backend Project
## Project Introduction
This repo holds three independent Python projects I built to practice core computer science fundamentals during self-study. I wanted to consolidate knowledge of graph algorithms, data processing pipelines and lightweight web service development, so I split the work into three separate modules with clear boundaries.

### Algorithm-Visualizer
I implemented animated visualization for bubble sort and Dijkstra’s shortest path algorithm. The animation step-by-step shows how each algorithm iterates and updates states, which helped me better understand the inner logic of sorting and graph pathfinding.

### Data-Simulation-Engine
A self-written time-series simulation framework. I coded basic metric calculation modules, rule-based simulation logic, result evaluation tools and plotting functions to visualize output performance. All data processing logic is modularized for easy extension.

### FastAPI-Service
A simple high-performance backend built with FastAPI. I created structured data ETL pipelines and exposed standard RESTful interfaces for data query and batch computation requests.

## Environment Setup
All required packages are unified in one dependency file. Open your terminal and run the command below to finish installation:
```bash
pip install -r requirements.txt

Personal Takeaways
Working on this multi-module project let me practice modular programming, cross-platform environment configuration and data visualization. I also learned how to design clean API layers and separate algorithm logic from data processing code.
