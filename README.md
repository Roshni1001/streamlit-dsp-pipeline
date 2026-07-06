# Raspberry Pi Pico DSP Dashboard

An end-to-end DSP project built using MicroPython on Raspberry Pi Pico, validated in Wokwi, and integrated with a Streamlit dashboard for interactive signal visualization. The project demonstrates signal acquisition, filtering, FFT analysis, and dashboard-based monitoring using simulated embedded hardware and Python-based visualization.

## Features

- MicroPython-based DSP implementation on Raspberry Pi Pico
- Wokwi simulation for hardware validation and prototyping
- Signal acquisition and preprocessing pipeline
- FIR/IIR filtering and FFT-based signal analysis
- Streamlit dashboard with interactive plots and controls
- Dashboard visualization using real/simulated traffic feed input
- Technical report and project documentation included

## Tech Stack

- MicroPython
- Raspberry Pi Pico
- Wokwi Simulator
- Python
- Streamlit
- DSP concepts: filtering, FFT, signal analysis

## Project Structure

```text
dsp-dashboard-project/
├── streamlit_app.py
├── README.md
├── Dsp_Project_Analysis.pdf
├── screenshots/
│   ├── dashboard-browser.png
│   └── wokwi-simulation.png
├── media/
│   └── traffic-feed.mp4
└── micropython/
    └── pico_dsp.py
```

## Workflow

1. Simulate the Raspberry Pi Pico setup and DSP logic in Wokwi.
2. Implement DSP routines in MicroPython for signal acquisition, filtering, and FFT.
3. Stream processed data to a Streamlit dashboard.
4. Visualize outputs using interactive plots, controls, and traffic feed integration.
5. Document the system design, implementation flow, and results.

## Screenshots

Project screenshots are available in the `screenshots/` folder:
- Streamlit dashboard running in browser
- Wokwi simulation setup

## Report

The detailed project report is available as `Dsp_Project_Analysis.pdf`.

## Applications

- Embedded DSP prototyping
- Real-time signal visualization
- Simulation-driven hardware-software validation
- Educational DSP demonstrations using Raspberry Pi Pico

## Author

**Roshni Chaudhuri**
