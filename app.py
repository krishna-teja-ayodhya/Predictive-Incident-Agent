import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Predictive Incident Agent", page_icon="🚨", layout="wide")

st.title("🚨 Predictive Incident Intelligence Agent")
st.markdown("Analyze system logs, find root causes, and predict future failures using Groq AI and Hindsight Vector Memory.")

# Backend configuration
BACKEND_URL = "http://127.0.0.1:8000"

# Sidebar configuration check
st.sidebar.header("System Status")
if not os.getenv("GROQ_API_KEY"):
    st.sidebar.error("⚠️ GROQ_API_KEY missing. Analysis will fail.")
else:
    st.sidebar.success("✅ GROQ_API_KEY configured.")

if not os.getenv("HINDSIGHT_API_KEY"):
    st.sidebar.warning("⚠️ HINDSIGHT_API_KEY missing. Vector Memory disabled.")
else:
    st.sidebar.success("✅ HINDSIGHT_API_KEY configured.")

st.subheader("Incident Log Input")
log_input = st.text_area("Paste your system log or error message here:", height=150)

col1, col2 = st.columns([1, 4])
with col1:
    analyze_btn = st.button("🔍 Analyze Incident", type="primary")
with col2:
    simulate_btn = st.button("🧪 Simulate Failure")

if simulate_btn:
    sample_log = """[2023-10-27 10:15:32] ERROR: OutOfMemoryError: Java heap space
    at com.example.service.DataProcessor.processBatch(DataProcessor.java:145)
    at com.example.service.WorkerThread.run(WorkerThread.java:55)"""
    log_input = sample_log
    st.info(f"Loaded Sample Log:\n\n{sample_log}")
    analyze_btn = True

if analyze_btn:
    if not log_input.strip():
        st.warning("Please enter a valid system log to analyze.")
    else:
        with st.spinner("Analyzing incident, querying memory, and predicting fallout..."):
            try:
                response = requests.post(f"{BACKEND_URL}/analyze", json={"log": log_input}, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    st.markdown("---")
                    
                    # Display Memory Status
                    if data.get("memory_used"):
                        st.success("🧠 Hindsight Memory Applied: Found context from similar past incidents.")
                    else:
                        st.info("🧠 No past incidents found in memory (or API unavailable).")
                        
                    # Display Analysis
                    st.subheader("🛠️ Root Cause & Solution")
                    st.write(data.get("analysis", "No analysis returned."))
                    
                    # Display Prediction
                    st.subheader("🔮 Cascading Failure Prediction")
                    st.warning(data.get("prediction", "No prediction available."))
                else:
                    st.error(f"Backend Error: {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to FastAPI backend. Ensure you run `uvicorn main:app --reload` first.")
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")

st.markdown("---")
st.markdown("<small>Powered by FastAPI, Streamlit, Groq (LLM), and Hindsight (Vector Memory).</small>", unsafe_allow_html=True)
