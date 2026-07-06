import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import time

st.set_page_config(layout="wide", page_title="Virtual Traffic DSP Simulator")

st.title("🚗 Fully Virtual Edge-DSP Traffic Simulator")
st.subheader("Zero-Hardware Demonstration Using Synchronized Data Streams")

# --- SIMULATION CONFIGURATION ---
fs = 50  # 50 Hz sampling rate
video_duration = 10  # 10 seconds video loop
total_samples = fs * video_duration
time_axis = np.linspace(0, video_duration, total_samples)

# --- PRE-GENERATING THE COMPANION MAGNETIC DATA (Matches Report Pipeline) ---
# 1. Background Earth Magnetic Field + Slow Drift Component
baseline_drift = 0.2 * np.sin(2 * np.pi * 0.05 * time_axis)
Bx = 0.3 + baseline_drift + np.random.normal(0, 0.04, total_samples)
By = 0.4 + baseline_drift + np.random.normal(0, 0.04, total_samples)
Bz = 0.5 + baseline_drift + np.random.normal(0, 0.04, total_samples)

# 2. Inject Virtual Vehicle Events (e.g., Vehicle passes at exactly 3.0s and 7.0s)
pass_times = [3.0, 7.0]
for t in pass_times:
    idx = int(t * fs)
    width = int(1.2 * fs)  # 1.2-second vehicle footprint
    start, end = idx - width//2, idx + width//2
    # Standard Gaussian envelope modeling ferromagnetic disruption
    pulse = 1.6 * np.exp(-np.linspace(-2, 2, end - start)**2)
    Bx[start:end] += pulse * 0.9
    By[start:end] += pulse * 0.6
    Bz[start:end] += pulse * 1.2

# --- APP LAYOUT ---
col_vid, col_metrics = st.columns([1.2, 1])

with col_vid:
    st.markdown("### 📽️ Simulated Traffic Video Feed")
    # Placeholder for video. In a real setup, you can point to a local file or URL
    # e.g., st.video("traffic_simulation.mp4")
    st.video("https://www.w3schools.com/html/mov_bbb.mp4") 
    st.caption("ℹ️ In production, replace this with your overhead scale-testbed video clip.")

    # Interactive simulation controller
    run_sim = st.checkbox("▶️ Start Live Data Processing Loop")

with col_metrics:
    st.markdown("### 📊 Edge Node DSP Dashboard")
    metric_status = st.empty()
    metric_energy = st.empty()
    metric_count = st.empty()

st.markdown("---")
plot_placeholder = st.empty()

# --- REAL-TIME PROCESSING LOOP ---
if run_sim:
    start_time = time.time()
    vehicle_count = 0
    detected_flags = [False, False]  # Track the two injected events
    
    while (time.time() - start_time) < video_duration:
        # Get current playback time relative to loop execution
        elapsed = time.time() - start_time
        current_sample_idx = min(int(elapsed * fs), total_samples - 1)
        
        # --- EXECUTE EXACT DSP CODES UP TO THE CURRENT TIME SLICE ---
        # Step 1: Scalar Magnitude Transformation
        B_total = np.sqrt(Bx**2 + By**2 + Bz**2)
        
        # Step 2: Baseline Correction (Moving Window M)
        M = int(fs * 2)
        B_base = pd.Series(B_total).rolling(window=M, min_periods=1, center=True).mean().to_numpy()
        B_corrected = B_total - B_base
        
        # Step 3: Low Pass Filter Smoothing
        B_filtered = pd.Series(B_corrected).rolling(window=5, min_periods=1).mean().to_numpy()
        
        # Slice vectors to match current playback timestamp window
        visible_time = time_axis[:current_sample_idx]
        visible_signal = B_filtered[:current_sample_idx]
        
        # Event Detection Logic (Threshold Checking)
        current_val = B_filtered[current_sample_idx]
        is_congested = False
        
        # Simple rule-based check to increment mock vehicle counter
        for i, p_t in enumerate(pass_times):
            if elapsed >= p_t and not detected_flags[i]:
                detected_flags[i] = True
                vehicle_count += 1
                
        # Compute instantaneous window energy
        window_size = int(fs * 1.5)
        if current_sample_idx > window_size:
            recent_window = B_filtered[current_sample_idx - window_size : current_sample_idx]
            inst_energy = np.sum(recent_window**2)
        else:
            inst_energy = 0.0

        # Update Metrics UI Components dynamically
        metric_status.metric("Traffic State", "🔴 HIGH (Vehicle Passing)" if current_val > 0.5 else "🟢 LOW / IDLE")
        metric_energy.metric("Instantaneous Window Energy (E_sig)", f"{inst_energy:.4f}")
        metric_count.metric("Cumulative Vehicle Count (N_events)", f"{vehicle_count}")
        
        # Dynamic Signal Processing Plot Render
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=visible_time, y=B_total[:current_sample_idx], name="Raw Input Magnitude B_total", line=dict(color="gray", width=1)))
        fig.add_trace(go.Scatter(x=visible_time, y=visible_signal, name="Processed Signal y[n]", line=dict(color="cyan", width=2)))
        fig.add_hline(y=0.5, line_dash="dash", line_color="red", annotation_text="Noise Floor Threshold (τ)")
        fig.update_layout(title="On-Device FIR Filtering & Baseline Extraction Window", xaxis_title="Time (seconds)", yaxis_title="Amplitude", xaxis_range=[0, video_duration], yaxis_range=[-0.5, 3.0])
        
        plot_placeholder.plotly_chart(fig, use_container_width=True)
        
        # Enforce loop pacing to mimic real-time 50Hz ingestion speeds
        time.sleep(1/fs)
else:
    st.info("Check the box above to trigger the synthetic real-time telemetry processing pipeline.")