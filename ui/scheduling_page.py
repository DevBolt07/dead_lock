import streamlit as st
import pandas as pd
import plotly.express as px
import time
from ui.components import render_process_table

def calculate_response_times(result, pm):
    # Calculates response times from Gantt chart data and arrival times
    response_times = {}
    gantt_data = result.get('gantt', [])
    for entry in gantt_data:
        pid = entry['Process']
        if pid == "IDLE":
            continue
        if pid not in response_times:
            p = pm.get_process(pid)
            if p:
                response_times[pid] = entry['Start'] - p.arrival_time
    return response_times

def render_simulation_ui(algo, quantum):
    st.divider()
    st.header("⏱️ Step-by-Step Simulation View")
    
    ss = st.session_state.get("step_scheduler")
    if not ss: return
    
    # Controls
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("▶ Start Simulation", disabled=ss.is_finished() or st.session_state.get('auto_play', False)):
            st.session_state.auto_play = True
            st.rerun()
    with c2:
        if st.button("⏸ Pause", disabled=not st.session_state.get('auto_play', False)):
            st.session_state.auto_play = False
            st.rerun()
    with c3:
        if st.button("⏭ Next Step", disabled=ss.is_finished() or st.session_state.get('auto_play', False)):
            st.session_state.auto_play = False
            ss.step()
            st.rerun()
    with c4:
        if st.button("🔄 Reset"):
            st.session_state.auto_play = False
            ss.reset(algo, quantum)
            st.rerun()
            
    st.subheader(f"Current Time: {ss.time}")
    
    col_q1, col_q2, col_q3 = st.columns(3)
    
    with col_q1:
        st.markdown("### Running Queue")
        if ss.running_process:
            st.success(f"**{ss.running_process.pid}** (Rem: {ss.running_process.remaining_time})", icon="🏃")
        else:
            st.info("Idle")
            
    with col_q2:
        st.markdown("### Ready Queue")
        if ss.ready_queue:
            for p in ss.ready_queue:
                st.warning(f"**{p.pid}** (Rem: {p.remaining_time})", icon="⏳")
        else:
            st.markdown("*Empty*")
            
    with col_q3:
        st.markdown("### Completed Processes")
        if ss.completed_processes:
            for p in ss.completed_processes:
                st.info(f"**{p.pid}** (TAT: {p.turnaround_time}, WT: {p.waiting_time})", icon="✅")
        else:
            st.markdown("*None*")

    if st.session_state.get('auto_play', False):
        if not ss.is_finished():
            time.sleep(1.0)
            ss.step()
            st.rerun()
        else:
            st.session_state.auto_play = False
            st.success("Simulation Completed!")

