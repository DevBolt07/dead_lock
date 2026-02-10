from process import ProcessManager
from scheduler import Scheduler

def test_phase2():
    pm = ProcessManager()
    scheduler = Scheduler(pm)

    print("Creating processes...")
    pm.create_process("P1", burst_time=5, priority=2, arrival_time=0)
    pm.create_process("P2", burst_time=3, priority=1, arrival_time=2)
    pm.create_process("P3", burst_time=2, priority=3, arrival_time=4)
    
    pm.display_process_table()

    print("\n--- Testing FCFS ---")
    scheduler.run_fcfs()
    
    print("\n--- Testing Priority (Non-Preemptive) ---")
    scheduler.run_priority()
    
    print("\n--- Testing Round Robin (Quantum=2) ---")
    scheduler.run_round_robin(quantum=2)

if __name__ == "__main__":
    test_phase2()
