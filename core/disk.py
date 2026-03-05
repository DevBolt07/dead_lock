class DiskManager:
    """
    Simulates Disk Scheduling Algorithms.
    Algorithms: FCFS, SSTF, SCAN, C-SCAN
    """
    def __init__(self, max_tracks=200):
        self.max_tracks = max_tracks
        
    def calculate_fcfs(self, requests, initial_head):
        """First-Come, First-Served Disk Scheduling"""
        seek_count = 0
        current_head = initial_head
        sequence = [initial_head]
        
        for req in requests:
            sequence.append(req)
            seek_count += abs(req - current_head)
            current_head = req
            
        return {"seek_count": seek_count, "sequence": sequence, "algo": "FCFS"}
        
    def calculate_sstf(self, requests, initial_head):
        """Shortest Seek Time First Disk Scheduling"""
        seek_count = 0
        current_head = initial_head
        sequence = [initial_head]
        
        # Work on a copy of requests
        pending = list(requests)
        
        while pending:
            # Find closest request
            closest = None
            min_dist = float('inf')
            
            for req in pending:
                dist = abs(req - current_head)
                if dist < min_dist:
                    min_dist = dist
                    closest = req
                    
            sequence.append(closest)
            seek_count += min_dist
            current_head = closest
            pending.remove(closest)
            
        return {"seek_count": seek_count, "sequence": sequence, "algo": "SSTF"}
        
    def calculate_scan(self, requests, initial_head, direction="Right"):
        """SCAN (Elevator) Disk Scheduling"""
        seek_count = 0
        current_head = initial_head
        sequence = [initial_head]
        
        pending = list(requests)
        
        # Sort left and right of head
        left = sorted([r for r in pending if r < initial_head], reverse=True)
        right = sorted([r for r in pending if r >= initial_head])
        
        if direction == "Right":
            # Go right to boundary, then left
            if right:
                for r in right:
                    sequence.append(r)
                    seek_count += abs(r - current_head)
                    current_head = r
            
            # Hit right boundary if there are left requests pending
            if left:
                boundary = self.max_tracks - 1
                if current_head != boundary:
                    sequence.append(boundary)
                    seek_count += abs(boundary - current_head)
                    current_head = boundary
                    
                for l in left:
                    sequence.append(l)
                    seek_count += abs(l - current_head)
                    current_head = l
                    
        else: # Left
            # Go left to boundary, then right
            if left:
                for l in left:
                    sequence.append(l)
                    seek_count += abs(l - current_head)
                    current_head = l
                    
            # Hit left boundary
            if right:
                boundary = 0
                if current_head != boundary:
                    sequence.append(boundary)
                    seek_count += abs(boundary - current_head)
                    current_head = boundary
                    
                for r in right:
                    sequence.append(r)
                    seek_count += abs(r - current_head)
                    current_head = r
                    
        return {"seek_count": seek_count, "sequence": sequence, "algo": f"SCAN ({direction})"}
        
    def calculate_cscan(self, requests, initial_head, direction="Right"):
        """Circular-SCAN Disk Scheduling"""
        seek_count = 0
        current_head = initial_head
        sequence = [initial_head]
        
        pending = list(requests)
        
        left = sorted([r for r in pending if r < initial_head]) # ascending
        right = sorted([r for r in pending if r >= initial_head]) # ascending
        
        if direction == "Right":
            # Right then jump to 0 and go right again
            if right:
                for r in right:
                    sequence.append(r)
                    seek_count += abs(r - current_head)
                    current_head = r
                    
            if left:
                # To right boundary
                boundary_right = self.max_tracks - 1
                if current_head != boundary_right:
                    sequence.append(boundary_right)
                    seek_count += abs(boundary_right - current_head)
                    current_head = boundary_right
                    
                # Jump to left boundary
                boundary_left = 0
                sequence.append(boundary_left)
                # Technically seek_count doesn't count the jump in some textbooks, but we'll include it or note it
                seek_count += abs(boundary_left - current_head)
                current_head = boundary_left
                
                # Service left requests
                for l in left:
                    sequence.append(l)
                    seek_count += abs(l - current_head)
                    current_head = l
                    
        else: # Left
            left = sorted(left, reverse=True)
            right = sorted(right, reverse=True)
            
            if left:
                for l in left:
                    sequence.append(l)
                    seek_count += abs(l - current_head)
                    current_head = l
                    
            if right:
                # To left boundary
                boundary_left = 0
                if current_head != boundary_left:
                    sequence.append(boundary_left)
                    seek_count += abs(boundary_left - current_head)
                    current_head = boundary_left
                    
                # Jump to right boundary
                boundary_right = self.max_tracks - 1
                sequence.append(boundary_right)
                seek_count += abs(boundary_right - current_head)
                current_head = boundary_right
                
                # Service right requests
                for r in right:
                    sequence.append(r)
                    seek_count += abs(r - current_head)
                    current_head = r
                    
        return {"seek_count": seek_count, "sequence": sequence, "algo": f"C-SCAN ({direction})"}
