import streamlit as st
import pandas as pd
import plotly.express as px

def render_vm_page(sim):
    st.header("📄 Virtual Memory & Demand Paging")
    
    # Needs a vm manager attached to sim if not already there
    if not hasattr(sim, 'vm_manager'):
        from core.virtual_memory import VirtualMemoryManager
        sim.vm_manager = VirtualMemoryManager()
        
    vm = sim.vm_manager
    
    with st.expander("ℹ️ Paging Concepts"):
        st.markdown("""
        **Virtual Memory**: A memory management technique that provides an "idealized abstraction of the storage resources that are actually available on a given machine" which "creates the illusion to users of a very large (main) memory".
        **Page Fault**: An exception that the memory management unit (MMU) raises when a process accesses a memory page without proper mappings in the MMU.
        
        **Page Replacement Algorithms**:
        - **FIFO**: Replaces the oldest page in memory.
        - **LRU (Least Recently Used)**: Replaces the page that has not been used for the longest time.
        - **Optimal**: Replaces the page that will not be used for the longest period of time (Theoretical).
        - **Clock (Second-Chance)**: A variation of FIFO that uses a 'use bit' to give pages a second chance before swapping them out.
        """)
        
    st.subheader("Paging Configuration")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Reference String (Comma separated integers)**")
        ref_input = st.text_input("Reference String", value="7,0,1,2,0,3,0,4,2,3,0,3")
        
    with col2:
        st.write("**Number of Page Frames**")
        frame_input = st.number_input("Frames", min_value=1, max_value=10, value=3)
        
    try:
        ref_string = [int(p.strip()) for p in ref_input.split(",") if p.strip().isdigit()]
    except:
        ref_string = []
        
    st.divider()
    
    st.subheader("Page Replacement Simulation")
    
    algo_col, btn_col = st.columns([2, 1])
    with algo_col:
        algo = st.selectbox("Algorithm", ["FIFO", "LRU", "Optimal", "Clock"])
    with btn_col:
        st.write("")
        st.write("")
        run_btn = st.button("▶ Run Simulation", width="stretch", type="primary", key="btn_run_vm")
        
    if run_btn and ref_string:
        if algo == "FIFO":
            result = vm.calculate_fifo(ref_string, frame_input)
        elif algo == "LRU":
            result = vm.calculate_lru(ref_string, frame_input)
        elif algo == "Optimal":
            result = vm.calculate_optimal(ref_string, frame_input)
        elif algo == "Clock":
            result = vm.calculate_clock(ref_string, frame_input)
            
        faults = result["faults"]
        hits = result["hits"]
        total = faults + hits
        hit_ratio = (hits / total) * 100 if total > 0 else 0
        miss_ratio = (faults / total) * 100 if total > 0 else 0
        
        # Display Metrics
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        col_m1.metric("Page Faults", faults)
        col_m2.metric("Page Hits", hits)
        col_m3.metric("Hit Ratio", f"{hit_ratio:.1f}%")
        col_m4.metric("Miss Ratio", f"{miss_ratio:.1f}%")
            
        st.subheader("Step-by-Step Visualization")
        
        # Build tabular visualizer
        steps = result["steps"]
        
        if steps:
            # Create a dataframe where rows=Frames, cols=Steps
            data = {}
            data["Reference Page"] = [str(step["Page"]) for step in steps]
            data["Status"] = [step["Status"] for step in steps]
            
            for i in range(frame_input):
                frame_row = []
                for step in steps:
                    if i < len(step["Frames"]):
                        val = str(step["Frames"][i])
                        # If Clock algo, it adds asterisk to frame directly in backend
                        frame_row.append(val)
                    else:
                        frame_row.append("-")
                data[f"Frame {i+1}"] = frame_row
                
            df_vis = pd.DataFrame(data).T # Transpose so Steps go left-to-right
            
            # Apply color to Status row
            def color_status(val):
                if val == "Miss":
                    return "color: #d62728; font-weight: bold;" # Red
                elif val == "Hit":
                    return "color: #2ca02c; font-weight: bold;" # Green
                return ""
            
            st.dataframe(df_vis.style.map(color_status), width="stretch")
            
        # Draw Pie Chart
        fig = px.pie(
            names=["Hits", "Faults (Misses)"],
            values=[hits, faults],
            title=f"Efficiency Breakdown ({algo})",
            color_discrete_sequence=["#2ca02c", "#d62728"]
        )
        st.plotly_chart(fig, width="stretch")
