from core.process import Process
import copy

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
        self.timeline = []
        self.event_log = []
        self.history = []

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
            new_p.response_time = -1
            self.processes.append(new_p)
            
        self.ready_queue = []
        self.running_process = None
        self.completed_processes = []
        self.quantum_time_left = quantum
        self.timeline = []
        self.event_log = []
        self.history = []

    def is_finished(self):
        return len(self.completed_processes) == len(self.processes)

    def add_event(self, message):
        self.event_log.append(f"t = {self.time} : {message}")
        if len(self.event_log) > 5:
            self.event_log.pop(0)

    @property
    def job_queue(self):
        return [p for p in self.processes if p.state == "New" and p.arrival_time > self.time]

    def step(self):
        if self.is_finished():
            return

        # Snapshot the current state before we augment anything
        # We must deepcopy the object graph together to preserve identical references 
        # between processes, ready_queue, and running_process.
        refs = copy.deepcopy({
            "processes": self.processes,
            "ready_queue": self.ready_queue,
            "running_process": self.running_process,
            "completed_processes": self.completed_processes
        })
        
        snapshot = {
            "time": self.time,
            "quantum_time_left": self.quantum_time_left,
            "timeline": copy.deepcopy(self.timeline),
            "event_log": copy.deepcopy(self.event_log),
            **refs
        }
        self.history.append(snapshot)

        # 1. If running process is done, move to completed
        if self.running_process and self.running_process.remaining_time == 0:
            self.running_process.state = "Terminated"
            self.running_process.completion_time = self.time
            self.running_process.turnaround_time = self.running_process.completion_time - self.running_process.arrival_time
            self.running_process.waiting_time = self.running_process.turnaround_time - self.running_process.burst_time
            
            # Safeguard: Remove from ready queue if it was somehow there
            self.ready_queue = [x for x in self.ready_queue if x.pid != self.running_process.pid]
            
            if not any(x.pid == self.running_process.pid for x in self.completed_processes):
                self.completed_processes.append(self.running_process)
            self.add_event(f"p{self.running_process.pid} completed -> Completed")
            self.running_process = None

        # 2. Check for newly arriving processes
        for p in self.processes:
            if p.arrival_time == self.time and p.state == "New":
                p.state = "Ready"
                # Safeguard: Remove it from ready_queue if it was already there
                self.ready_queue = [x for x in self.ready_queue if x.pid != p.pid]
                self.ready_queue.append(p)
                self.add_event(f"p{p.pid} arrived -> Ready Queue")

        # 3. Check for round robin quantum expiration
        if self.algo == "Round Robin" and self.running_process:
            if self.quantum_time_left == 0:
                self.running_process.state = "Ready"
                # Safeguard: Extra remove before append
                self.ready_queue = [x for x in self.ready_queue if x.pid != self.running_process.pid]
                self.ready_queue.append(self.running_process)
                self.add_event(f"Quantum expired for p{self.running_process.pid} -> Ready")
                self.running_process = None

        # 4. If SRTF, we might preempt the running process
        if self.algo == "SRTF (Preemptive)" and self.running_process:
            best_candidate = min(self.ready_queue, key=lambda x: (x.remaining_time, x.arrival_time), default=None)
            if best_candidate and best_candidate.remaining_time < self.running_process.remaining_time:
                self.running_process.state = "Ready"
                # Safeguard: Extra remove before append
                self.ready_queue = [x for x in self.ready_queue if x.pid != self.running_process.pid]
                self.ready_queue.append(self.running_process)
                self.add_event(f"p{self.running_process.pid} preempted by p{best_candidate.pid} -> Ready")
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
                
            # Extra safeguard: Ensure it doesn't linger in ready queue
            self.ready_queue = [x for x in self.ready_queue if x.pid != self.running_process.pid]

        # 6. Execute CPU for 1 time unit
        if self.running_process:
            # Calculate response time on first run
            if getattr(self.running_process, "response_time", -1) == -1:
                self.running_process.response_time = self.time - self.running_process.arrival_time

            if self.running_process.state == "Ready":
                self.add_event(f"p{self.running_process.pid} moved Ready -> CPU")
            self.running_process.state = "Running"
            self.running_process.remaining_time -= 1
            if self.algo == "Round Robin":
                self.quantum_time_left -= 1
            self.timeline.append(str(self.running_process.pid))
        else:
            self.timeline.append("Idle")
        
        self.time += 1

    def step_back(self):
        if not self.history:
            return
            
        # Pop the last snapshot entirely
        snapshot = self.history.pop()
        
        # Restore full memory
        self.time = snapshot["time"]
        self.processes = snapshot["processes"]
        self.ready_queue = snapshot["ready_queue"]
        self.running_process = snapshot["running_process"]
        self.completed_processes = snapshot["completed_processes"]
        self.quantum_time_left = snapshot["quantum_time_left"]
        self.timeline = snapshot["timeline"]
        self.event_log = snapshot["event_log"]
