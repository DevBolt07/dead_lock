# Simulator UI Guide

Welcome to the **Smart Process & Deadlock Manager**. Because this system relies heavily on a visual Streamlit dashboard rather than a CLI, this guide helps users effortlessly navigate the inputs, parameters, and visualizations available on each tab.

---

## 🧭 Global Controls (Sidebar)

On the left-hand side of the screen, you will always see the **Sidebar**.
- **Load Demo Data Button**: Clicking this resets the entire simulation and populates standard, solvable "dummy processes" (e.g., P1, P2, P3) so you can test features without typing arrays manually.
- **Active Processes List**: Displays the current PIDs loaded into memory.

---

## 1. CPU Scheduling Tab

**What it does:** Simulates time-slicing algorithms on the current process queue.

**Inputs Available:**
- **Add Process Row**: Use the editable table to define custom `PID`, `Arrival Time`, `Burst Time`, and `Priority` integers.
- **Algorithm Dropdown**: Select between FCFS, SJF, SRTF, Priority, and Round Robin.
- **Time Quantum**: (Only visible for Round Robin) Adjust the execution time slice.

**Outputs Generated:**
1. **Interactive Gantt Chart**: Hover over the horizontal bars to see exactly when contexts switched.
2. **Metrics Table**: A generated DataFrame tracking Turnaround Time mathematically.

---

## 2. Deadlock Management Tab

**What it does:** Simulates Banker's Algorithm and the circular-wait state mapping.

**Inputs Available:**
- **Max Need Matrix**: Pre-define the absolute maximum resources a process could request.
- **Live Allocation Matrix**: Define what processes currently physically hold.
- **Resource Request Array**: Force a theoretical allocation constraint request against Banker's safety loop.

**Outputs Generated:**
1. **Safe Sequence Array**: If safe, prints the execution string (e.g., `P2 -> P1 -> P4`).
2. **Recovery Simulator**: Visually terminates deadlocked processes one-by-one, releasing locks until the OS is safe again.

---

## 3. Memory Allocation Tab

**What it does:** Assigns incoming processes to fixed contiguous physical address spaces.

**Inputs Available:**
- **Custom Free Blocks Data**: A comma-separated string mapping out physical partition slots (e.g., `100, 500, 200, 300`).
- **Target Incoming Requests**: A comma-separated array of process sizes seeking memory execution (e.g., `212, 417, 112`).
- **Algorithm Dropdown**: Choose between Best Fit, Worst Fit, First Fit, Next Fit, or Buddy System.

**Outputs Generated:**
1. **Block Graph Trace**: A dynamically generated proportional bar chart showing specifically which process PID holds what memory segment, stacked against grey `Free Space`.
2. **Internal Fragmentation Log**: Mathematical sum of wasted space bytes explicitly mapped out alongside the execution log string.

---

## 4. Virtual Memory Tab

**What it does:** Replicates hardware page mapping frames against a continuous demand request reference string.

**Inputs Available:**
- **Reference String Array**: The exact order of pages required logically (e.g., `7,0,1,2,0,3...`).
- **Frames Counter**: Establish the physical bounding limit of memory slots (typically between 3 to 5).
- **Algorithm Dropdown**: FIFO, LRU, Clock, or Optimal theoretical mapping.

**Outputs Generated:**
1. **DataFrame Walkthrough**: A visual table stepping backwards and forwards recursively showing exactly when a 'Miss' occurred and which slot rotated appropriately.
2. **Hit vs Miss Ratio**: Interactive Plotly pie chart proving the statistical efficiency of the algorithm dynamically mapped.

---

## 5. Disk Scheduling Tab

**What it does:** Calculates seek distance mathematics for a physical physical hard drive mechanism.

**Inputs Available:**
- **Request Queue**: Comma separated array. Cylinders the device needs to index into sequentially (e.g., `82, 170, 43...`).
- **Head Position Integer**: The starting boundary track where the needle sits.
- **Direction**: (Only visible for SCAN/C-SCAN) Determines if the head should move `Left (to 0)` or `Right (to boundary limit)` initially.

**Outputs Generated:**
1. **Physical Path Distance Matrix**: Emits a descending trace map. You can visually track the 'elevator' scanning functionally up and down the boundary space across time ticks mathematically.
2. **Total Seek Metric**: Exact numerical distance summation output.
