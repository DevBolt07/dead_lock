# Smart Process & Deadlock Manager

A comprehensive, interactive Operating System Simulator built in Python. This project provides a visual, professional, and mathematically rigorous demonstration of core Operating System concepts. It features a modern web-based dashboard that interactively simulates algorithms, allowing students to trace step-by-step logic visually rather than relying on abstract console outputs.

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-red)
![License](https://img.shields.io/badge/license-MIT-green)

---

## Table of Contents
- [Problem Statement](#problem-statement)
- [Features by Module](#features-by-module)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [How to Run](#how-to-run)
- [Syllabus Coverage](#syllabus-coverage)
- [Screenshots](#screenshots)
- [Team Allocation](#team-allocation)
- [License](#license)

---

## Problem Statement
Operating system algorithms such as CPU scheduling and memory allocation execute in microseconds, making their internal workings practically invisible to students. The "Smart Process & Deadlock Manager" solves this educational gap by offering an interactive simulator where users can input specific datasets and visually trace every execution step. This maps abstract OS theories to observable and predictable software flows without risking actual host OS stability.

---

## Features by Module

### 1. CPU Scheduling
- Real-time interactive Gantt Chart visualization.
- Algorithms: FCFS, SJF (Non-preemptive), SRTF (Preemptive), Priority Scheduling, Round Robin.

### 2. Deadlock Management
- Tracks Resource configurations against dynamic Max Need / Allocation matrices.
- Features: Deadlock Detection, Banker's Algorithm (Avoidance), Safe Sequence Calculation, and automatic Recovery execution.

### 3. Memory Allocation
- Interactive physical partition mapping.
- Visualizes internal fragmentation and free space dynamically.
- Algorithms: First Fit, Best Fit, Worst Fit, Next Fit, and Buddy System.

### 4. Virtual Memory (Demand Paging)
- Simulates page frame memory misses using reference strings.
- Interactive Hit vs. Miss Ratio tracking.
- Algorithms: FIFO, LRU, Optimal, and Clock (Second Chance).

### 5. Disk Scheduling
- Maps physical disk Read/Write head movements visually.
- Generates 2D seek trace paths across simulated cylinders.
- Algorithms: FCFS, SSTF, SCAN, C-SCAN.

---

## Technology Stack

| Tool | Purpose | Version |
|---|---|---|
| **Python** | Core backend algorithmic logic engine | 3.10+ |
| **Streamlit** | Interactive UI frontend framework | Latest |
| **Pandas** | Matrix calculations, metric aggregations, and tables | Latest |
| **Plotly** | Dynamic Gantt charts, traces, and visual graphics | Latest |

---

## Project Structure

```text
os_cp/
├── app.py                      # Main entry point; renders Streamlit sidebar & tabs
├── core/                       # Simulation Engine Backend 
│   ├── process.py              # Process data structures and centralized list manager
│   ├── resource.py             # Global active/max physical resource tracker arrays 
│   ├── scheduler.py            # Static algorithm mappings running standard metrics
│   ├── step_scheduler.py       # Snapshot iteration simulator core (state caching)
│   ├── deadlock.py             # Banker's safety loop loops & detector
│   ├── memory.py               # Memory block grid manager & Buddy System builder 
│   ├── virtual_memory.py       # Page replacement tracking array matrices 
│   ├── disk.py                 # Seek algorithm sequence builders 
│   └── simulation_state.py     # Aggregated environment orchestrator / demo payload
└── ui/                         # Streamlit visual rendering blocks
    ├── components.py           # Boilerplate shared frontend UI grids
    ├── scheduling_page.py      # Simulation dashboards and CPU logic 
    ├── deadlock_page.py        # Resource table Matrix renderer 
    ├── memory_page.py          # Partitions visual layout 
    ├── vm_page.py              # Page array status frame map
    └── disk_page.py            # Math charts tracking IO head locations
```

---

## How to Run

```bash
git clone <repo>
cd os_cp
pip install -r requirements.txt
streamlit run app.py
```

---

## Syllabus Coverage

Mapping corresponding to ML2307 Operating Systems curriculum (VIT Pune, A.Y. 2025-26):

| Implemented Feature | ML2307 Unit Coverage |
|---|---|
| FCFS, SJF, SRTF, Priority, RR | Unit III: CPU Scheduling |
| Banker's, Detection, Recovery | Unit IV: Deadlocks |
| Contiguous Allocation, Target Fit Algorithms, Buddy System | Unit V: Memory Management |
| Virtual Memory, FIFO, LRU, Optimal, Clock Replacements | Unit V: Memory Management |
| FCFS, SSTF, SCAN, C-SCAN | Unit VI: Disk Scheduling |

---

## Screenshots

*(Placeholder: Make sure to add images covering the respective UI pages here.)*

- `![CPU Scheduler Dashboard](path/to/cpu_screenshot.png)`
- `![Deadlock Manager Matrices](path/to/deadlock_screenshot.png)`
- `![Memory Blocks Traces](path/to/memory_screenshot.png)`
- `![Virtual Memory Hit Ratios](path/to/vm_screenshot.png)`
- `![Disk Scheduling Vectors](path/to/disk_screenshot.png)`

---

## Team Allocation

Our simulation modules and algorithm functions have been securely distributed to ensure clean version control management: 
- **Person 1:** FCFS (CPU), First Fit, Best Fit, Disk FCFS
- **Person 2:** SJF (CPU), Worst Fit, Next Fit, SSTF (Disk)
- **Person 3:** SRTF (CPU), Banker's Algorithm, Deadlock Detection, Deadlock Recovery
- **Person 4:** Priority (CPU), FIFO, LRU, Optimal, Clock (Virtual Memory)
- **Person 5:** Round Robin (CPU), Buddy System, SCAN, C-SCAN, App Integration

---

