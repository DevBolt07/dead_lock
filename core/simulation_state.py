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
        """Loads predefined dataset for presentation purposes."""
        self.reset_system()
        
        # Automatically create processes
        self.process_manager.create_process("p1", 8, 3, 0)
        self.process_manager.create_process("p2", 4, 1, 1)
        self.process_manager.create_process("p3", 6, 2, 2)
        self.process_manager.create_process("p4", 3, 4, 3)
        
        # Configure resources
        self.resource_manager.initialize_resources({"R1": 6, "R2": 4})
        
        # Set Max Need
        self.resource_manager.set_max_need("p1", {"R1": 3, "R2": 2})
        self.resource_manager.set_max_need("p2", {"R1": 2, "R2": 1})
        self.resource_manager.set_max_need("p3", {"R1": 3, "R2": 2})
        self.resource_manager.set_max_need("p4", {"R1": 2, "R2": 1})
        
        return True
