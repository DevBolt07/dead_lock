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

def run_all_and_compare(sim, quantum):
    results = []
    
    res_fcfs = sim.scheduler.run_fcfs()
    if res_fcfs:
        res_fcfs['algo'] = "FCFS"
        results.append(res_fcfs)
        
    res_sjf = sim.scheduler.run_sjf()
    if res_sjf:
        res_sjf['algo'] = "SJF (Non-preemptive)"
        results.append(res_sjf)
        
    res_srtf = sim.scheduler.run_srtf()
    if res_srtf:
        res_srtf['algo'] = "SRTF (Preemptive)"
        results.append(res_srtf)
        
    res_pri = sim.scheduler.run_priority()
    if res_pri:
        res_pri['algo'] = "Priority Scheduling"
        results.append(res_pri)
        
    res_rr = sim.scheduler.run_round_robin(quantum)
    if res_rr:
        res_rr['algo'] = "Round Robin"
        results.append(res_rr)
        
    return results

def render_simulation_ui(algo, quantum):
    st.divider()
    st.header("⏱️ Step-by-Step Simulation View")
    
    ss = st.session_state.get("step_scheduler")
    if not ss: return
    
    # Controls
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        if st.button("▶ Start Simulation", disabled=ss.is_finished() or st.session_state.get('auto_play', False)):
            st.session_state.auto_play = True
            st.rerun()
    with c2:
        is_playing = st.session_state.get('auto_play', False)
        if is_playing:
            if st.button("⏸ Pause"):
                st.session_state.auto_play = False
                st.rerun()
        else:
            if st.button("▶ Resume", disabled=ss.is_finished()):
                st.session_state.auto_play = True
                st.rerun()
    with c3:
        if st.button("⏪ Previous Step", disabled=len(ss.history) == 0):
            st.session_state.auto_play = False
            ss.step_back()
            st.rerun()
    with c4:
        if st.button("⏭ Next Step", disabled=ss.is_finished()):
            st.session_state.auto_play = False
            ss.step()
            st.rerun()
    with c5:
        if st.button("🔄 Reset"):
            st.session_state.auto_play = False
            ss.reset(algo, quantum)
            st.rerun()
            
    st.markdown(f"#### 🔄 Queue Flow Simulation &nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp; ⏱️ Current Time: **{ss.time}**")
    col_q1, col_q2, col_q3, col_q4 = st.columns(4)
    
    with col_q1.empty().container():
        st.markdown("#### Job Queue")
        jobs = list({p.pid: p for p in ss.job_queue}.values())
        if jobs:
            for p in jobs:
                st.info(f"**{p.pid}** (Arr: {p.arrival_time})", icon="📦")
        else:
            st.markdown("*Empty*")
            
    with col_q2.empty().container():
        st.markdown("#### Ready Queue")
        unique_ready = list({p.pid: p for p in ss.ready_queue}.values())
        if unique_ready:
            for p in unique_ready:
                st.warning(f"**{p.pid}** (Rem: {p.remaining_time})", icon="⏳")
        else:
            st.markdown("*Empty*")
            
    with col_q3.empty().container():
        st.markdown("#### CPU (Running)")
        if ss.running_process:
            st.success(f"**{ss.running_process.pid}** (Rem: {ss.running_process.remaining_time})", icon="⚙️")
        else:
            st.error("Idle", icon="💤")
            
    with col_q4.empty().container():
        st.markdown("#### Completed")
        unique_completed = list({p.pid: p for p in ss.completed_processes}.values())
        if unique_completed:
            for p in unique_completed:
                st.info(f"**{p.pid}** (TAT: {p.turnaround_time}, WT: {p.waiting_time})", icon="✅")
        else:
            st.markdown("*None*")

    st.write("")

    # Live Metrics Table Section
    st.markdown("#### 📊 Live Metrics Table")
    metrics_data = []
    for p in ss.processes:
        # Fetch the dynamically added response_time (fallback seamlessly to -1)
        rt = getattr(p, "response_time", -1)
        metrics_data.append({
            "PID": str(p.pid),
            "Arrival Time": str(p.arrival_time),
            "Burst Time": str(p.burst_time),
            "Remaining Time": str(p.remaining_time),
            "Completion Time": str(p.completion_time) if p.state == "Terminated" else "-",
            "Turnaround Time": str(p.turnaround_time) if p.state == "Terminated" else "-",
            "Waiting Time": str(p.waiting_time) if p.state == "Terminated" else "-",
            "Response Time": str(rt) if rt != -1 else "-",
            "Status": str(p.state)
        })

    df_metrics = pd.DataFrame(metrics_data)

    def highlight_rows(row):
        color = ""
        st_val = row["Status"]
        if st_val == "Ready":
            color = "background-color: rgba(243, 156, 18, 0.2)" # Orange hint for arrival/waiting
        elif st_val == "Running":
            color = "background-color: rgba(39, 174, 96, 0.3)"  # Green hint for active computing
        elif st_val == "Terminated":
            color = "background-color: rgba(52, 152, 219, 0.2)" # Blue hint for strictly completed

        return [color] * len(row)

    # Calculate ideal exact height: 35px per row + ~38px header
    ideal_height = (len(ss.processes) + 1) * 36 + 3
    st.dataframe(df_metrics.style.apply(highlight_rows, axis=1), use_container_width=True, height=ideal_height, hide_index=True)

    st.write("")
    
    col_bot1, col_bot2 = st.columns([1, 2.5])
    
    with col_bot1:
        # Event Log Section
        st.markdown("#### 📝 Last Action Log")
        if ss.event_log:
            for event in reversed(ss.event_log):
                st.caption(f"🔹 {event}")
        else:
            st.caption("No events yet.")
            
    with col_bot2:
        # Timeline Section
        st.markdown("#### ⏱️ Execution Timeline")
        if ss.timeline:
            timeline_str = " | ".join(ss.timeline)
            st.code(timeline_str, language="text")
        else:
            st.code("Simulation not started.", language="text")

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

    st.divider()
    
    with st.expander("📊 Algorithm Comparison View", expanded=False):
        st.subheader("Compare All Algorithms")
        st.markdown("Runs all 5 CPU scheduling algorithms on the current processes simultaneously for direct performance comparison.")
        
        comp_quantum = st.number_input("Time Quantum for Round Robin (Comparison)", min_value=1, value=2, key="comp_quantum_input")
        
        if st.button("▶ Run All & Compare", type="primary", key="btn_compare_all"):
            results = run_all_and_compare(sim, comp_quantum)
            if not results:
                st.warning("⚠️ No processes to schedule!")
            else:
                st.success("✅ Comparison Complete!")
                comp_data = []
                for res in results:
                    rt_dict = calculate_response_times(res, sim.process_manager)
                    df_metrics = pd.DataFrame(res['metrics'])
                    if not df_metrics.empty:
                        df_metrics["Response Time"] = df_metrics["PID"].map(rt_dict).fillna(0).astype('int')
                        comp_data.append({
                            "Algorithm": res['algo'],
                            "Avg Waiting Time": df_metrics["Waiting"].mean(),
                            "Avg Turnaround Time": df_metrics["Turnaround"].mean(),
                            "Avg Response Time": df_metrics["Response Time"].mean()
                        })
                    else:
                        comp_data.append({
                            "Algorithm": res['algo'],
                            "Avg Waiting Time": 0,
                            "Avg Turnaround Time": 0,
                            "Avg Response Time": 0
                        })
                
                comp_df = pd.DataFrame(comp_data)
                
                # Render Unified Comparison Table
                st.markdown("#### Comparison Table")
                st.dataframe(comp_df.style.format({
                    "Avg Waiting Time": "{:.2f}", 
                    "Avg Turnaround Time": "{:.2f}",
                    "Avg Response Time": "{:.2f}"
                }), use_container_width=True)
                
                # Plot grouped bar chart
                st.markdown("#### Performance Chart")
                comp_melted = comp_df.melt(id_vars=["Algorithm"], var_name="Metric", value_name="Time (Units)")
                fig_comp = px.bar(
                    comp_melted, 
                    x="Algorithm", 
                    y="Time (Units)", 
                    color="Metric", 
                    barmode="group",
                    title="Algorithm Metrics Comparison"
                )
                st.plotly_chart(fig_comp, use_container_width=True)
