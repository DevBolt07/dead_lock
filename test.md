# Smart Process & Deadlock Manager - Test Plan

## 1. Project Under Test
**Project Name:** Smart Process & Deadlock Manager
**Type:** Command-Line Interface (CLI) Simulation
**Description:** A Python-based simulation of core Operating System components including Process Management, CPU Scheduling (FCFS, Priority, Round Robin), Resource Allocation, and Deadlock Management (Detection, Avoidance, Recovery). The system operates in user-space and simulates OS behaviors algorithmically.

## 2. Test Environment
- **Language:** Python 3.x
- **OS:** Windows / Linux / macOS (Cross-platform)
- **Execution Command:** `python main.py`
- **Interface:** Interactive Menu-Driven CLI

## 3. Test Data (Reusable Dataset)
Use the following data for consistent testing across scenarios.

### Processes
| PID | Burst Time | Priority (Lower=Higher) | Arrival Time |
| :--- | :--- | :--- | :--- |
| **p1** | 5 | 2 | 0 |
| **p2** | 3 | 1 | 2 |
| **p3** | 4 | 3 | 4 |

### Resources
- **R1**: 5 instances
- **R2**: 3 instances

### Max Need (Banker's Algorithm)
| PID | Max Need |
| :--- | :--- |
| **p1** | R1:3, R2:2 |
| **p2** | R1:2, R2:1 |
| **p3** | R1:4, R2:1 |

---

## 4. Functional Test Cases

### 4.1 Process Management
**Objective:** Verify process creation and state tracking.

| ID | Test Case | Steps / Input | Expected Result |
| :--- | :--- | :--- | :--- |
| **PM-01** | Create Process p1 | 1. Select **1** (Create Process)<br>2. PID: `p1`<br>3. Burst: `5`<br>4. Priority: `2`<br>5. Arrival: `0` | "Process p1 created successfully." |
| **PM-02** | Create Process p2 | 1. Select **1**<br>2. PID: `p2`<br>3. Burst: `3`<br>4. Priority: `1`<br>5. Arrival: `2` | "Process p2 created successfully." |
| **PM-03** | Create Process p3 | 1. Select **1**<br>2. PID: `p3`<br>3. Burst: `4`<br>4. Priority: `3`<br>5. Arrival: `4` | "Process p3 created successfully." |
| **PM-04** | Show Process Table | 1. Select **2** (Show Process Table) | Table displays p1, p2, p3 with correct attributes and state "Ready". |

### 4.2 Resource Management
**Objective:** Verify resource configuration, request, and allocation.

| ID | Test Case | Steps / Input | Expected Result |
| :--- | :--- | :--- | :--- |
| **RM-01** | Configure Resources | 1. Select **4** (Configure Resources)<br>2. Input: `R1:5,R2:3` | "Resources initialized: {'R1': 5, 'R2': 3}" |
| **RM-02** | Request Valid Resource | 1. Select **5** (Request Resource)<br>2. PID: `p1` -> Resource: `R1` -> Amount: `2` | "Request granted. p1 allocated 2 of R1." |
| **RM-03** | Check Status | 1. Select **7** (Show Resource Status) | p1 Allocation: R1=2. Available: R1=3, R2=3. |
| **RM-04** | Block Process (Wait) | 1. Select **5**<br>2. PID: `p2` -> Resource: `R1` -> Amount: `4` | "Resources not available. Process p2 blocked (Waiting)." |
| **RM-05** | Verify Waiting State | 1. Select **2** | p2 State is "Waiting". |
| **RM-06** | Release & Unblock | 1. Select **6** (Release Resource)<br>2. PID: `p1` -> Resource: `R1` -> Amount: `2` | Resources released. p2 checks wait, gets R1 (if available), state becomes "Ready". |

### 4.3 Deadlock Avoidance (Banker's Algorithm)
**Objective:** Verify safety checks.

| ID | Test Case | Steps / Input | Expected Result |
| :--- | :--- | :--- | :--- |
| **BA-01** | Set Max Need | 1. Select **8** (Set Max Need)<br>2. PID: `p1` -> Need: `R1:3,R2:2` | "Max need set for Process p1..." |
| **BA-02** | Avoidance Check (Safe) | 1. Select **10** (Option 10 simulates a request and performs a safety check using Banker’s algorithm.)<br>2. PID: `p1` -> Resource: `R1` -> Amount: `1` | "Safe State confirmed." |
| **BA-03** | Avoidance Check (Unsafe)| 1. Select **10** (Option 10 simulates a request and performs a safety check using Banker’s algorithm.)<br>2. Request amount > Available but leading to deadlock | "Unsafe State! Granting request would lead to possible deadlock." |

### 4.4 CPU Scheduling
**Note:** Scheduling terminates processes. Re-create processes if needed before running different algorithms.
**Note:** Deadlock and resource-management related test cases must be executed before running any scheduling algorithm, because scheduling terminates processes.

