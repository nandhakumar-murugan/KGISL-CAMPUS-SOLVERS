"""
KiTE Campus Smart Print Queue & Token Hub (Subproject #5)
Part of KGISL-CAMPUS-SOLVERS open-source campus engineering initiative.
Led by: Bala (@Bala050814, ECE/VLSI) & Prabakar A (@prabakar09, AI&DS)
"""

import io
import random
import time
import qrcode
import streamlit as st
from PIL import Image

# Page Configuration
st.set_page_config(
    page_title="KiTE Smart Print Hub",
    page_icon="🖨️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1A73E8;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #5F6368;
        margin-bottom: 1.5rem;
    }
    .token-card {
        background: linear-gradient(135deg, #1A73E8, #34A853);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .token-id {
        font-size: 2.4rem;
        font-weight: 800;
        letter-spacing: 2px;
        font-family: monospace;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar: Campus & Facility Info
with st.sidebar:
    st.image("https://img.shields.io/badge/Campus-KGiSL_Institute_of_Technology-EA4335?style=for-the-badge", use_container_width=True)
    st.title("🖨️ Facility Directory")
    
    campus_location = st.selectbox(
        "Select Campus Print Counter",
        [
            "KiTE Central Library Print Counter (Ground Floor)",
            "KGCAS Central Amenity Center",
            "IIM Campus Express Print Corner",
            "Mech / ECE Block Digital Lab Counter"
        ]
    )
    
    st.markdown("---")
    st.markdown("### ⏱️ Live Counter Status")
    st.success("🟢 Queue Status: Normal (Est. wait < 4 mins)")
    st.info("💡 **Tip**: Upload during class hours and pick up pre-printed sheets in seconds during lunch break!")
    
    st.markdown("---")
    st.caption("Built with ❤️ by KiTE Student Builders | KGISL-CAMPUS-SOLVERS")

# Main Page Header
st.markdown('<div class="main-header">🖨️ Campus Smart Print Queue & Token Hub</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">Eliminate lunch-hour printing queues across KiTE, KGCAS, and IIM. '
    'Pre-order your prints, generate your instant claim QR code, and pick up without waiting!</div>',
    unsafe_allow_html=True
)

# Initialize Session State
if "token_history" not in st.session_state:
    st.session_state.token_history = []

# Two Column Layout
col1, col2 = st.columns([1.2, 0.8], gap="large")

with col1:
    st.subheader("📄 1. Document & Print Preferences")
    
    uploaded_file = st.file_uploader(
        "Upload Document (PDF, Word, or Images)",
        type=["pdf", "docx", "png", "jpg", "jpeg"],
        help="Upload lecture notes, assignment submissions, lab records, or project reports."
    )
    
    cfg_col1, cfg_col2 = st.columns(2)
    with cfg_col1:
        color_mode = st.radio("Color Mode", ["Black & White (₹2 / page)", "Full Color (₹10 / page)"])
        sides = st.selectbox("Page Sides", ["Double Sided (Duplex - Eco Friendly)", "Single Sided"])
    
    with cfg_col2:
        paper_size = st.selectbox("Paper Size", ["A4 (Standard Document)", "A3 (Engineering Drawing)", "Letter"])
        copies = st.number_input("Number of Copies", min_value=1, max_value=50, value=1)
    
    special_notes = st.text_input(
        "Special Instructions for Operator (Optional)",
        placeholder="e.g. Spiral binding required, staple top-left, print pages 1-12 only"
    )
    
    submit_order = st.button("🚀 Generate Print Claim Token & QR", type="primary", use_container_width=True)

with col2:
    st.subheader("🎟️ 2. Instant Pickup Token & QR")
    
    if submit_order:
        if uploaded_file is None:
            st.warning("⚠️ Please upload a document to generate your print token.")
        else:
            with st.spinner("Processing document and generating secure pickup token..."):
                time.sleep(0.6)
                
                # Generate Token ID
                rand_id = f"KITE-PRN-{random.randint(1000, 9999)}"
                token_data = {
                    "token": rand_id,
                    "filename": uploaded_file.name,
                    "size_kb": round(len(uploaded_file.getvalue()) / 1024, 1),
                    "color": color_mode,
                    "sides": sides,
                    "copies": copies,
                    "location": campus_location,
                    "timestamp": time.strftime("%I:%M %p, %d %b %Y")
                }
                st.session_state.token_history.append(token_data)
                
                # Render Visual Token
                st.markdown(f"""
                <div class="token-card">
                    <div>OFFICIAL PRINT CLAIM TOKEN</div>
                    <div class="token-id">{rand_id}</div>
                    <div>Show this code at {campus_location.split('(')[0].strip()}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Generate QR Code
                qr_payload = f"TOKEN={rand_id}|CAMPUS=KITE|FILE={uploaded_file.name}|COPIES={copies}|COLOR={color_mode}"
                qr = qrcode.QRCode(box_size=8, border=2)
                qr.add_data(qr_payload)
                qr.make(fit=True)
                qr_img = qr.make_image(fill_color="#1A73E8", back_color="white")
                
                # Display QR
                buf = io.BytesIO()
                qr_img.save(buf, format="PNG")
                buf.seek(0)
                st.image(buf, caption="Scan this QR code at the counter for instant pickup", width=220)
                
                st.success(f"✅ Order queued! File `{uploaded_file.name}` ({token_data['size_kb']} KB) ready for print preparation.")
    else:
        st.info("👉 Upload your file on the left and click **Generate Print Claim Token** to receive your counter pickup QR code.")

# Token Queue History Table
if st.session_state.token_history:
    st.markdown("---")
    st.subheader("📋 Your Recent Print Tokens")
    st.table(st.session_state.token_history)
