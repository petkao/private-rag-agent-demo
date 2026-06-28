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
    initial_sidebar_state="auto"
)

# 🎨 STAGE 2: INJECT EMULATED DARK IDE STYLING LAYERS
st.markdown("""
    <style>
        .stApp {
            background-color: #0d0f12 !important;
            color: #e2e8f0 !important;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        }
        [data-testid="stMainBlockContainer"] {
            max-width: 840px !important;
            padding: 1rem 2rem 5rem 2rem !important;
            margin: 0 auto !important;
        }
        [data-testid="stSidebarUserContent"] {
            padding-top: 1rem !important;
        }
        [data-testid="stSidebar"] {
            background-color: #16191f !important;
            border-right: 1px solid #262c36 !important;
        }
        [data-testid="stVerticalBlock"] {
            gap: 0.75rem !important;
        }
        [data-testid="stChatInput"] {
            background-color: #16191f !important;
            border: 1px solid #262c36 !important;
            border-radius: 12px !important;
            color: #ffffff !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
        }
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
        .stApp {
            font-family: 'Outfit', sans-serif;
            background: linear-gradient(135deg, #090a0f 0%, #11131e 50%, #1a1528 100%) !important;
        }
        .stMarkdown p, .stMarkdown li, .stMarkdown span {
            color: #f1f5f9 !important;
        }
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
            color: #F0F2F6 !important;
            font-weight: 700 !important;
        }
        div[data-testid="stSidebar"] {
            background: rgba(13, 15, 24, 0.85) !important;
            backdrop-filter: blur(20px);
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }
        .glass-card {
            background: rgba(25, 28, 41, 0.6);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 20px;
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
        h1, h2, h3 {
            font-family: 'Outfit', sans-serif;
            font-weight: 700 !important;
            background: linear-gradient(90deg, #61afef, #c678dd);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        section[data-testid="stFileUploader"] {
            background-color: rgba(20, 22, 33, 0.5) !important;
            border: 2px dashed rgba(255, 255, 255, 0.15) !important;
            border-radius: 12px !important;
            padding: 15px !important;
        }
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
        
        /* Custom styled template chips */
        .div-chip-button button {
            background-color: #1e242e !important;
            border: 1px solid #262c36 !important;
            color: #e2e8f0 !important;
        }
        
        @media (max-width: 768px) {
            [data-testid="stMainBlockContainer"] { padding: 1rem !important; }
            h1 { font-size: 2rem !important; }
        }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# 🛠️ STAGE 3: DEMO STATE CONFIGURATIONS
# =====================================================================
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []
if "indexed_files" not in st.session_state:
    st.session_state.indexed_files = [
        {"filename": "personal_profile.txt", "chunks": 3, "format": "txt"},
        {"filename": "hardware_specs.pdf", "chunks": 14, "format": "pdf"}
    ]

llm_options = ["qwen2.5:7b (Demo)", "gemma4:12b (Demo)", "deepseek-r1:8b (Demo)"]
embedding_options = ["bge-large-en-v1.5", "nomic-embed-text"]

# =====================================================================
# 🧠 STAGE 4: CONTROL CENTER (SIDEBAR)
# =====================================================================
st.sidebar.markdown("<h2 style='text-align: center; margin-top:0;'>🔒 Vault Manager</h2>", unsafe_allow_html=True)

# AUDIT FIX: Hidden the complex technical model dropdown selectors behind an expander
with st.sidebar.expander("⚙️ Advanced Engine Settings", expanded=False):
    llm_model = st.selectbox("Select LLM Model", llm_options, index=0)
    embedding_model = st.selectbox("Select Embedding Model", embedding_options, index=0)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📥 Step 1: Add Local Files")
uploaded_files = st.sidebar.file_uploader("Drop project files here", type=["pdf", "txt", "png", "jpg"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        if not any(f["filename"] == uploaded_file.name for f in st.session_state.indexed_files):
            st.session_state.indexed_files.append({
                "filename": uploaded_file.name, "chunks": 5, "format": uploaded_file.name.split('.')[-1].lower()
            })

st.sidebar.markdown("---")
st.sidebar.markdown("### 🗄️ Your Files")

if not st.session_state.indexed_files:
    st.sidebar.info("Your local vault is currently empty.")
else:
    for f in list(st.session_state.indexed_files):
        display_name = f["filename"] if len(f["filename"]) <= 22 else f"{f['filename'][:19]}..."
        if st.sidebar.button(f"🗑️ Remove {display_name}", key=f"del_{f['filename']}"):
            st.session_state.indexed_files.remove(f)
            st.rerun()

if st.session_state.indexed_files:
    st.sidebar.markdown("#### Ready to Chat")
    for f in st.session_state.indexed_files:
        icon = "📄"
        st.sidebar.markdown(f"<span class='status-badge'>{icon} {f['filename']}</span>", unsafe_allow_html=True)

# =====================================================================
# 💻 STAGE 5: MAIN APP RENDERING ARCHITECTURE
# =====================================================================
# AUDIT FIX: Upgraded copy to focus heavily on the ultimate security result
st.markdown("<h1>🔒 Chat with your files without ever leaking data</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 1.1rem; color: #abb2bf;'>A secure, air-gapped environment running completely on your local computer infrastructure.</p>", unsafe_allow_html=True)

# AUDIT FIX: Transformed empty space into a clear "Capability vs Benefit" block
if not st.session_state.messages:
    st.markdown(f"""
        <div class='glass-card'>
            <div style="margin-bottom: 12px;">
                <span class='status-badge status-badge-blue'>🛡️ 100% Offline Architecture</span>
                <span class='status-badge status-badge-purple'>🔒 Enterprise Privacy Guarantee</span>
            </div>
            <div class='benefit-card'>
                <div style='font-weight: 600; color: #61afef; font-size: 1.05rem;'>💻 Runs Fully on Apple Silicon</div>
                <div style='font-size: 0.95rem; color: #abb2bf; margin-top: 4px;'>Because your vector search paths and open-weight models execute locally inside your physical machine, your company intellectual property, documents, and search metrics never pass through a third-party cloud.</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<p style='font-size: 0.9rem; color: #64748b; margin-bottom: 8px;'>💡 What do you want to learn today?</p>", unsafe_allow_html=True)
    chip_col1, chip_col2, chip_col3 = st.columns(3)
    with chip_col1:
        if st.button("🔍 Check local budget limit", use_container_width=True, key="chip1"):
            st.session_state.messages.append({"role": "user", "content": "What is my electronic device purchase budget limit?"})
            st.rerun()
    with chip_col2:
        if st.button("🌐 Search MacBook pricing", use_container_width=True, key="chip2"):
            st.session_state.messages.append({"role": "user", "content": "What is the latest pricing for Apple MacBook Air computers online?"})
            st.rerun()
    with chip_col3:
        if st.button("📋 Summarize vault files", use_container_width=True, key="chip3"):
            st.session_state.messages.append({"role": "user", "content": "Give me a high-level summary of all files currently inside my local storage vault."})
            st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            st.markdown(f"""
                <div style="margin-bottom: 8px;">
                    <span class='status-badge status-badge-purple'>STATUS: {message.get("status", "Success")}</span>
                    <span class='status-badge status-badge-blue'>MODE: {message.get("mode", "Offline")}</span>
                </div>
            """, unsafe_allow_html=True)
        st.markdown(f'<div style="line-height: 1.6; color: #f1f5f9; padding: 6px id=text;">{message["content"]}</div>', unsafe_allow_html=True)

if user_input := st.chat_input("Ask your private agent anything...", key="chat_input"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.rerun()

if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    last_msg = st.session_state.messages[-1]["content"]
    with st.chat_message("assistant"):
        progress_box = st.empty()
        progress_box.markdown("<div class='glass-card'>⚙️ Running local context match query...</div>", unsafe_allow_html=True)
        time.sleep(0.7)
        progress_box.empty()
        
        mock_reply = f"This is a local secure model inference summary. Your document vectors parsed '{last_msg}' successfully within your physical drive parameters without throwing any remote cloud exceptions."
        
        st.markdown("""
            <div style="margin-bottom: 8px;">
                <span class='status-badge status-badge-purple'>STATUS: Local Context Success</span>
                <span class='status-badge status-badge-blue'>MODE: Offline</span>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f'<div style="line-height: 1.6; color: #f1f5f9; padding: 6px;">{mock_reply}</div>', unsafe_allow_html=True)
        
        st.session_state.messages.append({
            "role": "assistant", "content": mock_reply,
            "status": "Local Context Success", "mode": "Offline"
        })