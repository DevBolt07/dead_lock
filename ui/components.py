import streamlit as st
import pandas as pd

def get_process_color(pid):
    colors = {
        "p1": "blue",
        "p2": "green",
        "p3": "orange",
        "p4": "red"
    }
    return colors.get(pid, "gray")

def render_process_table(pm):
    st.subheader("📊 Process Table")
    processes = pm.get_all_processes()
    
    data = []
    for p in processes:
        data.append({
            "PID": p.pid,
            "Burst Time": p.burst_time,
            "Arrival Time": p.arrival_time,
            "Priority": p.priority
        })
    
    if not data:
        # Create an empty dataframe with the required columns
        df = pd.DataFrame(columns=["PID", "Burst Time", "Arrival Time", "Priority"])
    else:
        df = pd.DataFrame(data)
    
    edited_df = st.data_editor(
        df,
        num_rows="dynamic",
        width="stretch",
        column_config={
            "PID": st.column_config.TextColumn("PID", disabled=False),
            "Burst Time": st.column_config.NumberColumn("Burst Time", min_value=1),
            "Arrival Time": st.column_config.NumberColumn("Arrival Time", min_value=0),
            "Priority": st.column_config.NumberColumn("Priority", min_value=1)
        },
        key="process_editor"
    )

    # Sync back to process_manager
    edited_pids = set()
    for _, row in edited_df.iterrows():
        pid = str(row.get("PID", "")).strip()
        if pd.isna(pid) or not pid:
            continue
            
        edited_pids.add(pid)
        burst_time = int(row.get("Burst Time", 1))
        arrival_time = int(row.get("Arrival Time", 0))
        priority = int(row.get("Priority", 1))
        
        p = pm.get_process(pid)
        if p:
            # Update existing
            p.burst_time = burst_time
            p.arrival_time = arrival_time
            p.priority = priority
            p.remaining_time = burst_time
        else:
            # Create new
            pm.create_process(pid, burst_time, priority, arrival_time)
            
    # Delete missing processes
    pm.processes = [p for p in pm.processes if p.pid in edited_pids]
