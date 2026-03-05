# Smart Process & Deadlock Manager

A comprehensive, interactive **Operating System Simulator** built in Python.

This project was developed to provide a visual, professional, and mathematically rigorous demonstration of core Operating System concepts taught in computer science curricula. It features a modern web-based dashboard that interactively simulates algorithms rather than relying on abstract console outputs.

---

## 🌟 Key Features

The simulator is divided into five core educational modules:

1. **CPU Scheduling**
   - Real-time Gantt Chart visualization of execution history.
   - Supports: FCFS, SJF (Non-preemptive), SRTF (Preemptive), Priority Scheduling, Round Robin.
2. **Deadlock Management**
   - Tracks Resource configurations against dynamic Max Need / Allocation matrices.
   - Supports: Deadlock Detection, Banker's Algorithm (Avoidance), and safe Recovery execution.
3. **Memory Allocation** 
   - Interactive physical memory partition assignment.
   - Visualizes internal fragmentation and free space mapping dynamically.
   - Supports: First Fit, Best Fit, Worst Fit, Next Fit, and the hierarchical **Buddy System**.
4. **Virtual Memory & Paging**
   - Simulates Translation Lookaside and Page Fault tracking based on reference strings.
   - Plots interactive Hit vs. Miss Ratio pie charts.
   - Supports: FIFO, LRU, Optimal, and Clock (Second Chance).
5. **Disk Scheduling**
   - Maps physical disk R/W Head movements across cylinders over time.
   - Visualizes seeking paths as a 2D line-trace graph.
   - Supports: FCFS, SSTF, SCAN, C-SCAN.

---

## 🛠️ Technology Stack

- **[Python 3.10+](https://www.python.org/)**: The core backend algorithmic engine.
- **[Streamlit](https://streamlit.io/)**: The frontend framework driving the interactive web dashboard.
- **[Plotly](https://plotly.com/python/)**: Powers the dynamic Gantt charts, Scatter traces, and Stacked block visualizers.
- **[Pandas](https://pandas.pydata.org/)**: Manages state matrix renderings and metrics tables cleanly.

---

## 🚀 How to Run the Simulator

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/os_simulator.git
   cd os_simulator
   ```

2. **Install dependencies:**
   *(Ensure you have `streamlit`, `pandas`, and `plotly` installed via pip)*
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the Engine:**
   ```bash
   streamlit run app.py
   ```
   *The dashboard will instantly open in your default local web browser (typically on `localhost:8501`).*

---

## 📸 Example Screenshots

*(Insert actual paths to your repository images here before deploying)*

- **CPU Scheduling Dashboard**: `![CPU Scheduler](path/to/cpu_screenshot.png)`
- **Memory Allocation Visualization**: `![Memory Blocks](path/to/memory_screenshot.png)`
- **Virtual Memory Simulation**: `![Page Replacement](path/to/vm_screenshot.png)`
- **Disk Scheduling Graph**: `![Disk Trace](path/to/disk_screenshot.png)`

---

## 📚 Documentation Reference

For deeper insights into how this project is structured and scaled, please refer to the adjoining documentation files:
- [ARCHITECTURE.md](./ARCHITECTURE.md) - System architecture and Python/Streamlit separation of concerns.
- [ALGORITHMS.md](./ALGORITHMS.md) - Theoretical rules driving the backend models.
- [UI_GUIDE.md](./UI_GUIDE.md) - Manual on operating the Streamlit dashboard effectively.
- [TESTING.md](./TESTING.md) - Quick-reference test scenarios for validating the system.
