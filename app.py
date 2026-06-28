import os
import uuid
import time
import streamlit as st

# =====================================================================
# 🌟 STAGE 1: SET INITIAL PAGE CONFIG
# =====================================================================
st.set_page_config(
    page_title="🔒 Private Intel Vault — Local AI Knowledge Base",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="auto"  # Changed to auto to improve responsive mobile scaling
)

# 🎨 STAGE 2: INJECT EMULATED DARK IDE STYLING LAYERS (WITH MOBILE FIXES)
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
        .element-container {
            margin-bottom: 0.25rem !important;
        }
        [data-testid="stChatInput"] {
            background-color: #16191f !important;
            border: 1px solid #262c36 !important;
            border-radius: 12px !important;
            color: #ffffff !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
        }
        code {
            background-color: #1e242e !important;
            color: #f1f5f9 !important;
            border-radius: 4px !important;
            padding: 0.2rem 0.4rem !important;
            font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace !important;
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
        
        /* 📱 RESPONSIVE MOBILE FIXES FROM THE ROAST REPORT */
        @media (max-width: 768px) {
            [data-testid="stMainBlockContainer"] {
                padding: 1rem 1rem 4rem 1rem !important;
            }
            .glass-card {
                padding: 12px !important;
            }
            h1 {
                font-size: 2rem !important;
            }
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

llm_options = ["qwen2.5:7b (Demo)", "gemma4:12b (Demo)", "deepseek-r1:8b (Demo)", "llama-3.3-70b (Demo)"]
embedding_options = ["bge-large-en-v1.5", "nomic-embed-text"]

# =====================================================================
# 🧠 STAGE 4: CONTROL CENTER (SIDEBAR)
# =====================================================================
st.sidebar.markdown("<h2 style='text-align: center; margin-top:0;'>🧠 Control Center</h2>", unsafe_allow_html=True)
llm_model = st.sidebar.selectbox("Select LLM Model", llm_options, index=0)
embedding_model = st.sidebar.selectbox("Select Embedding Model", embedding_options, index=0)

st.sidebar.markdown("---")
# AUDIT FIX: Added Step 1 labeling to clarify onboarding flow entry point
st.sidebar.markdown("### 📥 Step 1: Upload Documents")
uploaded_files = st.sidebar.file_uploader("Drag & drop documents here", type=["pdf", "txt", "png", "jpg", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        if not any(f["filename"] == uploaded_file.name for f in st.session_state.indexed_files):
            st.session_state.indexed_files.append({
                "filename": uploaded_file.name, 
                "chunks": 5, 
                "format": uploaded_file.name.split('.')[-1].lower()
            })

st.sidebar.markdown("---")
st.sidebar.markdown("### 🗄️ Manage Storage Vault")

if not st.session_state.indexed_files:
    st.sidebar.info("Your local vault is currently empty.")
else:
    for f in list(st.session_state.indexed_files):
        display_name = f["filename"] if len(f["filename"]) <= 22 else f"{f['filename'][:19]}..."
        if st.sidebar.button(f"🗑️ Delete {display_name}", key=f"del_{f['filename']}"):
            st.session_state.indexed_files.remove(f)
            st.rerun()

if st.sidebar.button("🗑️ Reset Session & Clear Vault", use_container_width=True):
    st.session_state.indexed_files = []
    st.session_state.messages = []
    st.rerun()

if st.session_state.indexed_files:
    st.sidebar.markdown("#### Currently Indexed Vault Items")
    for f in st.session_state.indexed_files:
        icon = "📸" if f["format"] in ["png", "jpg", "jpeg"] else "📄"
        st.sidebar.markdown(f"<span class='status-badge'>{icon} {f['filename']} ({f['chunks']} chunks)</span>", unsafe_allow_html=True)

# =====================================================================
# 💻 STAGE 5: MAIN APP RENDERING ARCHITECTURE
# =====================================================================
# AUDIT FIX: Substituted tech jargon for business value benefits
st.markdown("<h1>🔒 Your Private Knowledge Base</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 1.2rem; color: #abb2bf; font-weight: 400;'>Chat with your private documents safely—without your data ever leaving your computer.</p>", unsafe_allow_html=True)

# AUDIT FIX: Added benefit bullets and clear privacy validation badges inside hero card
st.markdown(f"""
    <div class='glass-card'>
        <div style="margin-bottom: 12px;">
            <span class='status-badge status-badge-blue'>🛡️ 100% Local & Offline</span>
            <span class='status-badge status-badge-purple'>💎 No Subscription Required</span>
            <span class='status-badge'>📁 PDF, TXT, & Image Support</span>
        </div>
        <div style="font-size: 0.9rem; color: #98c379; font-weight: 500; border-left: 3px solid #98c379; padding-left: 10px; margin-top: 5px;">
            ✓ Privacy Certified: Zero Cloud Latency & Zero External Model Data Retention.
        </div>
    </div>
""", unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown("<p style='font-size: 0.85rem; color: #64748b; margin-bottom: 4px;'>💡 Quick start templates:</p>", unsafe_allow_html=True)
    chip_col1, chip_col2, chip_col3 = st.columns(3)
    with chip_col1:
        if st.button("🔍 Check local budget limit", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": "What is my electronic device purchase budget limit?"})
            st.rerun()
    with chip_col2:
        if st.button("🌐 Search MacBook pricing", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": "What is the latest pricing for Apple MacBook Air computers online?"})
            st.rerun()
    with chip_col3:
        if st.button("📋 Summarize vault files", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": "Give me a high-level summary of all files currently inside my local storage vault."})
            st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            st.markdown(f"""
                <div style="margin-bottom: 8px;">
                    <span class='status-badge status-badge-purple'>STATUS: {message.get("status", "Success")}</span>
                    <span class='status-badge status-badge-blue'>MODE: {message.get("mode", "Offline RAG")}</span>
                    <span class='status-badge'>REFERENCE_ID: {message.get("reference_id", "REF-UNKNOWN")}</span>
                </div>
            """, unsafe_allow_html=True)
        st.markdown(f'<div style="line-height: 1.6; color: #f1f5f9; padding: 6px 10px; white-space: pre-wrap; word-wrap: break-word;">{message["content"]}</div>', unsafe_allow_html=True)

if user_input := st.chat_input("Query local agent...", key="primary_chat_input_canvas"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.rerun()

if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    last_msg = st.session_state.messages[-1]["content"]
    
    with st.chat_message("assistant"):
        progress_box = st.empty()
        
        def show_milestone(text, subtext=""):
            sub_html = f"<div style='font-size:0.9rem; color:#abb2bf; margin-top:4px;'>{subtext}</div>" if subtext else ""
            progress_box.markdown(f"""
                <div class='glass-card' style='padding: 14px 20px; border-left: 4px solid #61afef;'>
                    <div style='color: #ffffff; font-weight: 500;'>⚙️ {text}</div>
                    {sub_html}
                </div>
            """, unsafe_allow_html=True)

        show_milestone("Querying local database contexts...")
        time.sleep(0.6)
        show_milestone("Generating tool path selection...")
        time.sleep(0.4)
        
        has_search = any(w in last_msg.lower() for w in ["search", "online", "pricing", "latest", "web"])
        
        if has_search:
            show_milestone("Searching the web...", f"Query: {last_msg}")
            time.sleep(0.8)
            show_milestone("Web results integrated. Streaming final synthesis...")
            time.sleep(0.3)
            mock_reply = "This is a simulated real-time web search response! In production, this parses live markdown structures from DuckDuckGo to match marketplace listings while respecting security parameters."
            status_val, mode_val = "Web Retrieval Success", "RAG + Web Search"
        else:
            show_milestone("Synthesizing response using local context...")
            time.sleep(0.8)
            mock_reply = f"This is a mock RAG response. Your input query ('{last_msg}') was processed against your local document vectors successfully. The device budget rule checks out smoothly."
            status_val, mode_val = "Local Context Success", "Offline RAG"

        progress_box.empty()
        ref_id = f"REF-{uuid.uuid4().hex[:6].upper()}"
        
        st.markdown(f"""
            <div style="margin-bottom: 8px;">
                <span class='status-badge status-badge-purple'>STATUS: {status_val}</span>
                <span class='status-badge status-badge-blue'>MODE: {mode_val}</span>
                <span class='status-badge'>REFERENCE_ID: {ref_id}</span>
            </div>
        """, unsafe_allow_html=True)

        resp_placeholder = st.empty()
        running_text = ""
        for word in mock_reply.split(" "):
            running_text += word + " "
            resp_placeholder.markdown(f'<div style="line-height: 1.6; color: #f1f5f9; padding: 6px 10px;">{running_text}▌</div>', unsafe_allow_html=True)
            time.sleep(0.04)
        resp_placeholder.markdown(f'<div style="line-height: 1.6; color: #f1f5f9; padding: 6px 10px;">{running_text}</div>', unsafe_allow_html=True)
        
        st.session_state.messages.append({
            "role": "assistant", "content": running_text,
            "status": status_val, "mode": mode_val, "reference_id": ref_id
        })