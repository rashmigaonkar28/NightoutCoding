import streamlit as st

# Page configuration
st.set_page_config(page_title="E-Com Data Finder", layout="wide")

# Header
st.markdown("### 🛒 E-Com Data Finder")
st.write("---")

# Three-column layout for Fetch, Filter, and Email sections
col1, col2, col3 = st.columns([1.2, 1.2, 1])

# ========== Left Column: Fetch Websites ==========
with col1:
    with st.container():
        st.subheader("Fetch Websites")
        country = st.selectbox("Country", ["Select country", "USA", "India", "UK", "Germany"])
        state_city = st.text_input("State/city keyword", "Texas")
        industry = st.text_input("Industry keyword", "Eyeglasses store")
        count = st.number_input("Count", min_value=1, max_value=1000, value=100)
        st.markdown("###")
        if st.button("🔍 Fetch Websites"):
            st.success("Websites fetched (mock action).")

# ========== Middle Column: Filter Websites ==========
with col2:
    with st.container():
        st.subheader("Filter Websites")
        domain_active = st.checkbox("✅ Domain Active")
        shopify = st.checkbox("🛍️ Only Shopify websites")
        loads_in_5s = st.checkbox("⚡ Loads within 5 secs")
        uploaded_file = st.file_uploader("Upload CSV", type="csv")
        st.markdown("###")
        if st.button("🚫 Exclude Sites & Filter"):
            st.info("Filtering done (mock action).")

# ========== Right Column: Fetch Emails ==========
with col3:
    with st.container():
        st.subheader("Fetch Email IDs")
        email_file = st.file_uploader("Drop your CSV file here", type="csv")
        st.text_input("example: Websites_filtered1.csv")
        st.markdown("###")
        if st.button("📧 Fetch Email IDs"):
            st.success("Emails extracted (mock action).")

# ========== Results Section ==========
st.markdown("---")
st.subheader("Results")
st.write("Website/Email id")
results = ["jexample1.com", "info@example2.com"]
for res in results:
    st.code(res)

st.markdown("###")
if st.button("⬇️ Export in CSV"):
    st.success("Results exported (mock action).")

# Footer
st.markdown("""<hr style="margin-top: 40px;">""", unsafe_allow_html=True)
st.caption("© 2025 Modaka Technologies Pvt. Ltd.")
