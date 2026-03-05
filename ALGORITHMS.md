# Algorithms Documentation

This document explicitly outlines the theoretical rules, mathematical formulas, and simulation assumptions behind the **Smart Process & Deadlock Manager**.

---

## 1. CPU Scheduling Algorithms
**Purpose**: To decide which process in the ready queue gets the CPU next to maximize efficiency and minimize waiting time.

### Formulas
- **Completion Time (CT)**: Time at which process finishes execution.
- **Turnaround Time (TAT)**: `Completion Time − Arrival Time`
- **Waiting Time (WT)**: `Turnaround Time − Burst Time`
- **Response Time (RT)**: `First CPU Allocation Time − Arrival Time`

### Implemented Algorithms
1. **FCFS (First-Come, First-Served)**: Non-preemptive. Scheduled strictly iteratively by `Arrival Time`.
2. **SJF (Shortest Job First)**: Non-preemptive. Scheduled by the minimum purely expected `Burst Time`.
3. **SRTF (Shortest Remaining Time First)**: Preemptive. Re-evaluates CPU possession every time unit. If a new process arrives with a shorter `Remaining Time` than the currently running process, a context switch happens.
4. **Priority Scheduling**: Non-preemptive. Executes based on the provided integer `Priority` value (Lower numbers = Higher priority).
5. **Round Robin**: Preemptive. Assigns a fixed `Time Quantum` (e.g., 2 units) uniformly across the execution queue.

---

## 2. Deadlock Management
**Purpose**: Handling resource allocation tracking so that the OS does not enter a "circular wait" state.

### Banker's Algorithm (Avoidance)
- **Max Need Matrix**: Maximum demand of each process.
- **Allocation Matrix**: Resources currently held by a process.
- **Need Matrix**: Calculated logically as `Max Matrix − Allocation Matrix`.
- **Available Resources**: Total Resources initialized − Sum of Allocation columns.

**Rule**: A resource request is only granted if:
1. `Request <= Need`
2. `Request <= Available`
3. Simulating the allocation yields a computationally **Safe Sequence** where all processes can theoretically finish.

### Deadlock Detection & Recovery
- Uses the same algorithm as Banker's safety check but operates on assumed 'Request Arrays'.
- Recovery is executed by iteratively terminating processes holding resources (releasing their locks) until the circular wait breaks.

---

## 3. Contiguous Memory Management
**Purpose**: Partitioning physical main memory blocks mathematically for dynamic scaling.

### Algorithms
1. **First Fit**: Finds the very first available free block that satisfies `Block Size >= Process Request Size`.
2. **Best Fit**: Iterates the entire memory array to seek the smallest possible free block that satisfies `Block Size >= Process Request Size`. Designed to minimize leftover wasted space.
3. **Worst Fit**: Evaluates the memory array to intentionally assign the largest possible block fragment. 
4. **Next Fit**: Begins searching from the exact pointer location of the last assignment rather than scanning from memory index 0.

### Buddy System Allocation
- Mandates that memory pools must be powers of 2.
- A request of `Size N` will recursively seek the smallest power of 2 bounding target. If a node is too large, it is split in half (into "Buddies") until a precise match is found, building a bifurcating search tree.

---

## 4. Virtual Memory (Demand Paging)
**Purpose**: Solving situations where processes are larger than physical frames by swapping pages out to secondary storage limits.

### Terminology:
- **Reference String**: Sequential integers outlining which memory pages are required by a process incrementally.
- **Page Fault**: A "Miss". Raised when the CPU requests a page that is not currently mapped in any hardware frame, requiring a relatively costly swap-in operation.

### Page Replacement Implementations
1. **FIFO (First-In, First-Out)**: A basic queue implementation tracking the oldest frame assigned.
2. **LRU (Least Recently Used)**: Dynamically shuffles frame priorities so the most recently accessed node sits safely at the tail, and the unvisited node shifts natively to index 0 eviction status.
3. **Optimal**: Conceptually impossible in real OS engines. Looks into the *future arrays* of the Reference String to drop whichever page is required furthest out.
4. **Clock (Second-Chance)**: Similar to FIFO, but attaches a "1" bit flag to nodes upon first mapping. Upon eviction, if encountering a 1, it changes the bit to "0" (a second chance) and iterates to the next pointer.

---

## 5. Disk Scheduling Algorithms
**Purpose**: Navigating physical hard-drive controller head movements iteratively across track / cylinder arrays.

### Seek Time Implementations
1. **FCFS**: Heads move directly in the sequential order requested.
2. **SSTF (Shortest Seek Time First)**: Scans unserved requests seeking the minimal angular distance (Absolute Distance metric) from the current head pointer.
3. **SCAN (Elevator)**: Traces cleanly to the boundary limit of the disk (e.g., 0 or Max_Tracks), serving requests on its path, then reverses direction.
4. **C-SCAN (Circular SCAN)**: Traces cleanly to the boundary limit exclusively in one direction. Upon hitting the limit, mathematically 'jumps' back to the start (origin without serving entries mid-jump) and iterates again.
