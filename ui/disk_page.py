import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def render_disk_page(sim):
    st.header("💽 Disk Scheduling Simulator")
    
    # Needs a disk manager attached to sim if not already there
    if not hasattr(sim, 'disk_manager'):
        from core.disk import DiskManager
        sim.disk_manager = DiskManager()
        
    dm = sim.disk_manager
    
    with st.expander("ℹ️ Disk Scheduling Concepts"):
        st.markdown("""
        **Seek Time**: The time taken for a hard disk controller to locate a specific piece of stored data.
        
        **Algorithms**:
        - **FCFS (First-Come, First-Served)**: Services requests in the order they arrive.
        - **SSTF (Shortest Seek Time First)**: Selects the request that is closest to the current head position.
        - **SCAN (Elevator)**: Head moves from one end of the disk to the other, servicing requests along the way, then reverses direction.
        - **C-SCAN (Circular SCAN)**: Similar to SCAN, but when it reaches the end, it immediately returns to the beginning without servicing requests on the return trip.
        """)
        
    st.subheader("Disk Configuration")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("**Track Requests (Comma separated ints)**")
        req_input = st.text_input("Request Queue", value="82, 170, 43, 140, 24, 16, 190")
        
    with col2:
        st.write("**Initial Head Position**")
        head_input = st.number_input("Head Position", min_value=0, max_value=dm.max_tracks-1, value=50)
        
    with col3:
        st.write("**Max Tracks (Cylinders)**")
        max_tracks_input = st.number_input("Max Tracks", min_value=10, value=200)
        dm.max_tracks = max_tracks_input
        
    try:
        requests = [int(p.strip()) for p in req_input.split(",") if p.strip().isdigit()]
        # Filter out invalid tracks
        requests = [r for r in requests if 0 <= r < dm.max_tracks]
    except:
        requests = []
        
    st.divider()
    
    st.subheader("Scheduling Simulation")
    
    algo_col, dir_col, btn_col = st.columns([2, 1, 1])
    with algo_col:
        algo = st.selectbox("Algorithm", ["FCFS", "SSTF", "SCAN", "C-SCAN"])
    with dir_col:
        direction = "Right"
        if algo in ["SCAN", "C-SCAN"]:
            direction = st.selectbox("Direction", ["Right", "Left"])
    with btn_col:
        st.write("")
        st.write("")
        run_btn = st.button("▶ Run Simulation", width="stretch", type="primary", key="btn_run_disk")
        
    if run_btn and requests:
        if algo == "FCFS":
            result = dm.calculate_fcfs(requests, head_input)
        elif algo == "SSTF":
            result = dm.calculate_sstf(requests, head_input)
        elif algo == "SCAN":
            result = dm.calculate_scan(requests, head_input, direction)
        elif algo == "C-SCAN":
            result = dm.calculate_cscan(requests, head_input, direction)
            
        seek_count = result["seek_count"]
        sequence = result["sequence"]
        
        # Display Metrics
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Total Seek Count (Head Movements)", seek_count)
        col_m2.metric("Total Requests Serviced", len(requests))
            
        st.subheader("Head Movement Visualization")
        
        # Build 2D line graph over 'Time' steps
        if sequence:
            df = pd.DataFrame({
                "Step": range(len(sequence)),
                "Track": sequence
            })
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df["Track"], 
                y=df["Step"],
                mode='lines+markers+text',
                text=df["Track"],
                textposition="top center",
                line=dict(color="#1f77b4", width=3),
                marker=dict(size=10, color="#ff7f0e", symbol="diamond")
            ))
            
            fig.update_layout(
                title=f"Disk Head Path ({result['algo']})",
                xaxis_title="Track / Cylinder Number",
                yaxis_title="Time (Steps) ↓",
                xaxis=dict(range=[-5, dm.max_tracks + 5]),
                yaxis=dict(autorange="reversed"), # Steps go top to bottom
                height=600
            )
            
            st.plotly_chart(fig, width="stretch")
            
            st.write("**Seek Sequence:**", " ➡️ ".join([str(t) for t in sequence]))
