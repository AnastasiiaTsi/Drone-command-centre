import streamlit as st
import requests
import uuid
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(
    page_title="ORION | Drone Command",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

API_URL = "http://localhost:8000"

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #e6edf3; }
    h1, h2, h3 { color: #58a6ff !important; font-family: 'Segoe UI', sans-serif; }
    div[data-testid="stMetric"] {
        background-color: #161b22; border: 1px solid #30363d;
        padding: 15px; border-radius: 8px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #238636 0%, #2ea043 100%);
        color: white; border: none; padding: 0.5rem; width: 100%;
    }
    .console-box {
        background-color: #0d1117; border: 1px solid #30363d;
        border-radius: 6px; padding: 15px; font-family: 'Courier New', monospace;
        color: #7ee787; height: 400px; overflow-y: auto;
    }
    .custom-border {
        border: 1px solid #30363d; border-radius: 8px;
        padding: 20px; margin-bottom: 20px; background-color: #161b22;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
c1, c2 = st.columns([3, 1])
with c1:
    st.title("🛸 ORION COMMAND CENTER")
    st.caption("TACTICAL DRONE OPERATIONS SYSTEM v2.0")
with c2:
    if st.button("🔄 REFRESH SYSTEM"):
        st.rerun()
st.markdown("---")

# --- MAIN LAYOUT ---
col_sidebar, col_main = st.columns([1, 2], gap="large")

with col_sidebar:
    st.markdown("### 🛠 MISSION CONFIG")
    st.markdown('<div class="custom-border">', unsafe_allow_html=True)
    
    m_id = st.text_input("MISSION ID", value=str(uuid.uuid4())[:8].upper())
    
    st.markdown("#### PLATFORM")
    drone_choice = st.selectbox("Drone Class", 
        ["military", "agriculture", "rescue", "pollution_monitoring", "exploration", "defects_detection"])
    env_choice = st.selectbox("Environment", ["air", "sea", "surface"])
    
    st.markdown("#### PARAMETERS")
    eng_type = st.select_slider("Engine Type", options=["electric", "hybrid", "combustion"])
    payload_weight = st.slider("Payload (kg)", 0, 50, 15, format="%d kg")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🚀 INITIATE LAUNCH SEQUENCE"):
        payload = {
            "mission_id": m_id, "mission_type": drone_choice,
            "environment_type": env_choice, "platform_type": env_choice,
            "mode": "single", "target_area": [100.0, 100.0],
            "base_area": [0.0, 0.0], "thresholds": {},
            "behavior_params": {"weight": float(payload_weight), "wind_speed": 5.0}
        }
        try:
            with st.spinner('Uplinking to drone swarm...'):
                response = requests.post(f"{API_URL}/mission/run", json=payload, timeout=5)
                if response.status_code == 200:
                    st.success(f"MISSION {m_id} DEPLOYED")
                    st.session_state['last_mission_id'] = m_id
                else:
                    st.error(f"FAILED: {response.json().get('detail')}")
        except requests.exceptions.ConnectionError:
            st.error("CRITICAL: SERVER OFFLINE (Run main.py)")
        except Exception as e:
            st.error(f"ERROR: {e}")

    st.markdown('</div>', unsafe_allow_html=True)

with col_main:
    st.markdown("### TELEMETRY & LOGS")
    search_col, _ = st.columns([2,1])
    with search_col:
        default_id = st.session_state.get('last_mission_id', "")
        search_id = st.text_input("Search Mission ID:", value=default_id)
    
    if search_id:
        try:
            res = requests.get(f"{API_URL}/mission/result/{search_id}", timeout=2)
            if res.status_code == 200:
                data = res.json()
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("STATUS", "COMPLETED", delta="OK")
                m2.metric("DRONE", data["drone_type"].upper())
                m3.metric("ENV", data["environment"].upper())
                m4.metric("BATTERY", "87%", "-2%")
                
                logs_html = ""
                results_data = data["result"]
                if isinstance(results_data, dict): 
                    events = results_data.get("events", [])
                    logs = events + [f"Task: {results_data.get('task_result')}"]
                elif isinstance(results_data, list):
                    logs = results_data
                else:
                    logs = [str(results_data)]

                for step in logs:
                    logs_html += f"<div style='border-bottom:1px solid #21262d; padding:4px;'>➜ {step}</div>"
                st.markdown(f"<div class='console-box'>{logs_html}</div>", unsafe_allow_html=True)
            else:
                st.info("ℹAwaiting data... (ID not found)")
        except:
             st.warning("Telemetry Offline")
    else:
        st.info("Initiate a mission to view telemetry data")