import streamlit as st
import pandas as pd

def render_deadlock_page(sim):
    st.header("Deadlock & Resource Engine")
    
    rm = sim.resource_manager
    dm = sim.deadlock_manager
    pm = sim.process_manager
    
    st.subheader("System Resources")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Total Configured Resources**")
        st.json(rm.resources)
    with col2:
        st.write("**Available Resources**")
        st.json(rm.available)
        
    st.markdown("---")
    
    # Render Matrices
    st.subheader("Resource Matrices")
    
    m1, m2, m3 = st.columns(3)
    processes = pm.get_all_processes()
    
    def build_df(matrix_dict):
        if not processes: return pd.DataFrame()
        data = []
        for p in processes:
            if p.state == "Terminated": continue
            row = {"PID": p.pid}
            for res in rm.resources:
                val = 0
                if p.pid in matrix_dict and res in matrix_dict[p.pid]:
                    val = matrix_dict[p.pid][res]
                # Default property fallback
                elif hasattr(p, matrix_dict) and type(getattr(p, matrix_dict)) == dict:
                    val = getattr(p, matrix_dict).get(res, 0)
                row[res] = val
            data.append(row)
        return pd.DataFrame(data)
        
    with m1:
        st.write("**Max Need Matrix**")
        data = []
        for p in processes:
            if p.state == "Terminated": continue
            row = {"PID": p.pid}
            for res in rm.resources:
                row[res] = p.max_need.get(res, 0)
            data.append(row)
        if data: st.dataframe(pd.DataFrame(data), width="stretch")
            
    with m2:
        st.write("**Allocation Matrix**")
        if rm.allocation: st.dataframe(build_df(rm.allocation), width="stretch")
            
    with m3:
        st.write("**Request Matrix**")
        if rm.request: st.dataframe(build_df(rm.request), width="stretch")
        
    st.markdown("---")
    
    # Controls
    st.subheader("Deadlock Management")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        if st.button("Run Detect Deadlock", width="stretch"):
            deadlocked = dm.detect_deadlock()
            if deadlocked:
                st.error(f"Deadlock DETECTED! Processes involved: {deadlocked}")
            else:
                st.success("System is SAFE. No deadlock detected.")
                
    with c2:
        st.write("**Simulate Banker's Allocation**")
        bk1, bk2, bk3 = st.columns(3)
        with bk1: req_pid = st.text_input("PID", "p1")
        with bk2: req_res = st.text_input("Resource", "R1")
        with bk3: req_amt = st.number_input("Amount", min_value=1, value=1)
        
        if st.button("Run Avoidance Check", width="stretch"):
            result = dm.check_safety_for_request(req_pid, req_res, req_amt)
            if result.get("safe"):
                st.success(f"{result['msg']} Sequence: {' -> '.join(result['sequence'])}")
            else:
                st.error(result['msg'])
                
    with c3:
        if st.button("Run Deadlock Recovery", width="stretch"):
            logs = dm.resolve_deadlock()
            for log in logs:
                st.warning(log)
            st.rerun()
