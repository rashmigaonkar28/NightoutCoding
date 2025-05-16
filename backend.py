import streamlit as st
import pandas as pd
import requests
import time
import re
from bs4 import BeautifulSoup
from serpapi import GoogleSearch

# Configuration
st.set_page_config(page_title="E-Com Data Finder", layout="wide")
SERPAPI_KEY = "52b390467ad4417103c1776da98395e3d478cddd04ceea75f46bcbb9aca0a234"

# ========== BACKEND FUNCTIONS ==========

def fetch_websites(state, industry, country, count=100):
    query = f"{industry} in {state}, {country}"
    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPAPI_KEY,
        "num": min(count, 100),
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    links = [r.get("link") for r in results.get("organic_results", []) if r.get("link")]
    return links[:count]

def is_active(url):
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except:
        return False

def is_shopify(url):
    try:
        response = requests.get(url, timeout=5)
        return "shopify" in response.text.lower()
    except:
        return False

def loads_within_5s(url):
    try:
        start = time.time()
        requests.get(url, timeout=5)
        return (time.time() - start) < 5
    except:
        return False

def apply_filters(websites, active=False, shopify=False, fast=False):
    filtered = []
    for site in websites:
        if active and not is_active(site):
            continue
        if shopify and not is_shopify(site):
            continue
        if fast and not loads_within_5s(site):
            continue
        filtered.append(site)
    return filtered

def extract_emails_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()
        emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
        return list(set(emails))
    except:
        return []

# ========== UI ==========

st.markdown("### 🛒 E-Com Data Finder")
st.write("---")
col1, col2, col3 = st.columns([1.2, 1.2, 1])

# Fetch Websites Block
with col1:
    st.subheader("Fetch Websites")
    country = st.selectbox("Country", ["Select country", "USA", "India", "UK", "Germany"])
    state_city = st.text_input("State/city keyword", "Texas")
    industry = st.text_input("Industry keyword", "Eyeglasses store")
    count = st.number_input("Count", min_value=1, max_value=1000, value=100)
    if st.button("🔍 Fetch Websites"):
        if country == "Select country":
            st.error("Please select a valid country.")
        else:
            websites = fetch_websites(state_city, industry, country, count)
            st.session_state["websites"] = websites
            st.success(f"Fetched {len(websites)} websites.")
            st.write(websites)

            # ✅ Save raw CSV immediately after fetch
            raw_df = pd.DataFrame(websites, columns=["website"])
            raw_csv = raw_df.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Download All Websites", raw_csv, "websites_raw.csv", "text/csv")

# Filter Websites Block
with col2:
    st.subheader("Filter Websites")
    domain_active = st.checkbox("✅ Domain Active")
    shopify = st.checkbox("🛍️ Only Shopify websites")
    loads_in_5s = st.checkbox("⚡ Loads within 5 secs")

    if st.button("🚫 Exclude Sites & Filter"):
        sites_to_filter = st.session_state.get("websites", [])
        if not sites_to_filter:
            st.warning("No websites found. Please fetch first.")
        else:
            filtered_sites = apply_filters(sites_to_filter, domain_active, shopify, loads_in_5s)
            st.session_state["filtered"] = filtered_sites
            st.success(f"{len(filtered_sites)} sites remaining after filters.")
            st.write(filtered_sites)

            # ✅ Save filtered CSV after filter
            filtered_df = pd.DataFrame(filtered_sites, columns=["website"])
            filtered_csv = filtered_df.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Download Filtered CSV", filtered_csv, "filtered_websites.csv", "text/csv")

# Email Extraction Block
with col3:
    st.subheader("Fetch Email IDs")
    email_file = st.file_uploader("Drop your filtered CSV here", type="csv")
    st.text_input("example: filtered_websites.csv")
    if st.button("📧 Fetch Email IDs"):
        if email_file:
            uploaded_df = pd.read_csv(email_file)
            results = []
            for url in uploaded_df.iloc[:, 0]:
                emails = extract_emails_from_url(url)
                for email in emails:
                    results.append({"website": url, "email": email})
            result_df = pd.DataFrame(results)
            st.session_state["email_results"] = result_df
            st.write(result_df)
        else:
            st.error("Please upload a filtered CSV file.")

# Display Email Results
st.markdown("---")
st.subheader("Results")
if "email_results" in st.session_state:
    st.dataframe(st.session_state["email_results"])
    email_csv = st.session_state["email_results"].to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Export Emails CSV", email_csv, "emails.csv", "text/csv")

# Footer
st.markdown("<hr style='margin-top: 40px;'>", unsafe_allow_html=True)
st.caption("© 2025 Modaka Technologies Pvt. Ltd.")
