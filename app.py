import streamlit as st
import requests
import json
import base64
import os

# Page configuration
st.set_page_config(page_title="Donut SMP Schematic Share", layout="wide", page_icon="🏗️")

st.title("🏗️ Donut SMP Custom Schematic Downloader & Sharer")
st.write("Upload your own `.litematic` or `.schem` files. They will be saved permanently!")

# Fetch credentials from Render settings safely
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USER = os.getenv("GITHUB_USER")
GITHUB_REPO = "simply-s-schematics"

# Categories
CATEGORIES = ["🛡️ Bases & Stashes", "🏹 PvP Traps & Systems", "🌽 Automatic Farms", "📦 Others"]

# Helper function to fetch database from GitHub
def get_github_db():
    url = f"https://github.com{GITHUB_USER}/{GITHUB_REPO}/contents/database.json"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        content = res.json()
        file_content = base64.b64decode(content["content"]).decode("utf-8")
        return json.loads(file_content), content["sha"]
    return {cat: [] for cat in CATEGORIES}, None

# Helper function to save database to GitHub
def save_to_github(db_data, current_sha=None):
    url = f"https://github.com{GITHUB_USER}/{GITHUB_REPO}/contents/database.json"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    updated_content = base64.b64encode(json.dumps(db_data, indent=4).encode("utf-8")).decode("utf-8")
    
    payload = {
        "message": "Update schematic database",
        "content": updated_content
    }
    if current_sha:
        payload["sha"] = current_sha
        
    res = requests.put(url, headers=headers, json=payload)
    return res.status_code in [200, 201]

# Load permanent data
if not GITHUB_TOKEN or not GITHUB_USER:
    st.error("System Error: GitHub Credentials missing in Render Environment Settings.")
    db, db_sha = {cat: [] for cat in CATEGORIES}, None
else:
    db, db_sha = get_github_db()

# Sidebar - Upload Section
st.sidebar.header("📤 Upload New Schematic")
uploaded_file = st.sidebar.file_uploader("Choose a .litematic or .schem file:", type=["litematic", "schem"])
category_select = st.sidebar.selectbox("Choose Category for Upload:", CATEGORIES)
custom_details = st.sidebar.text_input("Enter schematic description (Optional):", placeholder="e.g., Unraidable obsidian vault")

if st.sidebar.button("🚀 Add to Download List") and uploaded_file is not None:
    file_bytes = uploaded_file.getvalue()
    file_name = uploaded_file.name
    encoded_file = base64.b64encode(file_bytes).decode("utf-8")
    
    if not any(item['name'] == file_name for item in db[category_select]):
        db[category_select].append({
            "name": file_name,
            "data": encoded_file,
            "details": custom_details if custom_details else "No description provided."
        })
        
        if save_to_github(db, db_sha):
            st.sidebar.success(f"Successfully saved permanently: {file_name}")
            st.io_cleanup() if hasattr(st, "io_cleanup") else None
            st.rerun()
        else:
            st.sidebar.error("Failed to save to cloud storage. Check token permissions.")
    else:
        st.sidebar.warning("A file with this name already exists in this category.")

# Main Screen
st.divider()
selected_category = st.selectbox("📂 Browse Category:", CATEGORIES)
st.header(f"{selected_category}")

if not db[selected_category]:
    st.info("No schematics uploaded in this category yet. Use the sidebar on the left to upload your own files!")
else:
    for index, schem in enumerate(db[selected_category]):
        with st.container():
            col1, col2 = st.columns()
            with col1:
                st.subheader(f"📄 {schem['name']}")
                st.write(f"ℹ️ **Description:** {schem['details']}")
            with col2:
                st.write("")
                st.write("")
                raw_file_bytes = base64.b64decode(schem["data"])
                st.download_button(
                    label="📥 Download Schematic",
                    data=raw_file_bytes,
                    file_name=schem["name"],
                    mime="application/octet-stream",
                    key=f"{schem['name']}_{index}"
                )
            st.divider()

st.info("💡 **How to use downloaded files?** Drop the downloaded `.litematic` file into your `.minecraft/schematics` folder. Open Minecraft, use the Litematica mod GUI, and load your blueprint on Donut SMP!")
