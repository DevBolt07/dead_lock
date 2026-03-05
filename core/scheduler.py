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

    def get_schedule_result(self, processes, execution_order, gantt_data=None):
        total_tat = 0
        total_wt = 0
        metrics = []

        for p in sorted(processes, key=lambda x: x.pid):
            metrics.append({
                "PID": p.pid,
                "Burst": p.burst_time,
                "Arrival": p.arrival_time,
                "Priority": p.priority,
                "Finish": p.completion_time,
                "Turnaround": p.turnaround_time,
                "Waiting": p.waiting_time
            })
            total_tat += p.turnaround_time
            total_wt += p.waiting_time
            
        n = len(processes)
        avg_tat = total_tat / n if n > 0 else 0
        avg_wt = total_wt / n if n > 0 else 0

        formatted_gantt = []
        if gantt_data:
            for item in gantt_data:
                formatted_gantt.append({
                    "Process": item[0],
                    "Start": item[1],
                    "Finish": item[2]
                })

        return {
            "execution_order": execution_order,
            "gantt": formatted_gantt,
            "metrics": metrics,
            "avg_waiting": avg_wt,
            "avg_turnaround": avg_tat
        }

    def run_fcfs(self):
        processes = [p for p in self.pm.get_all_processes()]
        if not processes:
            return None

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
            
        return self.get_schedule_result(processes, execution_order, gantt_data)

    def run_priority(self):
        # Non-preemptive Priority
        processes = [p for p in self.pm.get_all_processes()]
        if not processes:
            return None

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
            
        return self.get_schedule_result(processes, execution_order, gantt_data)

    def run_round_robin(self, quantum):
        processes = [p for p in self.pm.get_all_processes()] # Copy list
        if not processes:
            return None

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
                
        return self.get_schedule_result(processes, execution_order, gantt_data)

    def run_sjf(self):
        # Non-preemptive Shortest Job First
        processes = [p for p in self.pm.get_all_processes()]
        if not processes:
            return None

        self.reset_metrics(processes)
        
        completed = 0
        n = len(processes)
        current_time = 0
        execution_order = []
        gantt_data = []
        
        completed_pids = set()
        
        while completed < n:
            available = [p for p in processes if p.arrival_time <= current_time and p.pid not in completed_pids]
            
            if not available:
                pending = [p for p in processes if p.pid not in completed_pids]
                if pending:
                    next_arrival = min(p.arrival_time for p in pending)
                    gantt_data.append(("IDLE", current_time, next_arrival))
                    current_time = next_arrival
                    continue
                else:
                    break
            
            # Select shortest burst time
            # If tie, use FCFS (Arrival Time)
            available.sort(key=lambda x: (x.burst_time, x.arrival_time))
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
            
        return self.get_schedule_result(processes, execution_order, gantt_data)

    def run_srtf(self):
        # Preemptive Shortest Remaining Time First
        processes = [p for p in self.pm.get_all_processes()]
        if not processes:
            return None

        self.reset_metrics(processes)
        
        completed = 0
        n = len(processes)
        current_time = 0
        execution_order = []
        gantt_data = []
        
        completed_pids = set()
        current_process = None
        burst_start_time = 0
        
        total_time_needed = sum(p.burst_time for p in processes)
        
        # We simulate time unit by unit, or jump to next event (arrival or completion)
        while completed < n:
            available = [p for p in processes if p.arrival_time <= current_time and p.pid not in completed_pids]
            
            if not available:
                pending = [p for p in processes if p.pid not in completed_pids]
                if pending:
                    next_arrival = min(p.arrival_time for p in pending)
                    gantt_data.append(("IDLE", current_time, next_arrival))
                    current_time = next_arrival
                    continue
                else:
                    break
                    
            available.sort(key=lambda x: (x.remaining_time, x.arrival_time))
            shortest = available[0]
            
            # Context switch logic
            if current_process != shortest:
                if current_process is not None and current_process.remaining_time > 0:
                    # Preempted
                    gantt_data.append((current_process.pid, burst_start_time, current_time))
                    current_process.state = "Ready"
                
                # New process takes CPU
                current_process = shortest
                burst_start_time = current_time
                if len(execution_order) == 0 or execution_order[-1] != current_process.pid:
                    execution_order.append(current_process.pid)
                current_process.state = "Running"
                
            # Execute for 1 time unit (or jump to next event)
            # Find next event time: either this physical process completes, or a new process arrives
            time_to_completion = current_process.remaining_time
            pending_arrivals = [p.arrival_time for p in processes if p.pid not in completed_pids and p.arrival_time > current_time]
            
            if pending_arrivals:
                next_event_time = min(current_time + time_to_completion, min(pending_arrivals))
            else:
                next_event_time = current_time + time_to_completion
                
            executed_time = next_event_time - current_time
            current_process.remaining_time -= executed_time
            current_time = next_event_time
            
            if current_process.remaining_time == 0:
                # Finished
                gantt_data.append((current_process.pid, burst_start_time, current_time))
                current_process.state = "Terminated"
                current_process.completion_time = current_time
                current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
                current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
                
                completed_pids.add(current_process.pid)
                completed += 1
                current_process = None
                
        return self.get_schedule_result(processes, execution_order, gantt_data)
