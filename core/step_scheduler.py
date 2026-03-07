from core.process import Process

class StepScheduler:
    def __init__(self, process_manager):
        self.pm = process_manager
        self.time = 0
        self.algo = None
        self.quantum = 2
        self.processes = []
        self.ready_queue = []
        self.running_process = None
        self.completed_processes = []
        self.quantum_time_left = 0

    def reset(self, algo, quantum=2):
        self.time = 0
        self.algo = algo
        self.quantum = quantum
        
        # Create deep copies of the processes so UI renders don't overwrite simulation state
        self.processes = []
        for p in self.pm.get_all_processes():
            new_p = Process(p.pid, p.burst_time, p.priority, p.arrival_time)
            new_p.remaining_time = p.burst_time
            new_p.state = "New"
            new_p.completion_time = 0
            new_p.turnaround_time = 0
            new_p.waiting_time = 0
            self.processes.append(new_p)
            
        self.ready_queue = []
        self.running_process = None
        self.completed_processes = []
        self.quantum_time_left = quantum

    def is_finished(self):
        return len(self.completed_processes) == len(self.processes)

    def step(self):
        if self.is_finished():
            return

        # 1. If running process is done, move to completed
        if self.running_process and self.running_process.remaining_time == 0:
            self.running_process.state = "Terminated"
            self.running_process.completion_time = self.time
            self.running_process.turnaround_time = self.running_process.completion_time - self.running_process.arrival_time
            self.running_process.waiting_time = self.running_process.turnaround_time - self.running_process.burst_time
            
            self.completed_processes.append(self.running_process)
            self.running_process = None

        # 2. Check for newly arriving processes
        for p in self.processes:
            if p.arrival_time == self.time and p.state == "New":
                p.state = "Ready"
                self.ready_queue.append(p)

        # 3. Check for round robin quantum expiration
        if self.algo == "Round Robin" and self.running_process:
            if self.quantum_time_left == 0:
                self.running_process.state = "Ready"
                self.ready_queue.append(self.running_process)
                self.running_process = None

        # 4. If SRTF, we might preempt the running process
        if self.algo == "SRTF (Preemptive)" and self.running_process:
            best_candidate = min(self.ready_queue, key=lambda x: (x.remaining_time, x.arrival_time), default=None)
            if best_candidate and best_candidate.remaining_time < self.running_process.remaining_time:
                self.running_process.state = "Ready"
                self.ready_queue.append(self.running_process)
                self.running_process = None

        # 5. Select process if CPU is idle
        if not self.running_process and self.ready_queue:
            if self.algo == "FCFS":
                self.ready_queue.sort(key=lambda x: x.arrival_time)
                self.running_process = self.ready_queue.pop(0)
            elif self.algo == "SJF (Non-preemptive)":
                self.ready_queue.sort(key=lambda x: (x.burst_time, x.arrival_time))
                self.running_process = self.ready_queue.pop(0)
            elif self.algo == "SRTF (Preemptive)":
                self.ready_queue.sort(key=lambda x: (x.remaining_time, x.arrival_time))
                self.running_process = self.ready_queue.pop(0)
            elif self.algo == "Priority Scheduling":
                self.ready_queue.sort(key=lambda x: (x.priority, x.arrival_time))
                self.running_process = self.ready_queue.pop(0)
            elif self.algo == "Round Robin":
                self.running_process = self.ready_queue.pop(0)
                self.quantum_time_left = self.quantum

        # 6. Execute CPU for 1 time unit
        if self.running_process:
            self.running_process.state = "Running"
            self.running_process.remaining_time -= 1
            if self.algo == "Round Robin":
                self.quantum_time_left -= 1
        
        self.time += 1
