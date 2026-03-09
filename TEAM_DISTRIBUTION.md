# Team Task Distribution & Ownership Tracker

This document details the responsibilities of each of the 5 team members working on the **Smart Process & Deadlock Manager**. The distribution of tasks ensures that every developer is responsible for specific algorithms and their respective logic and UI components.

---

## 1. Summary Tracker

| Person | Algorithms Owned | Primary Files | Status |
|---|---|---|---|
| **Person 1** | FCFS (CPU), First Fit, Best Fit, Disk FCFS | `core/scheduler.py`, `core/memory.py`, `core/disk.py`, `ui/scheduling_page.py`, `ui/memory_page.py`, `ui/disk_page.py` | 🔄 In Progress |
| **Person 2** | SJF, Worst Fit, Next Fit, SSTF (Disk) | `core/scheduler.py`, `core/memory.py`, `core/disk.py`, `ui/scheduling_page.py`, `ui/memory_page.py`, `ui/disk_page.py` | 🔄 In Progress |
| **Person 3** | SRTF, Banker's Algorithm, Deadlock Detection, Recovery | `core/scheduler.py`, `core/deadlock.py`, `core/step_scheduler.py`, `ui/scheduling_page.py`, `ui/deadlock_page.py` | 🔄 In Progress |
| **Person 4** | Priority (CPU), FIFO, LRU, Optimal, Clock (VM) | `core/scheduler.py`, `core/virtual_memory.py`, `ui/scheduling_page.py`, `ui/vm_page.py` | 🔄 In Progress |
| **Person 5** | Round Robin, Buddy System, SCAN, C-SCAN, App | `core/scheduler.py`, `core/memory.py`, `core/disk.py`, `ui/..._page.py`, `app.py`, `core/simulation_state.py`, `core/process.py`, `core/resource.py`, `ui/components.py` | 🔄 In Progress |

---

## 2. Detailed Distribution & Pending Tasks

### Person 1 — FCFS + Memory Part 1 + Disk FCFS
**Algorithms owned (4):** FCFS (CPU Scheduling), First Fit, Best Fit, Disk FCFS

**Files to own:**
- `core/scheduler.py` → FCFS function only
- `core/memory.py` → First Fit and Best Fit functions
- `core/disk.py` → FCFS function only
- `ui/scheduling_page.py` → FCFS rendering section
- `ui/memory_page.py` → First Fit and Best Fit sections
- `ui/disk_page.py` → FCFS rendering section

**Pending Tasks:**
- [ ] Verify FCFS Gantt chart renders correctly with correct CT, TAT, WT, RT values
- [ ] Verify First Fit and Best Fit show memory block map with allocated vs free blocks
- [ ] Verify Disk FCFS shows correct head movement order and total seek distance
- [ ] Be able to explain Convoy Effect in FCFS verbally

**Review Questions:**
- *"Why does FCFS suffer from the Convoy Effect?"*  
  → One long-burst process blocks all shorter processes behind it, inflating average waiting time.
- *"How does Best Fit differ from First Fit?"*  
  → Best Fit scans all blocks to find the tightest match; First Fit takes the first available block large enough regardless of waste.

---

### Person 2 — SJF + Memory Part 2 + SSTF
**Algorithms owned (4):** SJF (CPU Scheduling), Worst Fit, Next Fit, SSTF (Disk)

**Files to own:**
- `core/scheduler.py` → SJF function only
- `core/memory.py` → Worst Fit and Next Fit functions
- `core/disk.py` → SSTF function only
- `ui/scheduling_page.py` → SJF rendering section
- `ui/memory_page.py` → Worst Fit and Next Fit sections
- `ui/disk_page.py` → SSTF rendering section

**Pending Tasks:**
- [ ] Verify SJF tie-breaking uses Arrival Time when burst times are equal
- [ ] Verify Next Fit correctly resumes from last allocation pointer using modulo logic
- [ ] Verify SSTF always picks the closest track to current head using absolute distance
- [ ] Add fragmentation metric display for Worst Fit (show leftover space per block)

**Review Questions:**
- *"What is the starvation problem in SJF?"*  
  → Long processes may never execute if shorter processes keep arriving continuously.
- *"Why does SSTF cause starvation for outer tracks?"*  
  → If requests cluster near the current head position, far-away tracks are permanently skipped.

---

### Person 3 — SRTF + Full Deadlock Module
**Algorithms owned (4):** SRTF (CPU Scheduling), Banker's Algorithm, Deadlock Detection, Deadlock Recovery

**Files to own:**
- `core/scheduler.py` → SRTF function only
- `core/deadlock.py` → full ownership
- `core/step_scheduler.py` → full ownership
- `ui/scheduling_page.py` → SRTF rendering section
- `ui/deadlock_page.py` → full ownership

