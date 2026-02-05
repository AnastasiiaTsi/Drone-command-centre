import streamlit as st
import requests
import uuid
import sys
import os

# Додає кореневу директорію проекту до шляхів пошуку модулів
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(
    page_title="Drone Mission Control",
    page_icon="🛸",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_URL = "http://localhost:8000"

# Стилізація інтерфейсу
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .mission-log { background-color: #1e1e1e; color: #d4d4d4; padding: 20px; border-radius: 5px; font-family: 'Courier New', monospace; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛸 Drone Mission Control Center")
st.markdown("---")

col_setup, col_monitor = st.columns([1, 2], gap="large")

with col_setup:
    st.header("🛠 Конфігуратор")
    with st.container():
        m_id = st.text_input("ID Місії", value=str(uuid.uuid4())[:8])
        
        drone_choice = st.selectbox("Тип дрона", 
            ["military", "agriculture", "rescue", "pollution_monitoring", "exploration", "defects_detection"])
        
        env_choice = st.selectbox("Середовище", ["air", "sea", "surface"])
        
        st.radio("Тип двигуна", ["electric"], horizontal=True)
        
        st.markdown("### ⚙️ Додаткові параметри")
        payload_weight = st.slider("Вага вантажу (кг)", 0, 50, 10)
        
        if st.button("Запустити місію 🚀"):
            # Формування даних згідно з MissionConfig
            payload = {
                "mission_id": m_id,
                "mission_type": drone_choice,
                "environment_type": env_choice,
                "platform_type": env_choice,
                "mode": "single",
                "target_area": [100.0, 100.0],
                "base_area": [0.0, 0.0],
                "thresholds": {},
                "behavior_params": {"weight": float(payload_weight)}
            }
            
            try:
                with st.spinner('Підключення до систем...'):
                    response = requests.post(f"{API_URL}/mission/run", json=payload)
                    if response.status_code == 200:
                        st.success(f"Місія {m_id} успішно ініційована!")
                        st.balloons()
                    else:
                        st.error(f"Помилка API: {response.json().get('detail')}")
            except Exception as e:
                st.error(f"Сервер не відповідає. Перевірте запуск main.py api")

with col_monitor:
    st.header("📊 Моніторинг та телеметрія")
    search_id = st.text_input("Введіть ID для отримання звіту:", placeholder="Наприклад: a1b2c3d4")
    
    if search_id:
        with st.expander("Завантаження даних місії...", expanded=True):
            try:
                res = requests.get(f"{API_URL}/mission/result/{search_id}")
                if res.status_code == 200:
                    data = res.json()
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Тип дрона", data["drone_type"].upper())
                    m2.metric("Середовище", data["environment"])
                    m3.metric("Статус", "COMPLETED")
                    
                    st.subheader("📋 Лог виконання (Template Method steps)")
                    log_html = "".join([f"<p style='margin:5px 0;'> > {step}</p>" for step in data["result"]])
                    st.markdown(f"<div class='mission-log'>{log_html}</div>", unsafe_allow_html=True)
                else:
                    st.warning("Дані для вказаного ID відсутні в базі.")
            except:
                st.error("Помилка з'єднання з API.")

st.markdown("---")
st.caption("Drone Mission Framework v1.0 | Лабораторна робота №7")