class Scheduler:
    """
    Handles CPU scheduling algorithms: FCFS, Priority (Non-Preemptive), Round Robin.
    """
    def __init__(self, process_manager):
        self.pm = process_manager

    def reset_metrics(self, processes):
        """Resets scheduling metrics for a fresh run."""
        for p in processes:
            p.waiting_time = 0
            p.turnaround_time = 0
            p.completion_time = 0
            p.remaining_time = p.burst_time
            p.state = "Ready"

    def print_schedule_result(self, processes, execution_order, gantt_data=None):
        """Prints the scheduling results: Execution Order, Waiting Time, Turnaround Time."""
        print("\nExecution Order:")
        print(" -> ".join(execution_order))

        if gantt_data:
            print("\nGantt Chart")
            top_row = "|"
            for item in gantt_data:
                pid = item[0]
                top_row += f" {pid} |"
            print(top_row)
            
            bottom_row = str(gantt_data[0][1])
            for item in gantt_data:
                pid, start, end = item
                width = len(f" {pid} |")
                bottom_row += str(end).rjust(width)
            print(bottom_row)
        
        print("\nProcess Metrics:")
        print(f"{'PID':<10} {'Burst':<10} {'Arrival':<10} {'Priority':<10} {'Finish':<10} {'Turnaround':<12} {'Waiting':<10}")
        print("-" * 75)
        
        total_tat = 0
        total_wt = 0
        
        # Sort by PID for cleaner output, or by finish time? usually by PID is easier to read
        # But we must ensure 'processes' has the updated values. It should since they are references.
        
        for p in sorted(processes, key=lambda x: x.pid):
            print(f"{p.pid:<10} {p.burst_time:<10} {p.arrival_time:<10} {p.priority:<10} {p.completion_time:<10} {p.turnaround_time:<12} {p.waiting_time:<10}")
            total_tat += p.turnaround_time
            total_wt += p.waiting_time
            
        n = len(processes)
        if n > 0:
            print("-" * 75)
            print(f"Average Turnaround Time: {total_tat / n:.2f}")
            print(f"Average Waiting Time:    {total_wt / n:.2f}")

    def run_fcfs(self):
        print("\n--- Running FCFS Scheduling ---")
        processes = [p for p in self.pm.get_all_processes()]
        if not processes:
            print("No processes to schedule.")
            return

        self.reset_metrics(processes)
        
        # Sort by Arrival Time
        processes.sort(key=lambda x: x.arrival_time)
        
        current_time = 0
        execution_order = []
        gantt_data = []
        
        for p in processes:
            if current_time < p.arrival_time:
                gantt_data.append(("IDLE", current_time, p.arrival_time))
                current_time = p.arrival_time
            
            p.state = "Running"
            execution_order.append(p.pid)
            start_time = current_time
            
            # Non-preemptive, runs to completion
            current_time += p.burst_time
            gantt_data.append((p.pid, start_time, current_time))
            
            p.completion_time = current_time
            p.turnaround_time = p.completion_time - p.arrival_time
            p.waiting_time = p.turnaround_time - p.burst_time
            p.state = "Terminated"
            
        self.print_schedule_result(processes, execution_order, gantt_data)

    def run_priority(self):
        # Non-preemptive Priority
        print("\n--- Running Priority Scheduling (Non-Preemptive) ---")
        processes = [p for p in self.pm.get_all_processes()]
        if not processes:
            print("No processes to schedule.")
            return

        self.reset_metrics(processes)
        
        # Current time starts at 0 or first arrival?
        # Standard Algorithm:
        # 1. At current_time, select process with highest priority (lowest number) from those arrived.
        # 2. If no process active, jump to next arrival.
        
        completed = 0
        n = len(processes)
        current_time = 0
        execution_order = []
        gantt_data = []
        
        # We need to keep track of completed processes to avoid re-running them
        # Using a set of PIDs is safer
        completed_pids = set()
        
        while completed < n:
            # Find available processes
            available = [p for p in processes if p.arrival_time <= current_time and p.pid not in completed_pids]
            
            if not available:
                # No process available, jump time
                # Find the next arrival time
                pending = [p for p in processes if p.pid not in completed_pids]
                if pending:
                    # Jump to the earliest arrival time among pending
                    next_arrival = min(p.arrival_time for p in pending)
                    gantt_data.append(("IDLE", current_time, next_arrival))
                    current_time = next_arrival
                    continue
                else:
                    break # Should not happen if completed < n
            
            # Select highest priority (lowest value)
            # If tie, use FCFS (Arrival Time)
            # Python's list sort is stable, or we can use tuple key
            available.sort(key=lambda x: (x.priority, x.arrival_time))
            p = available[0]
            
            p.state = "Running"
            execution_order.append(p.pid)
            start_time = current_time
            
            current_time += p.burst_time
            gantt_data.append((p.pid, start_time, current_time))
            
            p.completion_time = current_time
            p.turnaround_time = p.completion_time - p.arrival_time
            p.waiting_time = p.turnaround_time - p.burst_time
            p.state = "Terminated"
            
            completed_pids.add(p.pid)
            completed += 1
            
        self.print_schedule_result(processes, execution_order, gantt_data)

    def run_round_robin(self, quantum):
        print(f"\n--- Running Round Robin Scheduling (Quantum={quantum}) ---")
        processes = [p for p in self.pm.get_all_processes()] # Copy list
        if not processes:
            print("No processes to schedule.")
            return

        self.reset_metrics(processes)
        
        # For RR, we need a queue
        # Sort initially by arrival time to populate queue
        processes.sort(key=lambda x: x.arrival_time)
        
        queue = []
        current_time = 0
        execution_order = []
        gantt_data = []
        
        # Helper to track which processes are already in queue or completed
        # Actually in RR, we just pop from queue and push back if not done.
        # BUT we must add NEWLY ARRIVED processes to the queue before pushing back the current one?
        # Standard RR: 
        # 1. Execute current for min(quantum, remaining)
        # 2. current_time += executed_time
        # 3. Add any new arrivals [completed_time_prev, current_time] to queue
        # 4. If current not done, add to queue
        
        # Initial population
        # We need to be careful. 'processes' list has all.
        # Let's use an index to track which processes from 'processes' list have been added to queue
        
        n = len(processes)
        added_count = 0
        completed = 0
        
        # Add first process(es)
        if processes[0].arrival_time > 0:
            gantt_data.append(("IDLE", current_time, processes[0].arrival_time))
            current_time = processes[0].arrival_time
            
        while added_count < n and processes[added_count].arrival_time <= current_time:
            queue.append(processes[added_count])
            added_count += 1
            
        while completed < n:
            if not queue:
                # Jump to next arrival
                if added_count < n:
                    gantt_data.append(("IDLE", current_time, processes[added_count].arrival_time))
                    current_time = processes[added_count].arrival_time
                    while added_count < n and processes[added_count].arrival_time <= current_time:
                        queue.append(processes[added_count])
                        added_count += 1
                else:
                    break # Should not happen
            
            p = queue.pop(0)
            
            execute_time = min(quantum, p.remaining_time)
            p.state = "Running"
            execution_order.append(p.pid)
            start_time = current_time
            
            current_time += execute_time
            gantt_data.append((p.pid, start_time, current_time))
            
            p.remaining_time -= execute_time
            
            # Check for new arrivals during this time slice
            while added_count < n and processes[added_count].arrival_time <= current_time:
                queue.append(processes[added_count])
                added_count += 1
                
            if p.remaining_time > 0:
                p.state = "Ready"
                queue.append(p)
            else:
                p.state = "Terminated"
                p.completion_time = current_time
                p.turnaround_time = p.completion_time - p.arrival_time
                p.waiting_time = p.turnaround_time - p.burst_time
                completed += 1
                
        self.print_schedule_result(processes, execution_order, gantt_data)
