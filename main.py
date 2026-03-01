from process import ProcessManager
from scheduler import Scheduler
from resource import ResourceManager
from deadlock import DeadlockManager
import sys

def print_header():
    print("\n" + "="*40)
    print("   Smart Process & Deadlock Manager")
    print("="*40)

def main_menu():
    print("\n--- Main Menu ---")
    print("1. Create Process")
    print("2. Show Process Table")
    print("3. Run Scheduler")
    print("4. Configure Resources")
    print("5. Request Resource")
    print("6. Release Resource")
    print("7. Show Resource Status")
    print("8. Set Max Need (Banker's)")
    print("9. Run Deadlock Detection")
    print("10. Run Deadlock Avoidance Check")
    print("11. Run Deadlock Recovery")
    print("12. Exit")
    print("13. Load Demo Data")
    print("-----------------")

def get_valid_int(prompt):
    while True:
        try:
            val = int(input(prompt))
            if val < 0:
                print("Please enter a non-negative integer.")
                continue
            return val
        except ValueError:
            print("Invalid input. Please enter an integer.")

# --- Demo Mode Feature ---
def reset_system(pm, rm):
    """Resets system state for demo mode."""
    pm.processes.clear()
    rm.resources.clear()
    rm.available.clear()
    rm.allocation.clear()
    rm.request.clear()

def load_demo_data(pm, rm):
    """Loads predefined dataset for presentation purposes."""
    print("\n--- Loading Demo Data ---")
    reset_system(pm, rm)
    
    # Automatically create processes
    pm.create_process("p1", 5, 2, 0)
    pm.create_process("p2", 3, 1, 2)
    pm.create_process("p3", 4, 3, 4)
    
    # Configure resources
    rm.initialize_resources({"R1": 5, "R2": 3})
    
    # Set Max Need
    rm.set_max_need("p1", {"R1": 3, "R2": 2})
    rm.set_max_need("p2", {"R1": 2, "R2": 1})
    rm.set_max_need("p3", {"R1": 4, "R2": 1})
    
    print("Demo data loaded successfully.")
# -------------------------


def main():
    pm = ProcessManager()
    rm = ResourceManager(pm)
    dm = DeadlockManager(pm, rm)
    scheduler = Scheduler(pm)
    
    # Pre-configure some defaults for easier testing
    # rm.initialize_resources({'R1': 10, 'R2': 5}) 
    
    print_header()
    
    while True:
        main_menu()
        choice = input("Select an option: ").strip()
        
        if choice == '1':
            print("\n--- Create Process ---")
            pid = input("Enter Process ID (PID): ").strip()
            if not pid:
                print("PID cannot be empty.")
                continue
            
            burst = get_valid_int("Enter Burst Time: ")
            priority = get_valid_int("Enter Priority (lower = higher): ")
            arrival = get_valid_int("Enter Arrival Time: ")
            
            pm.create_process(pid, burst, priority, arrival)
            
        elif choice == '2':
            pm.display_process_table()
            
        elif choice == '3':
            print("\n--- Select Scheduling Algorithm ---")
            print("1. First Come First Serve (FCFS)")
            print("2. Priority Scheduling (Non-Preemptive)")
            print("3. Round Robin")
            algo = input("Select Algorithm: ").strip()
            
            if algo == '1':
                scheduler.run_fcfs()
            elif algo == '2':
                scheduler.run_priority()
            elif algo == '3':
                quantum = get_valid_int("Enter Time Quantum: ")
                if quantum == 0:
                    print("Quantum must be greater than 0.")
                else:
                    scheduler.run_round_robin(quantum)
            else:
                print("Invalid selection.")

        elif choice == '4':
            print("\n--- Configure Resources ---")
            print("Enter resources in format: Type:Count,Type:Count (e.g. R1:10,R2:5)")
            res_str = input("Resources: ").strip()
            try:
                resources = {}
                parts = res_str.split(',')
                for part in parts:
                    if ':' in part:
                        r_type, count = part.split(':')
                        resources[r_type.strip()] = int(count.strip())
                rm.initialize_resources(resources)
            except ValueError:
                print("Invalid format. Please use Type:Count,Type:Count")

        elif choice == '5':
            print("\n--- Request Resource ---")
            pid = input("Enter PID: ").strip()
            res_type = input("Enter Resource Type: ").strip()
            amount = get_valid_int("Enter Amount: ")
            rm.request_resource(pid, res_type, amount)

        elif choice == '6':
            print("\n--- Release Resource ---")
            pid = input("Enter PID: ").strip()
            res_type = input("Enter Resource Type: ").strip()
            amount = get_valid_int("Enter Amount: ")
            rm.release_resource(pid, res_type, amount)

        elif choice == '7':
            rm.display_resource_status()

        elif choice == '8':
            print("\n--- Set Max Need for Banker's Algorithm ---")
            pid = input("Enter PID: ").strip()
            print("Enter Max Need in format: Type:Count,Type:Count")
            res_str = input("Max Need: ").strip()
            try:
                max_need = {}
                parts = res_str.split(',')
                for part in parts:
                    if ':' in part:
                        r_type, count = part.split(':')
                        max_need[r_type.strip()] = int(count.strip())
                rm.set_max_need(pid, max_need)
            except ValueError:
                print("Invalid format.")

        elif choice == '9':
            dm.detect_deadlock()

        elif choice == '10':
            print("\n--- Deadlock Avoidance Check ---")
            pid = input("Enter PID: ").strip()
            res_type = input("Enter Resource Type: ").strip()
            amount = get_valid_int("Enter Amount to simulate: ")
            dm.check_safety_for_request(pid, res_type, amount)

        elif choice == '11':
            dm.resolve_deadlock()

        elif choice == '12':
            print("Exiting system. Goodbye!")
            sys.exit()

        elif choice == '13':
            load_demo_data(pm, rm)
            
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
