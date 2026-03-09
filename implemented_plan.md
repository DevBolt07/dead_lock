# Smart Process & Deadlock Manager
**Implementation Plan & Mid-Semester Review Document**

---

## Current Build Status

| Module / Feature | Status |
|------------------|--------|
| **Core Architecture & Streamlit UI Base** | ✅ Implemented |
| **CPU Scheduling Algorithms (All)** | ✅ Implemented |
| **Deadlock Avoidance & Detection** | ✅ Implemented |
| **Memory Allocation Basics** | ✅ Implemented |
| **Virtual Memory Map & Paging** | ✅ Implemented |
| **Disk Scheduling Seeking Matrix** | ✅ Implemented |
| **Algorithm Comparison Engine** | 🔄 In Progress |
| **Step-by-Step UI Execution** | 🔄 In Progress |
| **Process State Transition Graphs** | ❌ Pending |

---

## 1. Project Overview

**Project:** Smart Process & Deadlock Manager  
**Course:** ML2307 Operating Systems, Vishwakarma Institute of Technology (VIT) Pune, A.Y. 2025-26  

**Educational Problem Solved:**  
Operating system algorithms generally resolve rapidly behind the scenes, leaving students without a clear visual representation. The **Smart Process & Deadlock Manager** resolves this by providing an interactive UI mapping step-by-step algorithms logically for immediate visual tracing. This translates complex system theories into distinct, observable processes without directly risking host execution systems.

**Technology Stack:**
- **Language:** Python 3.9+
- **Frontend Framework:** Streamlit (UI components and continuous state rendering)
- **Data Manipulation:** Pandas (Metric organization and structural mapping)
- **Visualization:** Plotly Express (Interactive graphics: Gantt charts, Bar stacks, Traces)

**High-Level Architecture:**
The logic engine (`core/`) and frontend UI (`ui/`) are distinctly separated. Global application states persist successfully using `st.session_state` wrapped within a central `SimulationState` proxy map.

---

## 2. Syllabus Coverage Map

| Syllabus Unit | Core Concept Focus | Features Implemented |
|---|---|---|
| **Unit III** | CPU Scheduling | FCFS, SJF, SRTF, Priority, RR |
| **Unit IV** | Deadlocks | Banker's Avoidance, Detection, Recovery |
| **Unit V** | Memory Allocation | First/Best/Worst/Next Fit + Buddy System |
| **Unit V** | Page Replacement | FIFO, LRU, Optimal, Clock (Second Chance) |
| **Unit VI** | Disk Path Scheduling | FCFS, SSTF, SCAN, C-SCAN |

---

## 3. Simulator Modules Overview

### Module A: CPU Scheduling Simulator
**Purpose:** Maps OS context-switching workflows dynamically across time values.  
**Evaluations (`core/scheduler.py`):**
- **FCFS:** Non-preemptive. Executes sequentially based upon Arrival Time.
- **SJF:** Non-preemptive. Targets processes bearing the shortest remaining Burst Time.
- **SRTF:** Preemptive. Frequently compares existing execution limits to newly arrived processes, switching contexts appropriately.
- **Priority:** Processes trigger purely according to assigned integers.
- **Round Robin:** Processes are restricted by standard uniform Time Quantum constraints, shifting sequentially back to the execution queue naturally.

**Key Metrics Calculated:**
- Turnaround Time = `Completion Time - Arrival Time`
- Waiting Time = `Turnaround Time - Burst Time`
- Response Time = `First Execution Time - Arrival Time`

---

### Module B: Deadlock Management
**Purpose:** Visualizes safe process execution states without creating closed cyclic blockages.  
**Evaluations (`core/deadlock.py`):**
- System checks logic requirements measuring `Need = Max - Allocation`.
- **Banker’s Algorithm Avoidance:** Verifies a hypothetical resource map to ensure `Need <= Available`. If it clears sequentially across processes, it returns a Safe Sequence matrix.
- **Deadlock Detection & Recovery:** Checks for locked cycles dynamically, releasing processes holding resources one-by-one prioritizing lower priority process thresholds automatically via UI logs.

---

### Module C: Contiguous Memory Management
**Purpose:** Demonstrates OS physical allocation behavior mapping block assignments natively.  
**Evaluations (`core/memory.py`):**
- **First Fit:** Targets and returns the closest primary block exceeding requested limitations.
- **Best Fit:** Examines the complete array minimizing internal fragmentation.
- **Worst Fit:** Consciously assigns the highest volume block naturally leaving extended space fragments.
- **Next Fit:** Remembers sequence assignments across loops picking off sequential location indexes natively using modular loops.
- **Buddy System:** Adjusts requests cleanly into Power of 2 sets branching arrays into matching pairs efficiently via `Split` functionality.

---

### Module D: Virtual Memory — Demand Paging
**Purpose:** Simulates how physical memory boundaries fall back onto swap arrays tracking cache Fault / Hit metrics.  
**Evaluations (`core/virtual_memory.py`):**
- **FIFO:** Drops nodes based purely on earliest index entry.
- **LRU:** Up-cycles specific frame arrays sequentially protecting recently queried pages.
- **Optimal:** Calculates predictive indexes evaluating the longest untouched time metric against the remainder Reference array.
- **Clock:** Assigns 1-bit flags sequentially. Grants an additional validation check prior to eviction, displaying output logic physically to the user on the dashboard.

---

### Module E: Disk Scheduling
**Purpose:** Calculates read/write hardware head optimization seeking limits across defined track sets.  
**Evaluations (`core/disk.py`):**
- **FCFS:** Tracks sequentially evaluating the absolute difference from the source track directly mapping head values.
- **SSTF:** Examines queue targets selecting absolute nearest distance continuously creating localized starvation intentionally.
- **SCAN:** Calculates track lists processing limits exactly resolving bounds towards one side completely prior to reversing direction.
- **C-SCAN:** Examines limits linearly bounding dynamically reverting sequentially back to `Track 0` resolving arrays across continuous one-way loop sweeps.

---

## 4. Step-by-Step Execution Overview

The simulator incorporates a comprehensive deep-copied execution array model using `core/step_scheduler.py`.
- **Logic Format:** Freezes metrics across incremental Time variables (`t = 0, t = 1, t = 2`).
- **Dashboard Outputs:** The UI breaks standard queues functionally into `Job Queue`, `Ready Queue`, `Running CPU`, and `Completed` arrays dynamically allowing learners to step back and forth visually analyzing logic flow states logically mapped block-by-block.

---

## 5. File & Folder Hierarchy

```text
os_cp/
├── app.py                      
├── core/                       # Calculation backend operations
│   ├── process.py              
│   ├── resource.py             
│   ├── scheduler.py            
│   ├── step_scheduler.py       
│   ├── deadlock.py             
│   ├── memory.py               
│   ├── virtual_memory.py       
│   ├── disk.py                 
│   └── simulation_state.py     
└── ui/                         # Streamlit rendering outputs
    ├── components.py           
    ├── scheduling_page.py      
    ├── deadlock_page.py        
    ├── memory_page.py          
    ├── vm_page.py              
    └── disk_page.py            
```

---

## 6. How to Run

1. Configure Python 3.9+ requirements:
```bash
pip install streamlit pandas plotly
```

2. Initialize the application locally:
```bash
streamlit run app.py
```
*(The UI interface will instantly initialize routing port traffic securely toward localhost.)*