| ID | Test Case | Steps / Input | Expected Result |
| :--- | :--- | :--- | :--- |
| **SCH-01** | FCFS Scheduling | 1. Select **3** (Run Scheduler)<br>2. Select **1** (FCFS) | Order: p1 -> p2 -> p3. (Based on Arrival Time). |
| **SCH-02** | Priority Scheduling | 1. Re-create p1, p2, p3.<br>2. Select **3** -> **2** (Priority) | Order: p1 -> p2 -> p3 (p2 arrives at 2, but p1 runs 0-5. p2 is waiting. p1 finishes. p2(1) vs p3(3). p2 runs. Then p3 runs). |
| **SCH-03** | Round Robin | 1. Re-create p1, p2, p3.<br>2. Select **3** -> **3** (RR) -> Quantum: `2` | Interleaved execution (p1->p2->p1->p3...). |

---

## 5. Special Test Scenario - Deadlock Creation & Recovery
**Scenario:** Create a circular wait using 2 processes and 2 resources.
**Setup:** Resources `R1:1, R2:1`.

| Step | Action | Input | Expected Outcome |
| :--- | :--- | :--- | :--- |
| 1 | Configure Resources | **Option 4** -> `R1:1,R2:1` | Resources Set. |
| 2 | Create Process a | **Option 1** -> `a`, `10`, `1`, `0` | Process a created. |
| 3 | Create Process b | **Option 1** -> `b`, `10`, `5`, `0` | Process b created (Lower Priority). |
| 4 | a requests R1 | **Option 5** -> `a`, `R1`, `1` | Granted. Alloc: a={R1:1}. |
| 5 | b requests R2 | **Option 5** -> `b`, `R2`, `1` | Granted. Alloc: b={R2:1}. |
| 6 | a requests R2 | **Option 5** -> `a`, `R2`, `1` | **Blocked**. a waits for R2 (Held by b). |
| 7 | b requests R1 | **Option 5** -> `b`, `R1`, `1` | **Blocked**. b waits for R1 (Held by a). **DEADLOCK**. |
| 8 | Run Detection | **Option 9** | "Deadlock DETECTED! Processes involved: ['a', 'b']" |
| 9 | Run Recovery | **Option 11** | System selects **b** (Priority 5 is lower than 1).<br>b is Terminated.<br>Resources released.<br>a gets R2 and becomes Ready. |
| 10 | Verify | **Option 2** | a is Ready. b is Terminated. |

---

## 6. Edge Case Test Cases

| ID | Test Case | Input | Expected Result |
| :--- | :--- | :--- | :--- |
| **EC-01** | Non-existing PID | Request resource for `p99` | "Error: Process p99 not found." |
| **EC-02** | Release unheld resource | Release `R1` from `p1` (holding nothing) | "Error: Process p1 does not hold..." |
| **EC-03** | Request > Max Need | Request `R1:100` (Max is 5) | "Error: Max need exceeded" or "Available exceeded" (depending on check logic). |
| **EC-04** | Detection w/o Processes| Option 9 when no processes exist | "No active processes to check." |
| **EC-05** | Scheduler w/o Processes| Option 3 when no processes exist | "No processes to schedule." |
| **EC-06** | Duplicate PID | Create `p1` again | "Error: Process with PID p1 already exists." |
| **EC-07** | Zero Quantum | Round Robin with Quantum `0` | "Quantum must be greater than 0." |
| **EC-08** | Recovery when no deadlock exists | Option 11 when no deadlock is present | A clear message indicating that there is no deadlock to recover. |
| **EC-09** | Set Max Need before configuring resources | Option 8 before configuring resources using option 4 | A clear error message indicating that resources are not yet configured. |

---

## 7. Negative / Validation Test Cases

| ID | Test Case | Input | Expected Result |
| :--- | :--- | :--- | :--- |
| **VAL-01** | Invalid Menu Option | Select `99`, `abc` | "Invalid option" or "Invalid input". |
| **VAL-02** | Negative Amount | Request `R1: -5` | "Please enter a non-negative integer." |
| **VAL-03** | Empty PID | Create process with empty PID | "PID cannot be empty." |
| **VAL-04** | Invalid Resource Format| Configure `R1-5` or `R1` | "Invalid format. Please use Type:Count..." |
| **VAL-05** | Invalid Resource Type | Request `Z99` | "Error: Resource Z99 does not exist." |

---

## 8. Notes for Evaluator
1. **Simulation Constraints:** This is a user-space simulation. It does not interface with the actual OS kernel or hardware.
2. **Scheduling Side-Effects:** The specific scheduling algorithms (FCFS, RR) run to completion (simulated time) and set process states to `Terminated`. To test deadlock or resource management after a scheduling run, you must recreate the processes.
3. **Deadlock Logic:** Detection is based on the current state of Allocation and Request matrices. It logically detects cycles but does not automatically resolve them unless 'Recovery' is explicitly invoked.
4. **Priority logic:** Lower integer value = Higher Priority. Recovery targets the *Highest* integer value (Lowest Priority).
5. **Deadlock Detection Algorithm:** Deadlock detection uses the standard matrix-based detection algorithm based on Available, Allocation and Request matrices.
