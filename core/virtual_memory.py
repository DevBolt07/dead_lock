class VirtualMemoryManager:
    """
    Simulates Page Replacement Algorithms for Virtual Memory.
    Algorithms: FIFO, LRU, Optimal, Clock
    """
    def __init__(self, frame_count=3):
        self.frame_count = frame_count

    def calculate_fifo(self, reference_string, frames):
        """First-In, First-Out Page Replacement"""
        memory = []
        page_faults = 0
        hits = 0
        steps = []

        for curr_page in reference_string:
            status = "Miss"
            if curr_page in memory:
                hits += 1
                status = "Hit"
            else:
                page_faults += 1
                if len(memory) >= frames:
                    memory.pop(0)  # Remove oldest
                memory.append(curr_page)
            
            steps.append({
                "Page": curr_page,
                "Frames": list(memory),
                "Status": status
            })

        return {"faults": page_faults, "hits": hits, "steps": steps, "algo": "FIFO"}

    def calculate_lru(self, reference_string, frames):
        """Least Recently Used Page Replacement"""
        memory = []
        page_faults = 0
        hits = 0
        steps = []
        
        # We can use memory index as priority, where end of list is mostly recently used
        for curr_page in reference_string:
            status = "Miss"
            if curr_page in memory:
                hits += 1
                status = "Hit"
                memory.remove(curr_page)
                memory.append(curr_page)
            else:
                page_faults += 1
                if len(memory) >= frames:
                    memory.pop(0) # Least recently used is at index 0
                memory.append(curr_page)
                
            steps.append({
                "Page": curr_page,
                "Frames": list(memory),
                "Status": status
            })

        return {"faults": page_faults, "hits": hits, "steps": steps, "algo": "LRU"}

    def calculate_optimal(self, reference_string, frames):
        """Optimal Page Replacement (Furthest in future)"""
        memory = []
        page_faults = 0
        hits = 0
        steps = []

        for i, curr_page in enumerate(reference_string):
            status = "Miss"
            if curr_page in memory:
                hits += 1
                status = "Hit"
            else:
                page_faults += 1
                if len(memory) >= frames:
                    # Find furthest page in future
                    furthest_idx = -1
                    page_to_replace = None
                    for mem_page in memory:
                        try:
                            future_idx = reference_string[i+1:].index(mem_page)
                        except ValueError:
                            # Not used again
                            page_to_replace = mem_page
                            break
                        
                        if future_idx > furthest_idx:
                            furthest_idx = future_idx
                            page_to_replace = mem_page
                            
                    memory.remove(page_to_replace)
                memory.append(curr_page)
                
            steps.append({
                "Page": curr_page,
                "Frames": list(memory),
                "Status": status
            })

        return {"faults": page_faults, "hits": hits, "steps": steps, "algo": "Optimal"}

    def calculate_clock(self, reference_string, frames):
        """Clock (Second-Chance) Page Replacement"""
        memory = []
        use_bit = {}
        pointer = 0
        page_faults = 0
        hits = 0
        steps = []

        for curr_page in reference_string:
            status = "Miss"
            if curr_page in memory:
                hits += 1
                status = "Hit"
                use_bit[curr_page] = 1
            else:
                page_faults += 1
                if len(memory) < frames:
                    memory.append(curr_page)
                    use_bit[curr_page] = 1
                else:
                    while True:
                        victim = memory[pointer]
                        if use_bit[victim] == 0:
                            # Replace
                            memory[pointer] = curr_page
                            use_bit[curr_page] = 1
                            del use_bit[victim]
                            pointer = (pointer + 1) % frames
                            break
                        else:
                            # Second chance
                            use_bit[victim] = 0
                            pointer = (pointer + 1) % frames
                            
            # Format frame visual to include asterisks indicating use bit
            frame_visual = [f"{p}*" if use_bit.get(p, 0) == 1 else str(p) for p in memory]
            
            steps.append({
                "Page": curr_page,
                "Frames": frame_visual,
                "Status": status
            })

        return {"faults": page_faults, "hits": hits, "steps": steps, "algo": "Clock"}
