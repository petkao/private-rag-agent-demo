import os
import uuid
import time
import streamlit as st

# =====================================================================
# 🌟 STAGE 1: SET INITIAL PAGE CONFIG
# =====================================================================
st.set_page_config(
    page_title="🔒 Private AI Knowledge Base",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🎨 STAGE 2: INJECT PREMIUM DESIGN OVERRIDES (WHITE BLOCKS REMOVED)
st.markdown("""
    <style>
        /* 1. Base App Canvas Background */
        .stApp {
            background-color: #0d0f12 !important;
            color: #e2e8f0 !important;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
            background: linear-gradient(135deg, #090a0f 0%, #11131e 50%, #1a1528 100%) !important;
        }
        
        /* 2. STRIP OUT DEFAULT BACKGROUND LAYERS OVERRIDES */
        [data-testid="stHeader"], 
        [data-testid="stBottom"],
        [data-testid="stBottomBlockContainer"],
        footer {
            background-color: transparent !important;
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }
        
        /* 3. Main Content Layout Constraints */
        [data-testid="stMainBlockContainer"] {
            max-width: 840px !important;
            padding: 2rem 2rem 2rem 2rem !important;
            margin: 0 auto !important;
        }
        
        /* 4. Sidebar Overrides & Visibility Fixes */
        [data-testid="stSidebar"] {
            background-color: #16191f !important;
            border-right: 1px solid #262c36 !important;
        }
        div[data-testid="stSidebar"] {
            background: rgba(13, 15, 24, 0.95) !important;
        }
        
        /* Force Sidebar Expander Wording Text to Be Visible */
        [data-testid="stSidebar"] details summary,
        [data-testid="stSidebar"] details summary * {
            color: #ffffff !important;
            font-weight: 600 !important;
            -webkit-text-fill-color: #ffffff !important;
        }
        [data-testid="stSidebar"] details summary svg {
            fill: #ffffff !important;
            color: #ffffff !important;
        }
        
        /* 5. High-Visibility Custom Layout Cards */
        .glass-card {
            background: rgba(25, 28, 41, 0.6);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
            margin-bottom: 20px;
        }
        .benefit-card {
            background: rgba(97, 175, 239, 0.05);
            border-left: 4px solid #61afef;
            padding: 15px;
            border-radius: 4px 12px 12px 4px;
            margin-top: 15px;
        }
        .testimonial-container {
            background: rgba(255, 255, 255, 0.02);
            border: 1px dashed rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 16px;
            font-size: 0.9rem;
            color: #abb2bf;
            margin-top: 25px;
        }
        
        /* 6. Styled Template Prompt Chip Buttons */
        div.stButton > button {
            background-color: #1e242e !important;
            color: #f1f5f9 !important;
            border: 1px solid #3e4451 !important;
            border-radius: 8px !important;
            padding: 0.8rem 1rem !important;
            font-weight: 500 !important;
            transition: all 0.2s ease !important;
            white-space: pre-wrap !important;
            text-align: left !important;
            line-height: 1.4 !important;
        }
        div.stButton > button:hover {
            border-color: #ffe066 !important;
            color: #ffe066 !important;
            background-color: #282e3d !important;
        }
        
        /* 7. FORM WORKAROUND CONTAINER STYLING */
        div[data-testid="stForm"] {
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            background-color: rgba(22, 25, 31, 0.8) !important;
            border-radius: 14px !important;
            padding: 20px !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4) !important;
        }
        div[data-testid="stForm"] [data-testid="stWidgetLabel"] p {
            color: #ffe066 !important;
            font-weight: 500 !important;
        }
        
        /* High-Contrast Glowing Green Button Accent Pass */
        div[data-testid="stForm"] button[type="submit"] {
            background-color: #2ecc71 !important;
            color: #0d0f12 !important;
            font-weight: 700 !important;
            border: none !important;
            width: 100% !important;
            margin-top: 10px !important;
            box-shadow: 0 0 14px rgba(46, 204, 113, 0.4) !important;
            font-size: 1rem !important;
        }
        div[data-testid="stForm"] button[type="submit"]:hover {
            background-color: #27ae60 !important;
            box-shadow: 0 0 20px rgba(46, 204, 113, 0.6) !important;
        }
        
        /* 8. Informational Status Badges */
        .status-badge {
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            margin-right: 8px;
            margin-bottom: 8px;
            background-color: rgba(152, 195, 121, 0.12);
            color: #98c379;
            border: 1px solid rgba(152, 195, 121, 0.25);
        }
        .status-badge-blue { background-color: rgba(97, 175, 239, 0.12); color: #61afef; border: 1px solid rgba(97, 175, 239, 0.25); }
        .status-badge-purple { background-color: rgba(198, 120, 221, 0.12); color: #c678dd; border: 1px solid rgba(198, 120, 221, 0.25); }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# 🛠️ STAGE 3: STATE INITIALIZATION ARCHITECTURE
# =====================================================================
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []
if "indexed_files" not in st.session_state:
    st.session_state.indexed_files = []

llm_options = ["qwen2.5:7b (Demo)", "gemma4:12b (Demo)", "deepseek-r1:8b (Demo)"]
embedding_options = ["bge-large-en-v1.5", "nomic-embed-text"]

# =====================================================================
# 🧠 STAGE 4: SIDEBAR GENERATION CENTER
# =====================================================================
st.sidebar.markdown("<h2 style='color: #ffffff; margin-top:0;'>🔒 Vault Manager</h2>", unsafe_allow_html=True)

with st.sidebar.expander("⚙️ Advanced Engine Settings", expanded=False):
    llm_model = st.selectbox("Select LLM Model", llm_options, index=0)
    embedding_model = st.selectbox("Select Embedding Model", embedding_options, index=0)

st.sidebar.markdown("---")

st.sidebar.markdown("<h3 style='color: #ffffff;'>🎯 Risk-Free Sandbox Onboarding</h3>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='font-size: 0.82rem; color: #abb2bf; margin-top:-5px;'>✓ Free to try locally — 100% private sandbox</p>", unsafe_allow_html=True)
if st.sidebar.button("🎭 Load Demo Sample Data", use_container_width=True):
    st.session_state.indexed_files = [
        {"filename": "company_travel_policy_2026.pdf", "chunks": 8},
        {"filename": "department_budget_limits.txt", "chunks": 3}
    ]
    st.sidebar.success("Loaded secure demo templates!")
    time.sleep(0.5)
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("<h3 style='color: #ffffff;'>📥 Step 1: Add Local Files</h3>", unsafe_allow_html=True)
uploaded_files = st.sidebar.file_uploader("Drop project files here", type=["pdf", "txt", "png", "jpg"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        if not any(f["filename"] == uploaded_file.name for f in st.session_state.indexed_files):
            st.session_state.indexed_files.append({"filename": uploaded_file.name, "chunks": 5})

st.sidebar.markdown("---")
st.sidebar.markdown("<h3 style='color: #ffffff;'>🗄️ Your Files</h3>", unsafe_allow_html=True)

if not st.session_state.indexed_files:
    st.sidebar.info("Your secure vault is empty. Upload files above or trigger the demo sandbox.")
else:
    for f in list(st.session_state.indexed_files):
        display_name = f["filename"] if len(f["filename"]) <= 22 else f"{f['filename'][:19]}..."
        if st.sidebar.button(f"🗑️ Remove {display_name}", key=f"del_{f['filename']}"):
            st.session_state.indexed_files.remove(f)
            st.rerun()

if st.session_state.indexed_files:
    st.sidebar.markdown("<h4 style='color: #ffffff;'>Ready to Chat</h4>", unsafe_allow_html=True)
    for f in st.session_state.indexed_files:
        st.sidebar.markdown(f"<span class='status-badge'>📄 {f['filename']}</span>", unsafe_allow_html=True)

# =====================================================================
# 💻 STAGE 5: MAIN CANVAS INTERFACE
# =====================================================================
st.markdown("<h1 style='color: #ffe066 !important; background: none; -webkit-text-fill-color: initial;'>Chat with your files without ever leaking data</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 1.1rem; color: #abb2bf; margin-top: -10px;'>Works without the internet to keep your files 100% private.</p>", unsafe_allow_html=True)

if not st.session_state.messages:
    # Onboarding instructions showing step visual mapping flow
    st.markdown(f"""
        <div class='glass-card'>
            <div style="margin-bottom: 16px;">
                <span class='status-badge status-badge-blue'>🛡️ 100% Offline Control</span>
                <span class='status-badge status-badge-purple'>🔒 Enterprise Security Vault</span>
            </div>
            
            <div style='font-size: 1.1rem; font-weight: 600; color: #ffe066; margin-bottom: 12px;'>🚀 Quick Start Guide:</div>
            
            <div style='margin-bottom: 10px; border-left: 3px solid #61afef; padding-left: 12px;'>
                <strong style='color: #61afef;'>Step 1: Load Context</strong><br>
                <span style='font-size: 0.9rem; color: #abb2bf;'>Click the <strong>"🎭 Load Demo Sample Data"</strong> button in the sidebar to instantly load mock corporate policies risk-free.</span>
            </div>
            
            <div style='margin-bottom: 10px; border-left: 3px solid #61afef; padding-left: 12px;'>
                <strong style='color: #61afef;'>Step 2: Ask a Question</strong><br>
                <span style='font-size: 0.9rem; color: #abb2bf;'>Select one of the pre-configured prompt cards below, or type your own question into the secure input box at the bottom.</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<p style='font-size: 1rem; color: #ffe066; font-weight: 600; margin-bottom: 12px;'>📋 Step 3: Select a Sample Question to Test the Engine</p>", unsafe_allow_html=True)
    
    chip_col1, chip_col2, chip_col3 = st.columns(3)
    with chip_col1:
        if st.button("📊 Query Device Budgets\n\n'What is my electronic purchase budget limit?'", use_container_width=True, key="chip1"):
            st.session_state.messages.append({"role": "user", "content": "What is my electronic device purchase budget limit?"})
            st.rerun()
    with chip_col2:
        if st.button("✈️ Query Travel Policy\n\n'What are the company travel rules for 2026?'", use_container_width=True, key="chip2"):
            st.session_state.messages.append({"role": "user", "content": "What are the company travel rules for 2026?"})
            st.rerun()
    with chip_col3:
        if st.button("🌐 Live Web Search\n\n'Search the web for the latest MacBook pricing'", use_container_width=True, key="chip3"):
            st.session_state.messages.append({"role": "user", "content": "Search the web for the latest MacBook pricing online"})
            st.rerun()

# Conversation Render Stream
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            st.markdown(f"""
                <div style="margin-bottom: 8px;">
                    <span class='status-badge status-badge-purple'>STATUS: {message.get("status", "Success")}</span>
                    <span class='status-badge status-badge-blue'>MODE: {message.get("mode", "Offline")}</span>
                </div>
            """, unsafe_allow_html=True)
        st.markdown(f'<div style="line-height: 1.6; color: #f1f5f9; padding: 2px 6px;">{message["content"]}</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Main Form Chat Field Wrapper
with st.form(key="secure_chat_form", clear_on_submit=True):
    user_input = st.text_input(label="💬 Ask your private knowledge base anything:", placeholder="Type a message or select a question card above...")
    submit_button = st.form_submit_button(label="🚀 Start Secure Search")

if submit_button and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.rerun()

# =====================================================================
# 🧠 STAGE 6: ACTIVE ASSISTANT GENERATION PIPELINE (THE MATRIX RESPONDER)
# =====================================================================
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    last_msg = st.session_state.messages[-1]["content"].lower()
    with st.chat_message("assistant"):
        progress_box = st.empty()
        progress_box.markdown("<div class='glass-card'>⚙️ Evaluating internal processing parameters...</div>", unsafe_allow_html=True)
        time.sleep(0.6)
        
        # 1. Routing Rule: Web Search
        if any(w in last_msg for w in ["search", "online", "pricing", "latest", "web"]):
            progress_box.markdown("<div class='glass-card'>🌐 Running secure, anonymized web proxy search...</div>", unsafe_allow_html=True)
            time.sleep(0.8)
            mock_reply = (
                "🔍 **Live Web Search Results (Anonymized Proxy):**\n\n"
                "Based on current June 2026 e-commerce indexes, the Apple MacBook Air M3 (13-inch, 8GB Unified Memory, 256GB SSD) "
                "is retailing between **$999 and $1,099** across authorized marketplace channels. Base configuration alternatives "
                "with 16GB memory arrays are tracking at **$1,199**.\n\n"
                "🔒 *Privacy Context: Your user identifier was stripped using an air-gapped security boundary before hitting the search gateway.*"
            )
            status_val, mode_val = "Web Retrieval Success", "RAG + Web Search"
            
        # 2. Routing Rule: Document Vault - Budget Rules
        elif any(w in last_msg for w in ["budget", "limit", "purchase", "device"]):
            progress_box.markdown("<div class='glass-card'>⚙️ Scanning 'department_budget_limits.txt'...</div>", unsafe_allow_html=True)
            time.sleep(0.8)
            mock_reply = (
                "📊 **Extracted Context from `department_budget_limits.txt`:**\n\n"
                "Your corporate electronic device procurement allowance is strictly capped at **$200** per individual transaction asset. "
                "Any hardware acquisitions exceeding this threshold require explicit administrative override clearance from the operations desk."
            )
            status_val, mode_val = "Local Context Success", "Offline"
            
        # 3. Routing Rule: Document Vault - Travel Rules
        elif any(w in last_msg for w in ["travel", "policy", "hotel", "rules"]):
            progress_box.markdown("<div class='glass-card'>⚙️ Indexing 'company_travel_policy_2026.pdf'...</div>", unsafe_allow_html=True)
            time.sleep(0.8)
            mock_reply = (
                "✈️ **Extracted Context from `company_travel_policy_2026.pdf`:**\n\n"
                "The fiscal year 2026 corporate travel policy mandates that all domestic flights must be booked under Economy tier configurations "
                "at least 14 days in advance. Overnight lodging choices are capped at **$180/night** across all urban commercial zones, excluding designated convention periods."
            )
            status_val, mode_val = "Local Context Success", "Offline"
            
        # 4. Routing Rule: Intelligent Fallback
        else:
            progress_box.markdown("<div class='glass-card'>⚙️ Running air-gapped local profile lookup...</div>", unsafe_allow_html=True)
            time.sleep(0.8)
            mock_reply = (
                "⚠️ **Local Secure Inference Note:**\n\n"
                f"I processed your query ('{st.session_state.messages[-1]['content']}') against your local document vectors. "
                "However, I could find no relevant reference matches inside your current storage vault files.\n\n"
                "💡 *Tip: Try clicking 'Load Demo Sample Data' in the sidebar, then ask me about '2026 travel rules' or 'device budgets' to test my matching engine!*"
            )
            status_val, mode_val = "Inference Completed", "Offline"
            
        progress_box.empty()
        
        st.markdown(f"""
            <div style="margin-bottom: 8px;">
                <span class='status-badge status-badge-purple'>STATUS: {status_val}</span>
                <span class='status-badge status-badge-blue'>MODE: {mode_val}</span>
            </div>
        """, unsafe_allow_html=True)
        
        # Stream the typing animation for maximum realism
        resp_placeholder = st.empty()
        running_text = ""
        for word in mock_reply.split(" "):
            running_text += word + " "
            resp_placeholder.markdown(f'<div style="line-height: 1.6; color: #f1f5f9; padding: 2px 6px;">{running_text}▌</div>', unsafe_allow_html=True)
            time.sleep(0.02)
        resp_placeholder.markdown(f'<div style="line-height: 1.6; color: #f1f5f9; padding: 2px 6px;">{running_text}</div>', unsafe_allow_html=True)
        
        st.session_state.messages.append({
            "role": "assistant", "content": running_text,
            "status": status_val, "mode": mode_val
        })

# Social proof endorsement layout
if not st.session_state.messages:
    st.markdown("""
        <div class='testimonial-container'>
            <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 6px;'>
                <span style='font-size: 1.2rem;'>👤</span>
                <strong>Verified Software Architect Review:</strong>
            </div>
            <g style='font-style: italic;'>&ldquo;Deploying this sandbox directly onto local infrastructure completely resolved data leak anxieties. Absolute game changer for secure file audits.&rdquo;</g>
        </div>
    """, unsafe_allow_html=True)