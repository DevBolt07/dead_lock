from process import ProcessManager
from resource import ResourceManager

def test_phase3():
    pm = ProcessManager()
    rm = ResourceManager(pm)

    print("--- Phase 3 Test ---")
    
    # 1. Initialize Resources
    rm.initialize_resources({'R1': 10})
    
    # 2. Create Processes
    pm.create_process("P1", 10, 1, 0)
    pm.create_process("P2", 10, 1, 0)
    
    print("\n[Step 1] P1 requests 8 R1")
    rm.request_resource("P1", "R1", 8)
    rm.display_resource_status()
    print(f"P1 State: {pm.get_process('P1').state}") # Should be Ready (or Running/Allocated, actually Ready)
    
    print("\n[Step 2] P2 requests 3 R1 (Available: 2)")
    rm.request_resource("P2", "R1", 3)
    rm.display_resource_status()
    print(f"P2 State: {pm.get_process('P2').state}") # Should be Waiting
    
    print("\n[Step 3] P1 releases 5 R1 (Available becomes 2+5=7)")
    rm.release_resource("P1", "R1", 5)
    rm.display_resource_status()
    
    print(f"P2 State: {pm.get_process('P2').state}") # Should be Ready now
    print(f"P2 Allocation: {pm.get_process('P2').allocation}") # Should have R1: 3

if __name__ == "__main__":
    test_phase3()
