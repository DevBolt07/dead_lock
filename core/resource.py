class ResourceManager:
    """
    Manages system resources: Available vector, Allocation matrix, Request matrix.
    """
    def __init__(self, process_manager):
        self.pm = process_manager
        self.resources = {}       # Total instances of each resource type
        self.available = {}       # Current available instances
        self.allocation = {}      # dict[pid][resource] = amount
        self.request = {}         # dict[pid][resource] = amount (Process waiting for these)

    def initialize_resources(self, resource_dict):
        """
        Initializes the resources with total instances.
        resource_dict: {'R1': 10, 'R2': 5, ...}
        """
        self.resources = resource_dict.copy()
        self.available = resource_dict.copy()
        self.allocation = {}
        self.request = {}
        print("Resources initialized:", self.available)

    def get_process_allocation(self, pid):
        if pid not in self.allocation:
            self.allocation[pid] = {r: 0 for r in self.resources}
        return self.allocation[pid]

    def request_resource(self, pid, resource_type, amount):
        """
        Handles a resource request from a process.
        """
        process = self.pm.get_process(pid)
        if not process:
            print(f"Error: Process {pid} not found.")
            return False

        if resource_type not in self.resources:
            print("Error: Invalid resource type.")
            return False

        if amount <= 0:
            print("Error: Request amount must be positive.")
            return False

        current_alloc = self.get_process_allocation(pid)
        
        # Check Max Need
        if process.max_need:
            current_val = current_alloc.get(resource_type, 0)
            max_val = process.max_need.get(resource_type, 0)
            if max_val > 0 and (current_val + amount) > max_val:
                print("Error: Request exceeds maximum declared need.")
                return False
        
        # Check if request is valid (conceptually, valid if it doesn't exceed max need, 
        # but we don't have Max Need enforced yet in Phase 3, just basic allocation)
        
        print(f"Process {pid} requesting {amount} instances of {resource_type}...")

        if self.available[resource_type] >= amount:
            # Grant immediately
            self.available[resource_type] -= amount
            current_alloc[resource_type] += amount
            
            # Ensure process is Allocating in its own record too (optional but good for consistency)
            if resource_type not in process.allocation:
                process.allocation[resource_type] = 0
            process.allocation[resource_type] += amount
            
            print(f"Request granted. {pid} allocated {amount} of {resource_type}.")
            return True
        else:
            # Block the process
            print(f"Resources not available. Process {pid} blocked (Waiting).")
            process.state = "Waiting"
            
            if pid not in self.request:
                self.request[pid] = {r: 0 for r in self.resources}
            self.request[pid][resource_type] += amount
            
            # Update process internal request tracking
            if resource_type not in process.request:
                process.request[resource_type] = 0
            process.request[resource_type] += amount
            
            return False

    def release_resource(self, pid, resource_type, amount):
        """
        Releases resources held by a process.
        """
        process = self.pm.get_process(pid)
        if not process:
            print(f"Error: Process {pid} not found.")
            return False

        if resource_type not in self.resources:
            print("Error: Invalid resource type.")
            return False

        if pid not in self.allocation or self.allocation[pid][resource_type] < amount:
            print(f"Error: Process {pid} does not hold {amount} instances of {resource_type}.")
            return False

        # Release
        self.available[resource_type] += amount
        self.allocation[pid][resource_type] -= amount
        
        # Update process internal
        process.allocation[resource_type] -= amount
        
        print(f"Process {pid} released {amount} of {resource_type}.")
        print(f"Available resources: {self.available}")
        
        # Check if any waiting process can be unblocked
        self.check_waiting_processes()
        return True

    def check_waiting_processes(self):
        """
        Checks if any waiting process can have its request satisfied.
        FIFO check (simple approach).
        """
        # Iterate over processes that have requests
        # Note: This is a simple check. It doesn't modify state unless fully satisfied?
        # A process might be waiting for multiple resources. 
        # For simplicity, we assume one request at a time or we check if ALL requests can be met?
        # The 'request' matrix stores outstanding requests.
        
        for pid, reqs in list(self.request.items()):
            process = self.pm.get_process(pid)
            if not process or process.state != "Waiting":
                continue
                
            # Check if ALL requests for this process can be satisfied
            can_satisfy = True
            for r, amt in reqs.items():
                if amt > 0 and self.available.get(r, 0) < amt:
                    can_satisfy = False
                    break
            
            if can_satisfy:
                # Grant all requests
                print(f"Resources became available for {pid}. Allocating...")
                for r, amt in reqs.items():
                    if amt > 0:
                        self.available[r] -= amt
                        self.allocation[pid][r] += amt
                        process.allocation[r] = self.allocation[pid][r] # Sync
                        reqs[r] = 0 # Request satisfied
                        process.request[r] = 0
                
                # Update State
                process.state = "Ready" 
                # Why Ready? Because it has resources now and can be scheduled.
                # Or Running? Usually Ready.
                print(f"Process {pid} is now Ready.")
                
                # Cleanup request entry if empty
                # self.request[pid] should be cleared? 
                # We updated values to 0.

    def set_max_need(self, pid, max_need):
        """Sets the maximum resource need for a process (used for Banker's Algorithm)."""
        process = self.pm.get_process(pid)
        if not process:
            print(f"Error: Process {pid} not found.")
            return False
            
        # Validate keys
        for r, amt in max_need.items():
            if r not in self.resources:
                print(f"Error: Resource {r} does not exist.")
                return False
            if amt > self.resources[r]:
                print(f"Error: Max need {amt} exceeds total system capacity for {r}.")
                return False

        process.max_need = max_need
        print(f"Max need set for Process {pid}: {max_need}")
        return True

    def release_all_resources(self, pid):
        """Releases ALL resources held by a process (used for Process Termination)."""
        process = self.pm.get_process(pid)
        if not process:
            return False
            
        print(f"Releasing all resources for {pid}...")
        # Make a copy of keys as we modify allocation in loop
        allocated_resources = list(process.allocation.items())
        
        for r, amount in allocated_resources:
            if amount > 0:
                self.release_resource(pid, r, amount)
        
        # Clear allocation and request just in case
        process.allocation = {}
        process.request = {}
        if pid in self.allocation:
            del self.allocation[pid]
        if pid in self.request:
            del self.request[pid]

        return True

    def display_resource_status(self):
        print("\n--- Resource Status ---")
        print(f"Available: {self.available}")
        print("\nAllocation Matrix:")
        print(f"{'PID':<10} " + " ".join([f"{r:<5}" for r in self.resources]))
        for pid, alloc in self.allocation.items():
            print(f"{pid:<10} " + " ".join([f"{alloc.get(r,0):<5}" for r in self.resources]))
            
        print("\nMax Need Matrix (Banker's):")
        print(f"{'PID':<10} " + " ".join([f"{r:<5}" for r in self.resources]))
        for p in self.pm.get_all_processes():
            if p.state != "Terminated":
                print(f"{p.pid:<10} " + " ".join([f"{p.max_need.get(r,0):<5}" for r in self.resources]))
        
        print("\nRequest Matrix:")
        print(f"{'PID':<10} " + " ".join([f"{r:<5}" for r in self.resources]))
        for pid, req in self.request.items():
            # Only show if there are actual requests?
            has_req = any(v > 0 for v in req.values())
            if has_req:
                print(f"{pid:<10} " + " ".join([f"{req.get(r,0):<5}" for r in self.resources]))
        print("-----------------------")
