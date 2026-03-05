# Project Architecture

The **Smart Process & Deadlock Manager** simulator utilizes a modern, clean separation of concerns. The application is strictly divided between the **Frontend UI Layer** (Streamlit rendering) and the **Backend Modeling Layer** (pure Python object-oriented algorithms).

This ensures the simulation algorithms are mathematically pure, testable, and entirely agnostic of the GUI visualization tools used to display them.

---

## 📂 Directory Structure

```text
os_cp/
│── app.py                      # Main application entry point & Streamlit configuration
│
├── core/                       # Pure Python Backend Engine
│   ├── simulation_state.py     # Global state holder (injects modules into Streamlit session)
│   ├── process.py              # Process Control Block (PCB) definitions
│   ├── scheduler.py            # CPU time-slicing logic (SJF, SRTF, MLFQ)
│   ├── resource.py             # Matrices for OS deadlock states
│   ├── deadlock.py             # Banker's safety and extraction routines
│   ├── memory.py               # Memory partitioning logic & Buddy System trees
│   ├── virtual_memory.py       # Paging fault reference array mapping
│   └── disk.py                 # R/W Head track distance calculations
│
└── ui/                         # Streamlit View Modules
    ├── components.py           # Shared UI elements (editable process dataframes)
    ├── scheduling_page.py      # CPU Metrics and Gantt Chart Plotly renders
    ├── deadlock_page.py        # Resource Allocation tables
    ├── memory_page.py          # Partitions and Stacked Bar Graph blocks
    ├── vm_page.py              # Stepped Page Fault arrays and Hit Ratio Pies
    └── disk_page.py            # 2D Head-Movement tracing algorithms
```

---

## 🔄 State Management

Because Streamlit reruns scripts continuously upon any user interaction, maintaining a persistent simulation state across tabs requires caching. 

The project solves this by attaching an instance of `SimulationState` to `st.session_state` upon app launch.

`app.py` acts as the router. It instantiates the central brain:
```python
if "sim" not in st.session_state:
    st.session_state.sim = SimulationState()
```

Each modular UI page in `ui/` receives this `sim` object and interacts strictly with its internal sub-managers (e.g., `sim.process_manager`, `sim.memory_manager`).

### Example Flow:
1. User interacts with Streamlit's `ui/memory_page.py`.
2. UI passes an array of partition sizes to `sim.memory_manager.allocate_first_fit()`.
3. `core/memory.py` executes mathematical validations, updates internal dictionary properties, and returns a JSON-style result dictionary.
4. `ui/memory_page.py` reads the returned logs and draws a Stacked Bar Graph via Plotly Express.
