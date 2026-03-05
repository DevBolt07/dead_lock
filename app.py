import streamlit as st
from core.simulation_state import SimulationState
from ui.scheduling_page import render_scheduling_page
from ui.deadlock_page import render_deadlock_page
from ui.memory_page import render_memory_page
from ui.vm_page import render_vm_page
from ui.disk_page import render_disk_page

st.set_page_config(page_title="Smart Process & Deadlock Manager", layout="wide")

if "sim" not in st.session_state:
    st.session_state.sim = SimulationState()

st.title("Smart Process & Deadlock Manager")

with st.sidebar:
    st.header("Global Controls")
    if st.button("Load Demo Data", width="stretch"):
        st.session_state.sim.load_demo_data()
        st.success("Demo data loaded!")
    
    st.markdown("---")
    st.markdown("**Processes:**")
    st.write([p.pid for p in st.session_state.sim.process_manager.get_all_processes()])

tab1, tab2, tab3, tab4, tab5 = st.tabs(["CPU Scheduling", "Deadlock Management", "Memory Allocation", "Virtual Memory", "Disk Scheduling"])

with tab1:
    render_scheduling_page(st.session_state.sim)

with tab2:
    render_deadlock_page(st.session_state.sim)

with tab3:
    render_memory_page(st.session_state.sim)
    
with tab4:
    render_vm_page(st.session_state.sim)

with tab5:
    render_disk_page(st.session_state.sim)
