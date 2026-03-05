class MemoryManager:
    """
    Manages physical contiguous memory partitions.
    """
    def __init__(self, total_memory=1024, os_size=128):
        self.total_memory = total_memory
        self.os_size = os_size
        self.blocks = []
        self.reset_blocks()

    def reset_blocks(self):
        """Resets the memory grid representing partitions."""
        # By default create a single large free block representing available user space
        self.blocks = [
            {"id": "b1", "size": self.total_memory - self.os_size, "allocated": False, "pid": None}
        ]

    def add_custom_blocks(self, sizes):
        """Initializes predefined partition sizes (e.g. Fixed Partitioning)."""
        self.blocks = []
        for i, size in enumerate(sizes):
            self.blocks.append(
                {"id": f"b{i+1}", "size": size, "allocated": False, "pid": None}
            )

    def total_free_space(self):
        return sum(b['size'] for b in self.blocks if not b['allocated'])

    def clear_allocations(self):
        """Frees all blocks for a new simulation run."""
        for b in self.blocks:
            b['allocated'] = False
            b['pid'] = None

    def allocate_first_fit(self, requests):
        """
        Allocates memory using First Fit strategy.
        Returns a list of logs and total internal fragmentation.
        """
        logs = []
        internal_frag = 0
        self.clear_allocations()

        for req in requests:
            pid = req['pid']
            size = req['size']
            allocated = False

            for block in self.blocks:
                if not block['allocated'] and block['size'] >= size:
                    block['allocated'] = True
                    block['pid'] = pid
                    internal_frag += (block['size'] - size)
                    logs.append(f"✅ Process {pid} ({size}K) allocated to Block {block['id']} ({block['size']}K).")
                    allocated = True
                    break
            
            if not allocated:
                logs.append(f"❌ Process {pid} ({size}K) FAILED to allocate (Requires {size}K, Max Available Block < {size}K).")

        return {"logs": logs, "internal_frag": internal_frag, "algorithm": "First Fit"}

    def allocate_best_fit(self, requests):
        logs = []
        internal_frag = 0
        self.clear_allocations()

        for req in requests:
            pid = req['pid']
            size = req['size']
            
            # Find the best block: smallest free block that is large enough
            best_idx = -1
            min_diff = float('inf')

            for i, block in enumerate(self.blocks):
                if not block['allocated'] and block['size'] >= size:
                    diff = block['size'] - size
                    if diff < min_diff:
                        min_diff = diff
                        best_idx = i

            if best_idx != -1:
                block = self.blocks[best_idx]
                block['allocated'] = True
                block['pid'] = pid
                internal_frag += (block['size'] - size)
                logs.append(f"✅ Process {pid} ({size}K) allocated to Block {block['id']} ({block['size']}K) [Diff: {min_diff}K].")
            else:
                logs.append(f"❌ Process {pid} ({size}K) FAILED to allocate.")

        return {"logs": logs, "internal_frag": internal_frag, "algorithm": "Best Fit"}

    def allocate_worst_fit(self, requests):
        logs = []
        internal_frag = 0
        self.clear_allocations()

        for req in requests:
            pid = req['pid']
            size = req['size']
            
            # Find the worst block: largest free block that is large enough
            worst_idx = -1
            max_diff = -1

            for i, block in enumerate(self.blocks):
                if not block['allocated'] and block['size'] >= size:
                    diff = block['size'] - size
                    if diff > max_diff:
                        max_diff = diff
                        worst_idx = i

            if worst_idx != -1:
                block = self.blocks[worst_idx]
                block['allocated'] = True
                block['pid'] = pid
                internal_frag += (block['size'] - size)
                logs.append(f"✅ Process {pid} ({size}K) allocated to Block {block['id']} ({block['size']}K) [Diff: {max_diff}K].")
            else:
                logs.append(f"❌ Process {pid} ({size}K) FAILED to allocate.")

        return {"logs": logs, "internal_frag": internal_frag, "algorithm": "Worst Fit"}

    def allocate_next_fit(self, requests):
        logs = []
        internal_frag = 0
        self.clear_allocations()
        
        last_allocated_index = 0

        for req in requests:
            pid = req['pid']
            size = req['size']
            allocated = False
            
            n = len(self.blocks)
            for i in range(n):
                idx = (last_allocated_index + i) % n
                block = self.blocks[idx]
                
                if not block['allocated'] and block['size'] >= size:
                    block['allocated'] = True
                    block['pid'] = pid
                    internal_frag += (block['size'] - size)
                    logs.append(f"✅ Process {pid} ({size}K) allocated to Block {block['id']} ({block['size']}K) [Next Fit Search].")
                    last_allocated_index = idx
                    allocated = True
                    break
            
            if not allocated:
                logs.append(f"❌ Process {pid} ({size}K) FAILED to allocate.")

        return {"logs": logs, "internal_frag": internal_frag, "algorithm": "Next Fit"}

    def allocate_buddy_system(self, requests, initial_size=1024):
        """
        Simulates the Buddy System memory allocation.
        Memory sizes must be powers of 2.
        """
        import math
        logs = []
        internal_frag = 0
        
        # Power of 2 check
        def next_power_of_2(x):
            return 1 if x == 0 else 2**(x - 1).bit_length()
            
        initial_size = next_power_of_2(initial_size)
        
        # Represent memory as a list of free lists keyed by sizes
        self.blocks = [] # for visualization
        
        # We will track active nodes
        # nodes = list of dict: {id, size, address, allocated, pid}
        nodes = [{"id": "b_root", "size": initial_size, "address": 0, "allocated": False, "pid": None}]
        
        for req in requests:
            pid = req['pid']
            req_size = req['size']
            target_size = next_power_of_2(req_size)
            
            allocated = False
            
            # Find the best fitting node
            # 1. Look for exact match
            # 2. Look for larger free nodes to split
            
            while not allocated:
                # Find smallest free node >= target_size
                suitable_nodes = [n for n in nodes if not n['allocated'] and n['size'] >= target_size]
                if not suitable_nodes:
                    break
                    
                # Sort by size (ascending) to get smallest first, then by address
                suitable_nodes.sort(key=lambda x: (x['size'], x['address']))
                best_node = suitable_nodes[0]
                
                if best_node['size'] == target_size:
                    # Allocate
                    best_node['allocated'] = True
                    best_node['pid'] = pid
                    internal_frag += (target_size - req_size)
                    logs.append(f"✅ Process {pid} ({req_size}K) allocated successfully (Buddy Block {target_size}K).")
                    allocated = True
                else:
                    # Need to split
                    new_size = best_node['size'] // 2
                    nodes.remove(best_node)
                    
                    left_buddy = {
                        "id": f"{best_node['id']}_L",
                        "size": new_size,
                        "address": best_node['address'],
                        "allocated": False,
                        "pid": None
                    }
                    right_buddy = {
                        "id": f"{best_node['id']}_R",
                        "size": new_size,
                        "address": best_node['address'] + new_size,
                        "allocated": False,
                        "pid": None
                    }
                    nodes.extend([left_buddy, right_buddy])
                    logs.append(f"✂️ Split block ({best_node['size']}K) into Buddies (2x {new_size}K).")
                    
            if not allocated:
                logs.append(f"❌ Process {pid} ({req_size}K) FAILED to allocate (Requires {target_size}K).")
                
        # Re-map self.blocks for the visualizer to render
        # Sort by address
        nodes.sort(key=lambda x: x['address'])
        self.blocks = nodes
        
        return {"logs": logs, "internal_frag": internal_frag, "algorithm": "Buddy System"}
