import streamlit as st
import requests
import json
from typing import List, Dict, Any
import datetime

# Page configuration
st.set_page_config(
    page_title="Wall of Fame - Customer Details",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for a clean, modern look
st.markdown("""
<style>
    html, body, .main {
        font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
        background: #f7f7fa;
        padding: 0;
        margin: 0;
    }
    
    .main {
        padding-top: 0.5rem;
        max-width: 100vw;
    }
    
    .header-container {
        display: flex;
        align-items: center;
        justify-content: flex-start;
        gap: 0.7rem;
        background: none;
        margin-bottom: 1rem;
        padding: 0.5rem 0.5rem 0 0.5rem;
    }
    .header-logo {
        font-size: 2.2rem;
        background: linear-gradient(135deg, #6ee7b7 0%, #3b82f6 100%);
        border-radius: 50%;
        width: 2.7rem;
        height: 2.7rem;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #fff;
        box-shadow: 0 2px 8px rgba(59,130,246,0.10);
    }
    .header-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #222;
        margin: 0;
    }
    .header-desc {
        font-size: 1rem;
        color: #555;
        margin: 0 0 0 0.2rem;
    }
    .customer-card {
        background: #fff;
        border-radius: 18px;
        padding: 1.2rem 1rem 1.5rem 1rem;
        margin: 1.2rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.07);
        border-left: 4px solid #3b82f6;
        position: relative;
        display: flex;
        flex-direction: column;
        gap: 0.7rem;
        transition: box-shadow 0.2s;
    }
    .customer-badge {
        position: absolute;
        top: -1.1rem;
        left: -1.1rem;
        background: #3b82f6;
        color: #fff;
        border-radius: 50%;
        width: 2.2rem;
        height: 2.2rem;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 1.1rem;
        box-shadow: 0 2px 8px rgba(59,130,246,0.10);
    }
    .remove-btn {
        position: absolute;
        top: 0.7rem;
        right: 0.7rem;
        background: #fca5a5;
        color: #fff;
        border: none;
        border-radius: 50%;
        width: 2rem;
        height: 2rem;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
        cursor: pointer;
        transition: background 0.2s;
    }
    .remove-btn:hover {
        background: #ef4444;
    }
    .input-label {
        font-size: 1rem;
        color: #333;
        font-weight: 500;
        margin-bottom: 0.2rem;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }
    .input-icon {
        font-size: 1.1rem;
        color: #3b82f6;
    }
    .avatar-preview {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid #3b82f6;
        margin-bottom: 0.5rem;
        background: #f3f4f6;
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    .add-customer-btn {
        background: #3b82f6;
        color: #fff;
        border: none;
        border-radius: 12px;
        padding: 0.8rem 1.2rem;
        font-weight: 600;
        font-size: 1.1rem;
        margin: 0.5rem 0 1.2rem 0;
        width: 100%;
        box-shadow: 0 2px 8px rgba(59,130,246,0.08);
        transition: background 0.2s;
    }
    .add-customer-btn:disabled {
        background: #dbeafe;
        color: #93c5fd;
        cursor: not-allowed;
    }
    .progress-bar {
        width: 100%;
        height: 12px;
        background: #e5e7eb;
        border-radius: 8px;
        margin: 1rem 0 0.5rem 0;
        overflow: hidden;
    }
    .progress-bar-inner {
        height: 100%;
        background: linear-gradient(90deg, #6ee7b7 0%, #3b82f6 100%);
        border-radius: 8px;
        transition: width 0.3s;
    }
    .fab-submit {
        position: fixed;
        bottom: 1.2rem;
        left: 50%;
        transform: translateX(-50%);
        background: linear-gradient(135deg, #6ee7b7 0%, #3b82f6 100%);
        color: #fff;
        border: none;
        border-radius: 30px;
        padding: 1.1rem 2.2rem;
        font-size: 1.2rem;
        font-weight: 700;
        box-shadow: 0 4px 24px rgba(59,130,246,0.18);
        z-index: 1000;
        transition: background 0.2s, box-shadow 0.2s;
    }
    .fab-submit:disabled {
        background: #d1fae5;
        color: #6ee7b7;
        cursor: not-allowed;
        box-shadow: none;
    }
    .toast {
        position: fixed;
        top: 1.2rem;
        left: 50%;
        transform: translateX(-50%);
        min-width: 220px;
        background: #fff;
        color: #222;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.13);
        padding: 1rem 1.5rem;
        z-index: 2000;
        font-weight: 600;
        text-align: center;
        border-left: 5px solid #3b82f6;
        animation: fadein 0.4s;
    }
    @keyframes fadein {
        from { opacity: 0; top: 0.5rem; }
        to { opacity: 1; top: 1.2rem; }
    }
    .footer {
        text-align: center;
        color: #888;
        padding: 0.7rem 0 0.5rem 0;
        font-size: 0.95rem;
    }
    @media (max-width: 700px) {
        .main, .header-container, .customer-card {
            padding-left: 0.2rem !important;
            padding-right: 0.2rem !important;
        }
        .fab-submit {
            width: 95vw;
            left: 2.5vw;
            transform: none;
        }
    }
    @media (max-width: 500px) {
        .header-title { font-size: 1.1rem; }
        .customer-card { padding: 0.7rem 0.2rem 1.2rem 0.2rem; }
        .fab-submit { font-size: 1.05rem; padding: 0.9rem 1.2rem; }
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-container">
    <div class="header-logo">🏆</div>
    <div>
        <div class="header-title">Wall of Fame</div>
        <div class="header-desc">Add up to 5 customers at once!</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Configuration section (sidebar, but minimal)
n8n_endpoint = "https://n8n-aaagentive.onrender.com/webhook/254bc938-1e68-4c92-86b3-6caab41a20ce"

# Initialize session state for customer data
if 'customers' not in st.session_state:
    st.session_state.customers = [{}]

# Add/Remove customer logic
if 'num_customers' not in st.session_state:
    st.session_state.num_customers = 1

def add_customer():
    if st.session_state.num_customers < 5:
        st.session_state.customers.append({})
        st.session_state.num_customers += 1

def remove_customer(idx):
    if st.session_state.num_customers > 1:
        st.session_state.customers.pop(idx)
        st.session_state.num_customers -= 1

# Function to validate customer data
def validate_customer(customer_data: Dict[str, Any]) -> List[str]:
    """Validate customer data and return list of errors"""
    errors = []
    if not customer_data.get('name', '').strip():
        errors.append("Name is required")
    if not customer_data.get('image_file'):
        errors.append("Image is required")
    if not customer_data.get('add_date'):
        errors.append("Date is required")
    return errors

# Function to send data to n8n
def send_to_n8n(customers_data: List[Dict[str, Any]], endpoint: str) -> bool:
    """Send customer data to n8n endpoint as multipart/form-data with image as file."""
    try:
        for customer in customers_data:
            data = {
                "name": customer["name"],
                "comment": customer["comment"],
                "add_date": customer["add_date"],
            }
            image_file = customer.get("image_file")
            files = {"photo": (image_file.name, image_file, image_file.type)} if image_file else None
            response = requests.post(endpoint, data=data, files=files)
            if response.status_code != 200:
                st.error(f"Failed to send data for {customer['name']}. Status code: {response.status_code}")
                return False
        return True
    except Exception as e:
        st.error(f"Error: {e}")
        return False

# Main form
st.markdown("### 📝 Add Customer Details")

# Number of customers selector
num_customers = st.session_state.num_customers
customers_data = []
valid_count = 0

for i in range(num_customers):
    st.markdown(f"""
    <div class="customer-card">
        <div class="customer-badge">{i+1}</div>
    """, unsafe_allow_html=True)
    # Remove button (Streamlit-native)
    if num_customers > 1:
        remove_btn_key = f"remove_customer_{i}"
        if st.button("✖️ Remove", key=remove_btn_key):
            st.session_state.customers.pop(i)
            st.session_state.num_customers -= 1
            st.rerun()
    name = st.text_input(
        f"Name*",
        key=f"name_{i}",
        placeholder="Enter customer name",
        help="Customer's full name (required)"
    )
    st.markdown(f'<div class="input-label"><span class="input-icon">👤</span>Name*</div>', unsafe_allow_html=True)
    comment = st.text_area(
        f"Comment",
        key=f"comment_{i}",
        placeholder="Optional comment or testimonial",
        help="Optional customer comment or testimonial",
        height=80
    )
    st.markdown(f'<div class="input-label"><span class="input-icon">💬</span>Comment</div>', unsafe_allow_html=True)
    # Date field for when to add to main wall of fame
    add_date = st.date_input(
        f"Date to add to Wall of Fame*",
        key=f"date_{i}",
        value=datetime.date.today(),
        help="Select the date when this customer should appear on the main wall of fame."
    )
    st.markdown(f'<div class="input-label"><span class="input-icon">📅</span>Date to add*</div>', unsafe_allow_html=True)
    image_file = st.file_uploader(
        f"Image*",
        key=f"image_{i}",
        type=['png', 'jpg', 'jpeg'],
        help="Upload customer image (required)"
    )
    st.markdown(f'<div class="input-label"><span class="input-icon">📷</span>Image*</div>', unsafe_allow_html=True)
    if image_file:
        st.image(image_file, caption=f"Customer {i+1} Image", width=150)
    customer_data = {
        'name': name.strip() if name else '',
        'comment': comment.strip() if comment else '',
        'add_date': str(add_date),
        'image_file': image_file
    }
    errors = validate_customer(customer_data)
    if not errors:
        valid_count += 1
    customers_data.append(customer_data)
    st.markdown("</div>", unsafe_allow_html=True)

# Add customer button (Streamlit-native)
col_add, col_spacer = st.columns([4,1])
with col_add:
    if num_customers < 5:
        if st.button("➕ Add another customer", key="add_customer_btn"):
            st.session_state.customers.append({})
            st.session_state.num_customers += 1
            st.rerun()

# Progress bar
progress = int((valid_count / num_customers) * 100) if num_customers else 0
st.markdown(f'''
<div class="progress-bar">
    <div class="progress-bar-inner" style="width: {progress}%"></div>
</div>
''', unsafe_allow_html=True)
st.markdown(f'<div style="text-align:center;font-size:1rem;color:#3b82f6;font-weight:600;">{valid_count} of {num_customers} ready</div>', unsafe_allow_html=True)

# Floating submit button
submit_disabled = not all(validate_customer(c) == [] for c in customers_data)
submit_btn = st.button("🚀 Submit to Wall of Fame", key="submit", disabled=submit_disabled)
if submit_btn:
    with st.spinner('Submitting customer details...'):
        success = send_to_n8n(customers_data, n8n_endpoint)
    if success:
        st.session_state.customers = [{}]
        st.session_state.num_customers = 1
        st.markdown('''
<div style="max-width: 420px; margin: 2rem auto; padding: 2rem 1rem; background: #f6fff7; border: 1px solid #b6e7c9; border-radius: 12px; text-align: center; box-shadow: 0 2px 12px rgba(16,185,129,0.07);">
  <div style="font-size:2.5rem;">🎉</div>
  <h2 style="color:#166534; margin-bottom:0.5rem;">Submission Successful!</h2>
  <div style="color:#166534; font-size:1.1rem;">All customer details have been submitted.<br>Thank you!</div>
</div>
''', unsafe_allow_html=True)
        st.stop()
    else:
        st.markdown('<div class="toast" style="border-left-color:#ef4444;">❌ Submission failed. Check your endpoint and try again.</div>', unsafe_allow_html=True)

# Minimal footer
st.markdown('<div class="footer">🌟 Wall of Fame Tool for <strong>bogartman.com</strong> &mdash; Built with ❤️ using Streamlit</div>', unsafe_allow_html=True)