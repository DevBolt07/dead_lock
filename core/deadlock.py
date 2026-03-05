class DeadlockManager:
    """
    Handles Deadlock Detection, Avoidance (Banker's Algorithm), and Recovery.
    """
    def __init__(self, process_manager, resource_manager):
        self.pm = process_manager
        self.rm = resource_manager

    def detect_deadlock(self):
        """
        Detects deadlock using the standard detection algorithm for multiple resource instances.
        Returns a list of deadlocked process PIDs.
        """
        processes = [p for p in self.pm.get_all_processes() if p.state != "Terminated"]
        if not processes:
            print("No active processes to check.")
            return []

        # 1. Initialize Work and Finish
        work = self.rm.available.copy()
        finish = {p.pid: False for p in processes}
        
        # processes with no allocation are treated as finished?
        # Actually in detection algorithm, if Allocation != 0, finish=False. 
        # If Allocation == 0, finish=True? No, if it has Request it might be stuck?
        # Standard algo: Finish[i] = False.
        # But if Allocation[i] is all 0, strictly speaking it can't hold up others, 
        # but if it has a request, it might never finish if availability is low.
        # Standard: Finish[i] = False.
        
        # Wait, if a process has no edges in WFG (no allocation, no request), it's not involved.
        # But let's stick to the algo:
        # Find i such that Finish[i] == False and Request[i] <= Work
        
        print("\n--- Running Deadlock Detection ---")
        
        while True:
            progress_made = False
            for p in processes:
                pid = p.pid
                if finish[pid]:
                    continue
                
                # Check if Request <= Work
                # process.request might act as the Request matrix
                req_vector = p.request if hasattr(p, 'request') else {}
                can_proceed = True
                
                for r in self.rm.resources:
                    needed = req_vector.get(r, 0)
                    if needed > work.get(r, 0):
                        can_proceed = False
                        break
                
                if can_proceed:
                    # Grant resources (conceptually), process finishes, return allocated to Work
                    # work += allocation
                    alloc_vector = p.allocation if hasattr(p, 'allocation') else {}
                    for r, val in alloc_vector.items():
                        work[r] = work.get(r, 0) + val
                    
                    finish[pid] = True
                    progress_made = True
            
            if not progress_made:
                break
                
        deadlocked_pids = [pid for pid, done in finish.items() if not done]
        
        if deadlocked_pids:
            print(f"Deadlock DETECTED! Processes involved: {deadlocked_pids}")
        else:
            print("System is SAFE. No deadlock detected.")
            
        return deadlocked_pids

    def check_safety_for_request(self, pid, resource, amount):
        """
        Simulate the request and check if the resulting state is Safe (Banker's Algorithm).
        Returns True if Safe, False otherwise.
        """
        print(f"\n[Banker's] Checking safety for hypothetical allocation: {pid} requests {amount} of {resource}...")

        if resource not in self.rm.resources:
            return {"safe": False, "msg": "Invalid resource type.", "sequence": []}
        
        # 0. Check basic validity (already done in RM but good to double check)
        if self.rm.available.get(resource, 0) < amount:
            return {"safe": False, "msg": "Resources not currently available.", "sequence": []}

        # 1. Temporarily allocate
        # We need deep copies to simulate without affecting real state
        temp_avail = self.rm.available.copy()
        temp_alloc = {p.pid: p.allocation.copy() for p in self.pm.get_all_processes()}
        
        # Since 'max_need' is static, correct 'need' = max_need - allocation
        # temp_need is calculated dynamically
        
        # Apply the hypothetical change
        temp_avail[resource] -= amount
        if pid not in temp_alloc: temp_alloc[pid] = {}
        temp_alloc[pid][resource] = temp_alloc[pid].get(resource, 0) + amount
        
        # 2. Run Safety Algorithm
        processes = [p for p in self.pm.get_all_processes() if p.state != "Terminated"]
        work = temp_avail.copy()
        finish = {p.pid: False for p in processes}
        
        safety_sequence = []
        
        while True:
            progress_made = False
            for p in processes:
                if finish[p.pid]:
                    continue
                
                # Check Need <= Work
                # Need = Max - Alloc
                can_proceed = True
                for r in self.rm.resources:
                    alloc_val = temp_alloc[p.pid].get(r, 0)
                    max_val = p.max_need.get(r, 0)
                    need_val = max_val - alloc_val
                    
                    # Banker's specific: If need < 0, implies Alloc > Max (Error state, theoretically shouldn't happen)
                    if need_val < 0: 
                        # This might happen if user didn't set Max correctly or over-allocated.
                        # We assume Max >= Alloc.
                        pass
                        
                    if need_val > work.get(r, 0):
                        can_proceed = False
                        break
                
                if can_proceed:
                    # Process can finish, return Alloc to Work
                    for r, val in temp_alloc[p.pid].items():
                        work[r] = work.get(r, 0) + val
                    finish[p.pid] = True
                    safety_sequence.append(p.pid)
                    progress_made = True
            
            if not progress_made:
                break
                
        if all(finish.values()):
            return {"safe": True, "msg": "Safe State confirmed.", "sequence": safety_sequence}
        else:
            return {"safe": False, "msg": "Unsafe State! Granting request would lead to possible deadlock.", "sequence": []}

    def resolve_deadlock(self):
        """
        Recover from deadlock by terminating the lowest priority process involved.
        """
        log = []
        deadlocked = self.detect_deadlock()
        if not deadlocked:
            return ["No deadlock detected."]
            
        log.append("--- Deadlock Recovery ---")
        # Strategy: Terminate Lowest Priority
        # Lower number = Higher priority. So Highest number = Lowest priority.
        
        victim = None
        highest_prio_val = -1
        
        for pid in deadlocked:
            p = self.pm.get_process(pid)
            if p.priority > highest_prio_val:
                highest_prio_val = p.priority
                victim = p
            elif p.priority == highest_prio_val:
                # Tie-breaker? PID?
                pass
                
        if victim:
            log.append(f"Selected Victim: Process {victim.pid} (Priority {victim.priority}). Terminating...")
            
            self.rm.release_all_resources(victim.pid)
            self.pm.terminate_process(victim.pid)
            
            log.append("Victim terminated. Checking system status again...")
            # Recursive check?
            remaining = self.detect_deadlock()
            if remaining:
                log.append("Deadlock persists. Resolving again...")
                log.extend(self.resolve_deadlock())
            else:
                log.append("Deadlock resolved!")
        else:
            log.append("Could not identify victim.")
            
        return log
