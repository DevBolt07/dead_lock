import streamlit as st
import pandas as pd
import plotly.express as px

def render_memory_page(sim):
    st.header("🧱 Contiguous Memory Allocation")
    
    # Needs a memory manager attached to sim if not already there
    if not hasattr(sim, 'memory_manager'):
        from core.memory import MemoryManager
        sim.memory_manager = MemoryManager()
        
    mm = sim.memory_manager
    
    with st.expander("ℹ️ Memory Concepts"):
        st.markdown("""
        **Fixed Partitioning**: Main memory is divided into static partitions at system generation time.
        **Dynamic Partitioning**: Partitions are created dynamically, so that each process is loaded into a partition of exactly the same size as the process.
        
        **Placement Algorithms**:
        - **First Fit**: Allocate the first free block that is large enough.
        - **Best Fit**: Allocate the smallest free block that is large enough.
        - **Worst Fit**: Allocate the largest free block that is large enough.
        - **Next Fit**: Allocate the first free block that is large enough, starting to search from the location of the last allocation.
        """)
        
    st.subheader("Memory Configuration")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Define Memory Partitions (Comma separated, in KB)**")
        default_blocks = ",".join([str(b['size']) for b in mm.blocks])
        blocks_input = st.text_input("Partition Blocks", value=default_blocks if default_blocks else "300,600,350,200,750")
        
    with col2:
        st.write("**Process Requests (PID:Size, comma separated)**")
        req_input = st.text_input("Requests", value="p1:115, p2:500, p3:358, p4:200, p5:375")
        
    # Parse blocks
    try:
        parsed_blocks = [int(b.strip()) for b in blocks_input.split(",") if b.strip().isdigit()]
    except:
        parsed_blocks = []
        
    # Parse requests
    try:
        parsed_requests = []
        for r in req_input.split(","):
            if ":" in r:
                pid, size = r.split(":")
                parsed_requests.append({"pid": pid.strip(), "size": int(size.strip())})
    except:
        parsed_requests = []
        
    st.divider()
    
    st.subheader("Allocation Simulation")
    
    algo_col, btn_col = st.columns([2, 1])
    with algo_col:
        algo = st.selectbox("Algorithm", ["First Fit", "Best Fit", "Worst Fit", "Next Fit", "Buddy System"])
    with btn_col:
        st.write("")
        st.write("")
        run_btn = st.button("▶ Run Allocation", width="stretch", type="primary", key="btn_run_memory")
        
    if run_btn and parsed_blocks and parsed_requests:
        mm.add_custom_blocks(parsed_blocks)
        
        if algo == "First Fit":
            result = mm.allocate_first_fit(parsed_requests)
        elif algo == "Best Fit":
            result = mm.allocate_best_fit(parsed_requests)
        elif algo == "Worst Fit":
            result = mm.allocate_worst_fit(parsed_requests)
        elif algo == "Next Fit":
            result = mm.allocate_next_fit(parsed_requests)
        elif algo == "Buddy System":
            # For Buddy System we treat the sum of custom blocks as initial max memory pool size
            pool_size = sum(parsed_blocks) if parsed_blocks else 1024
            result = mm.allocate_buddy_system(parsed_requests, initial_size=pool_size)
            
        logs = result.get("logs", [])
        
        # Display Logs and Internal Frag
        col_res1, col_res2 = st.columns([2, 1])
        with col_res1:
            st.write("**Allocation Logs**")
            for log in logs:
                if "✅" in log:
                    st.success(log)
                else:
                    st.error(log)
                    
        with col_res2:
            st.metric("Total Internal Fragmentation", f"{result['internal_frag']} KB")
            total_free = mm.total_free_space()
            st.metric("Remaining Free Space", f"{total_free} KB")
            
        st.subheader("Memory Block Visualization")
        
        # Visualization
        vis_data = []
        for b in mm.blocks:
            allocated_size = 0
            free_size = b['size']
            state = "Free"
            pid_label = "Free"
            
            if b['allocated']:
                # Find size from reqs
                req_size = next((r['size'] for r in parsed_requests if r['pid'] == b['pid']), b['size'])
                allocated_size = req_size
                free_size = b['size'] - req_size
                state = "Allocated"
                pid_label = b['pid']
                
            vis_data.append({
                "Block ID": b['id'],
                "Total Size (KB)": b['size'],
                "State": state,
                "Process": pid_label,
                "Used (KB)": allocated_size,
                "Internal Frag (KB)": free_size if b['allocated'] else 0,
                "Free Space (KB)": free_size if not b['allocated'] else 0
            })
            
        df_vis = pd.DataFrame(vis_data)
        st.dataframe(df_vis, width="stretch")
        
        # Draw stacked bar using Plotly to show utilization per block
        # We need data in format: Block, Type (Used/Frag/Free), Value
        chart_data = []
        for b in mm.blocks:
            if b['allocated']:
                req_size = next((r['size'] for r in parsed_requests if r['pid'] == b['pid']), b['size'])
                chart_data.append({"Block": b['id'], "Segment": f"Used by {b['pid']}", "Size": req_size})
                if b['size'] > req_size:
                    chart_data.append({"Block": b['id'], "Segment": "Internal Fragmentation", "Size": b['size'] - req_size})
            else:
                chart_data.append({"Block": b['id'], "Segment": "Free Space", "Size": b['size']})
                
        if chart_data:
            df_chart = pd.DataFrame(chart_data)
            fig = px.bar(
                df_chart, 
                x="Block", 
                y="Size", 
                color="Segment", 
                title=f"Memory Utilization ({algo})",
                color_discrete_map={
                    "Internal Fragmentation": "#ff7f0e",
                    "Free Space": "#2ca02c"
                }
            )
            fig.update_layout(barmode='stack')
            st.plotly_chart(fig, width="stretch")