**Pending Tasks:**
- [ ] Verify SRTF preempts correctly on every new process arrival
- [ ] Add step-by-step Banker's safety loop visualization (show each iteration — which process gets added to safe sequence and why)
- [ ] Ensure Max, Allocation, Need, Available matrices all visible simultaneously in UI
- [ ] Ensure Recovery output shows terminated processes in order with released resources

**Review Questions:**
- *"How does SRTF decide when to context switch?"*  
  → It compares the running process's remaining time against the burst time of any newly arrived process at every time unit.
- *"Walk through the Banker's safety check steps"*  
  → Compute Need = Max - Allocation, find a process where Need <= Available, simulate its completion, release its resources, repeat until all processes finish or no candidate found.

---

### Person 4 — Priority + Full Virtual Memory Module
**Algorithms owned (5):** Priority Scheduling (CPU), FIFO, LRU, Optimal, Clock/Second Chance (all Virtual Memory)

*Note: Person 4 owns 5 algorithms because they have no app integration responsibility — workload is balanced.*

**Files to own:**
- `core/scheduler.py` → Priority function only
- `core/virtual_memory.py` → full ownership
- `ui/scheduling_page.py` → Priority rendering section
- `ui/vm_page.py` → full ownership

**Pending Tasks:**
- [ ] Verify Priority tie-breaking uses Arrival Time when priority values are equal
- [ ] Add step-by-step page replacement table (frame contents updating reference by reference with Hit/Fault marked at each step)
- [ ] Ensure Clock algorithm shows reference bit state per frame at every step with asterisk annotation for second-chance pages
- [ ] Add hit ratio display: Hit Ratio = (Total Refs - Faults) / Total Refs
- [ ] Add comparison table: page fault count for all 4 VM algorithms on same reference string

**Review Questions:**
- *"Why is Optimal page replacement impossible in a real OS?"*  
  → It requires knowing the future reference string, which no real OS can access — used only as a theoretical benchmark.
- *"How does Clock differ from pure FIFO?"*  
  → Clock gives each page a second chance by checking a reference bit before eviction; FIFO evicts blindly based on load order only.

---

### Person 5 — Round Robin + Disk SCAN/C-SCAN + Buddy System + App
**Algorithms owned (4):** Round Robin (CPU), Buddy System (Memory), SCAN (Disk), C-SCAN (Disk)

**Files to own:**
- `core/scheduler.py` → Round Robin function only
- `core/memory.py` → Buddy System function only
- `core/disk.py` → SCAN and C-SCAN functions
- `ui/scheduling_page.py` → Round Robin section
- `ui/memory_page.py` → Buddy System section
- `ui/disk_page.py` → SCAN and C-SCAN sections
- `app.py` → full ownership
- `core/simulation_state.py` → full ownership
- `core/process.py` → full ownership
- `core/resource.py` → full ownership
- `ui/components.py` → full ownership

**Pending Tasks:**
- [ ] Verify Round Robin correctly handles quantum expiry and re-queuing to back of ready queue
- [ ] Improve Buddy System tree visualization (show split/merge tree not just final state)
- [ ] Add disk seek movement chart with head position clearly plotted against request order
- [ ] Add seek distance comparison table for all 4 disk algorithms on same input (FCFS, SSTF, SCAN, C-SCAN side by side)
- [ ] Fix session state conflicts between modules (switching tabs must not reset other module states)
- [ ] Maintain implemented_plan.md as team completes pending tasks

**Review Questions:**
- *"What happens to Round Robin efficiency as quantum size increases?"*  
  → Very large quantum approaches FCFS behaviour; very small quantum increases context switching overhead and hurts performance.
- *"How does C-SCAN differ from SCAN at the boundary?"*  
  → SCAN reverses direction at the boundary and serves requests on the return sweep; C-SCAN jumps back to position 0 without serving any requests on the return, ensuring uniform wait times.

---

## 3. Shared Responsibilities

- **Code Merging / Global State:** Person 5 handles all Git merges and cross-module changes to `app.py` and `components.py`.
- **Validation Pipeline:** All team members must thoroughly test their algorithms using at least 3 separate deterministic dataset strings prior to the project review.
- **Review Strategy:** Every individual is fully accountable for manually presenting their configured modules. You must only answer questions on your specific algorithms constraint map.

---

## 4. Ground Rules

- **Respect Module Ownership:** Never computationally modify another person's algorithm function directly. Provide feedback to them Native so they can execute their own refactoring.
- **Centralized Logic Pipeline:** All core file mapping and logic updates impacting shared component UI (`app.py`, `components.py`) must be systematically processed through Person 5.
- **Testing Standard:** Code execution without verification is forbidden. Every logic engine must run 3 custom input dataset scenarios flawlessly before we approach presentation staging status.
