from process import ProcessManager
from resource import ResourceManager
from deadlock import DeadlockManager

def test_deadlock_scenario():
    print("\n=== Testing Deadlock Detection & Recovery ===")
    pm = ProcessManager()
    rm = ResourceManager(pm)
    dm = DeadlockManager(pm, rm)
    
    # 1. Setup Resources
    rm.initialize_resources({'R1': 1, 'R2': 1})
    
    # 2. Create Processes
    # P1: Priority 2 (Lower priority number = Higher priority? No, usually Lower number = Higher priority)
    # Prompt says: "lower number = higher priority" in 2.1 Process Management.
    # Recovery says: "terminate the lowest-priority process" 
    # Lowest priority process = Highest number.
    
    # P1 (Priority 1 - High), P2 (Priority 5 - Low)
    pm.create_process("P1", 10, 1, 0)
    pm.create_process("P2", 10, 5, 0)
    
    # 3. Create Deadlock
    # P1 gets R1
    rm.request_resource("P1", "R1", 1)
    # P2 gets R2
    rm.request_resource("P2", "R2", 1)
    
    # P1 requests R2 (Blocked)
    print("\n-- P1 requests R2 --")
    rm.request_resource("P1", "R2", 1)
    
    # P2 requests R1 (Blocked) -> DEADLOCK
    print("\n-- P2 requests R1 --")
    rm.request_resource("P2", "R1", 1)
    
    # 4. Detect
    print("\n-- Running Detection --")
    deadlocked = dm.detect_deadlock()
    assert "P1" in deadlocked and "P2" in deadlocked
    
    # 5. Recover
    print("\n-- Running Recovery --")
    # Should pick P2 (Priority 5, Lower priority than P1)
    dm.resolve_deadlock()
    
    # Verify P2 is terminated and P1 is unblocked?
    # Unblocking logic: when P2 resources released, P1 should get R1?
    # Wait, P2 held R2. P1 wanted R2. P2 released R2.
    # P1 should get R2.
    # Does 'release_all_resources' trigger 'check_waiting_processes'? Yes.
    
    print("\n-- Final Status --")
    pm.display_process_table()
    rm.display_resource_status()

def test_bankers():
    print("\n=== Testing Banker's Algorithm ===")
    pm = ProcessManager()
    rm = ResourceManager(pm)
    dm = DeadlockManager(pm, rm)
    
    # Resources: A: 10, B: 5, C: 7
    rm.initialize_resources({'A': 10, 'B': 5, 'C': 7})
    
    # P1
    pm.create_process("P1", 10, 1, 0)
    rm.set_max_need("P1", {'A': 7, 'B': 5, 'C': 3})
    
    # Alloc some
    rm.request_resource("P1", "A", 0) # Just to ensure alloc entry exists? Not needed.
    # Request A: 5, B: 2, C: 2
    rm.request_resource("P1", "A", 5) # Alloc: 5, Need: 2. Avail: 5.
    rm.request_resource("P1", "B", 2)
    rm.request_resource("P1", "C", 2)
    
    # Check Safety of new request P1 wants A: 1
    # Current: Alloc A:5, Need A:2. Avail A:5.
    # Request 1 -> Alloc 6, Need 1. Avail 4.
    # 1 <= 4? Yes. Safe.
    
    print("\n-- Checking Safety for P1 requesting A:1 --")
    is_safe = dm.check_safety_for_request("P1", "A", 1)
    print(f"Is Safe: {is_safe}")
    
    # Check unsafe request
    # Request A: 3 => Alloc 8, Need -1 (Error).
    # Request A: 2 (if max was 7, need is 2).
    # Wait. Max=7. Alloc=5. Need=2.
    # Request 3 -> exceeds Max. My rm.request doesn't check against Max (Phase 3 didn't require).
    # But Banker's check does: need = max - alloc.
    # If request > need -> Error logic in loop.
    
    # Let's try P1 requesting more than Max Need?
    # Or creating unsafe state with multiple processes.
    
    # P2
    pm.create_process("P2", 10, 1, 0)
    rm.set_max_need("P2", {'A': 8}) # Max 8
    # Request 3 A. Avail was 5. Now 2.
    rm.request_resource("P2", "A", 3)
    
    # Now State:
    # P1: Alloc A:5, Max A:7, Need A:2.
    # P2: Alloc A:3, Max A:8, Need A:5.
    # Avail A: 2.
    
    # Request P1 A: 1.
    # Temp Alloc P1: 6, Need P1: 1. Avail: 1.
    # Can P1 finish? Need 1 <= Avail 1. Yes. Returns 6. Avail becomes 7.
    # Can P2 finish? Need 5 <= Avail 7. Yes.
    # SAFE.
    
    print("\n-- Checking Safety for P1 requesting A:1 (Scenario 2) --")
    dm.check_safety_for_request("P1", "A", 1)

if __name__ == "__main__":
    test_deadlock_scenario()
    test_bankers()
