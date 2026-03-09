class Process:
    """
    Process Control Block (PCB) Simulation
    Holds all information related to a process.
    """
    def __init__(self, pid, burst_time, priority, arrival_time=0):
        self.pid = pid
        self.burst_time = burst_time
        self.priority = priority
        self.arrival_time = arrival_time
        self.state = "Ready"
        
        # Scheduling metrics
        self.remaining_time = burst_time
        self.waiting_time = 0
        self.turnaround_time = 0
        self.completion_time = 0
        
        # Resource Management (for later phases)
        self.allocation = {}      # Resources currently held
        self.max_need = {}        # Max resources needed (for Banker's)
        self.request = {}         # Current resource request

    def __str__(self):
        return f"PID: {self.pid} | State: {self.state} | Priority: {self.priority} | Arrival: {self.arrival_time}"

class ProcessManager:
    """
    Manages the lifecycle and storage of processes.
    """
    def __init__(self):
        self.processes = []
        
    def create_process(self, pid, burst_time, priority, arrival_time):
        """Creates a new process and adds it to the list."""
        if any(p.pid == pid for p in self.processes):
            return False
            
        new_process = Process(pid, burst_time, priority, arrival_time)
        self.processes.append(new_process)
        return True

    def get_process(self, pid):
        """Retrieves a process by PID."""
        for p in self.processes:
            if p.pid == pid:
                return p
        return None

    def get_all_processes(self):
        """Returns list of all processes."""
        return self.processes

    def terminate_process(self, pid):
        """Terminates a process."""
        p = self.get_process(pid)
        if p:
            p.state = "Terminated"
            return True
        return False
