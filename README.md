# Smart Process & Deadlock Manager

## Project Overview
This project is a CLI-based simulation of an Operating System's core components: Process Management, CPU Scheduling, Resource Allocation, and Deadlock Management. It is implemented in Python and designed for academic purposes to demonstrate OS concepts without kernel-level complexity.

## Features & Phases

### Phase 1: Process Management
- **PCB Simulation**: processes have PID, State, Burst Time, Priority, Arrival Time.
- **Process States**: Ready, Running, Waiting, Terminated.
- **Creation**: Users can create processes dynamically.

### Phase 2: CPU Scheduling
- **FCFS**: First-Come-First-Serve scheduling based on Arrival Time.
- **Priority**: Non-preemptive priority scheduling (Lower number = Higher priority).
- **Round Robin**: Time-quantum based preemptive scheduling.
- **Metrics**: Calculates Waiting Time and Turnaround Time.

### Phase 3: Resource Management
- **Resource Types**: Supports multiple resource types (e.g., R1, R2).
- **Allocation & Request**: Tracks resources using Allocation and Request matrices.
- **Blocking**: Processes are blocked (Waiting state) if resources are unavailable.

### Phase 4: Deadlock Detection
- **Detection Algorithm**: Implements the standard detection algorithm for multiple resource instances (Available, Allocation, Request).
- **Reporting**: Identifies and lists deadlocked processes.

### Phase 5: Deadlock Avoidance
- **Banker's Algorithm**: Checks for Safe State before granting resource requests (simulated mode).
- **Safety Check**: Ensures system never enters an unsafe state if enabled.

### Phase 6: Deadlock Recovery
- **Recovery Strategy**: Terminates the lowest-priority process involved in a deadlock to break the cycle.
- **Resource Release**: Automatically releases resources of the terminated process and unblocks waiting processes.

## How to Run
1. Ensure Python 3.x is installed.
2. Run the main program:
   ```bash
   python main.py
   ```
3. Follow the menu prompts to creating processes, schedule them, or manage resources/deadlocks.

## Demo Mode
To simplify presentations, the system includes a Demo Mode option (Option 13) in the main menu. 
- **What it does**: It auto-loads a predefined set of processes and resource configurations.
- **Usefulness**: This allows for quick setup and is highly useful for academic presentation or rapid testing without manually typing inputs.

## OS Concepts Demonstrated
- **Context Switching**: Simulated by saving/loading process states in Scheduler.
- **Queuing**: Ready Queue (Scheduler) and Waiting Queue (Resource Manager).
- **Mutual Exclusion & Hold-and-Wait**: Demonstrated via Resource Manager blocking.
- **Circular Wait**: Demonstrated in Deadlock Detection.
- **Starvation**: Can be observed in Priority Scheduling with low-priority processes.

## Possible Extensions
1. **GUI Visualization**: Implement a graphical interface using Tkinter or PyQt to visualize the Gantt chart and Resource Graph.
2. **Memory Management**: Add contiguous memory allocation (First-Fit, Best-Fit) simulation.
3. **File System**: Simulate a simple hierarchical file system with permissions.
4. **Multi-level Feedback Queue**: Implement a more advanced scheduler with aging to prevent starvation.
5. **Thread Simulation**: Extend Process to support multiple threads sharing the same PCB resources.
