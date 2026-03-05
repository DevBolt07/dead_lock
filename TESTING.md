# Testing & Validation Guide

The **Smart Process & Deadlock Manager** is a visual simulation suite, making automated unit testing secondary to **Manual Interaction Verification**. 

This document outlines the standard test cases to input into the Streamlit dashboard to verify theoretical fidelity.

---

## 1. Validating CPU Scheduling

Navigate to the **CPU Scheduling** tab.
- Click **"Load Demo Data"** from the left sidebar to pre-populate 5 standardized test processes.
- Set the Algorithm to: `SJF (Non-preemptive)`
- Click **"▶ Run Scheduler"**
- **Expected Verification**: The Plotly Gantt chart should explicitly jump to process P4 purely because its `Burst Time` structurally outweighs its `Arrival Time` when the CPU queue evaluated shorter jobs dynamically.

---

## 2. Validating Deadlock Management

Navigate to the **Deadlock Management** tab.
- Notice the initialized state of Resouces `R1 (6 units)` and `R2 (4 units)`.
- Under the specific `Run Banker's Algorithm (Avoidance)` subheader, click the submit button.
- **Expected Verification**: The simulator will generate a mathematical dataframe proving that `State is SAFE`.
- **Negative Testing**: Using the editable `Request Resource` allocation table, deliberately request 5 units of `R1` for Process 1. The Banker's verification should reject it mathematically (request exceeds max need / available resources).

---

## 3. Validating Memory Allocation

Navigate to the **Memory Allocation** tab.
- For **Custom Free Blocks Data**, enter: `100, 500, 200, 300, 600`
- For **Incoming Process Requests**, enter: `212, 417, 112, 426`
- Set Algorithm to `Best Fit`.
- **Expected Verification**: 
  - The 212K request maps optimally to the 300K block (leaving 88K internal fragmentation).
  - The stacked Block Visualization rendering should render exactly 5 categorical traces corresponding to the physical array limits.

---

## 4. Validating Virtual Memory 

Navigate to the **Virtual Memory** tab.
- For **Reference String**, enter the classic academic test array: `7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3`
- Enter **Frames**: `3`
- Set Algorithm to `LRU` (Least Recently Used).
- **Expected Verification**: 
  - The simulation metrics should strictly state: **Page Faults = 9**.
  - The step-by-step DataFrame will map out the 3 hardware framing nodes moving dynamically along the reference pointer.

---

## 5. Validating Disk Scheduling

Navigate to the **Disk Scheduling** tab.
- Enter **Request Queue**: `82, 170, 43, 140, 24, 16, 190`
- Enter **Head Position**: `50`
- Define Boundary Limit: `200` cylinder tracks.
- Set Algorithm to `SSTF`.
- **Expected Verification**: 
  - The Plotly 2D trace map initially drops immediately from integer 50 to 43 (absolute shortest angular seek distance of 7) rather than jumping to 82.
  - Total Seek Count mathematically resolves to exactly `208` physical head movements.
