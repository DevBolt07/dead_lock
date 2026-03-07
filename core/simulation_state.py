import random
from core.process import ProcessManager
from core.scheduler import Scheduler
from core.resource import ResourceManager
from core.deadlock import DeadlockManager

class SimulationState:
    def __init__(self):
        self.process_manager = ProcessManager()
        self.scheduler = Scheduler(self.process_manager)
        self.resource_manager = ResourceManager(self.process_manager)
        self.deadlock_manager = DeadlockManager(self.process_manager, self.resource_manager)
        
    def reset_system(self):
        """Resets system state for demo mode."""
        self.process_manager.processes.clear()
        self.resource_manager.resources.clear()
        self.resource_manager.available.clear()
        self.resource_manager.allocation.clear()
        self.resource_manager.request.clear()

    def load_demo_data(self):
        """Loads randomized predefined dataset for educational purposes."""
        self.reset_system()
        
        # Decide between 4 to 5 processes
        num_processes = random.choice([4, 5])
        
        arrival_choices = list(range(1, 7)) # 1 to 6
        burst_choices = list(range(2, 11))  # 2 to 10
        priority_choices = list(range(1, 6)) # 1 to 5
        
        # Force at least one process to arrive at time 0
        p1_burst = random.choice(burst_choices)
        p1_priority = random.choice(priority_choices)
        self.process_manager.create_process("p1", p1_burst, p1_priority, 0)
        
        used_arrivals = [0]
        
        for i in range(2, num_processes + 1):
            pid = f"p{i}"
            
            # Avoid all arriving at same time; prefer staggered
            at = random.choice(arrival_choices)
            # Bias slightly to unique arrival times to show Ready Queue better
            if at in used_arrivals and random.random() < 0.5:
                at = random.choice([a for a in arrival_choices if a not in used_arrivals] or arrival_choices)
            
            used_arrivals.append(at)
            bt = random.choice(burst_choices)
            pr = random.choice(priority_choices)
            
            self.process_manager.create_process(pid, bt, pr, at)
            
        # Configure standard resources for Deadlock demo backward compatibility
        self.resource_manager.initialize_resources({"R1": 6, "R2": 4})
        
        # Set dummy Max Needs for however many processes were generated
        for i in range(1, num_processes + 1):
            pid = f"p{i}"
            self.resource_manager.set_max_need(pid, {
                "R1": random.randint(1, 4), 
                "R2": random.randint(1, 3)
            })
            
        return True