def render_scheduling_page(sim):
    st.header("💻 CPU Scheduling Simulator")
    
    with st.container():
        render_process_table(sim.process_manager)
    
    st.divider()
    
    with st.container():
        st.subheader("⚙️ Scheduling Controls")
        col1, col2, col3, col4 = st.columns([1.5, 1, 1, 1])
        with col1:
            algo = st.selectbox("Select Algorithm", ["FCFS", "SJF (Non-preemptive)", "SRTF (Preemptive)", "Priority Scheduling", "Round Robin"])
        
        with col2:
            quantum = 2
            if algo == "Round Robin":
                quantum = st.number_input("Time Quantum", min_value=1, value=2)
                
        with col3:
            st.write("")
            st.write("")
            run_btn = st.button("▶ Run Scheduler", width="stretch", type="primary", key="btn_run_cpu")
            
        with col4:
            st.write("")
            st.write("")
            sim_btn = st.button("⏱️ Run Simulation", width="stretch", type="secondary", key="btn_sim_cpu")
            
    if sim_btn:
        st.session_state.scheduler_mode = "simulation"
        from core.step_scheduler import StepScheduler
        st.session_state.step_scheduler = StepScheduler(sim.process_manager)
        st.session_state.step_scheduler.reset(algo, quantum)
        st.session_state.auto_play = False

    mode = st.session_state.get("scheduler_mode")
    if mode == "simulation":
        render_simulation_ui(algo, quantum)

    if run_btn:
        st.session_state.scheduler_mode = "instant"
        st.divider()
        result = None
        if algo == "FCFS":
            result = sim.scheduler.run_fcfs()
        elif algo == "SJF (Non-preemptive)":
            result = sim.scheduler.run_sjf()
        elif algo == "SRTF (Preemptive)":
            result = sim.scheduler.run_srtf()
        elif algo == "Priority Scheduling":
            result = sim.scheduler.run_priority()
        elif algo == "Round Robin":
            result = sim.scheduler.run_round_robin(quantum)
            
        if not result or not result['metrics']:
            st.warning("⚠️ No processes to schedule!")
        else:
            st.success("✅ Scheduling Complete!")
            
            # Additional metric calculation: Response Time
            response_times = calculate_response_times(result, sim.process_manager)

            # Update metrics table terminology
            metrics_df = pd.DataFrame(result['metrics'])
            if not metrics_df.empty:
                metrics_df = metrics_df.rename(columns={
                    "Burst": "Burst Time",
                    "Arrival": "Arrival Time",
                    "Finish": "Completion Time",
                    "Turnaround": "Turnaround Time",
                    "Waiting": "Waiting Time"
                })
                # Add response time column
                metrics_df["Response Time"] = metrics_df["PID"].map(response_times).fillna(0).astype(int)

                # Calculate Averages
                avg_wt = metrics_df["Waiting Time"].mean()
                avg_tat = metrics_df["Turnaround Time"].mean()
                avg_rt = metrics_df["Response Time"].mean()
            else:
                avg_wt = 0
                avg_tat = 0
                avg_rt = 0

            with st.container():
                st.subheader("📈 Metrics")
                
                # Educational block
                with st.expander("ℹ️ Scheduling Concepts"):
                    st.markdown("""
                    **Burst Time**  
                    CPU time required by a process.
                    
                    **Arrival Time**  
                    Time at which a process enters the ready queue.
                    
                    **Completion Time**  
                    Time at which process finishes execution.
                    
                    **Turnaround Time**  
                    Turnaround Time = Completion Time − Arrival Time
                    
                    **Waiting Time**  
                    Waiting Time = Turnaround Time − Burst Time
                    
                    **Response Time**  
                    Response Time = First CPU Allocation − Arrival Time
                    """)

                col_m1, col_m2, col_m3 = st.columns(3)
                with col_m1:
                    st.metric("Avg Waiting Time", f"{avg_wt:.2f}")
                with col_m2:
                    st.metric("Avg Turnaround Time", f"{avg_tat:.2f}")
                with col_m3:
                    st.metric("Avg Response Time", f"{avg_rt:.2f}")
                    
                st.dataframe(metrics_df, width="stretch")
                
            st.divider()
                
            with st.container():
                st.subheader("📉 Gantt Chart")
                gantt_data = result.get('gantt', [])
                
                if gantt_data:
                    df = pd.DataFrame(gantt_data)
                    df['Start_Time'] = pd.to_datetime(df['Start'], unit='s')
                    df['Finish_Time'] = pd.to_datetime(df['Finish'], unit='s')
                    
                    color_map = {
                        "p1": "#1f77b4", # blue
                        "p2": "#2ca02c", # green
                        "p3": "#ff7f0e", # orange
                        "p4": "#d62728", # red
                        "IDLE": "#7f7f7f"
                    }

                    fig = px.timeline(
                        df, 
                        x_start="Start_Time", 
                        x_end="Finish_Time", 
                        y="Process", 
                        color="Process",
                        color_discrete_map=color_map,
                        title=f"Execution Timeline ({algo})",
                        custom_data=['Process', 'Start', 'Finish']
                    )
                    
                    fig.update_xaxes(
                        type='date',
                        tickformat="%-S",
                        title_text="Time (Units)"
                    )

                    fig.update_traces(
                        hovertemplate="<b>Process ID:</b> %{customdata[0]}<br><b>Start Time:</b> %{customdata[1]}<br><b>End Time:</b> %{customdata[2]}<extra></extra>"
                    )
                    
                    st.plotly_chart(fig, width="stretch")
                    
                st.write("**Execution Order:** ", " ➡️ ".join([str(pid) for pid in result.get('execution_order', [])]))
