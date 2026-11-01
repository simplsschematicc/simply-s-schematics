import streamlit as st

# Page configuration and theme
st.set_page_config(page_title="Donut SMP Schematic Share", layout="wide", page_icon="🏗️")

st.title("🏗️ Donut SMP Custom Schematic Downloader & Sharer")
st.write("Upload your own `.litematic` or `.schem` files, categorize them, and download them with a single click!")

# Creating a permanent memory for uploaded files in the website session
if "database" not in st.session_state:
    st.session_state.database = {
        "🛡️ Bases & Stashes": [],
        "🏹 PvP Traps & Systems": [],
        "🌽 Automatic Farms": [],
        "📦 Others": []
    }

# Sidebar Settings - Upload Section
st.sidebar.header("📤 Upload New Schematic")
uploaded_file = st.sidebar.file_uploader("Choose a .litematic or .schem file:", type=["litematic", "schem"])
category_select = st.sidebar.selectbox("Choose Category for Upload:", list(st.session_state.database.keys()))
custom_details = st.sidebar.text_input("Enter schematic description (Optional):", placeholder="e.g., Unraidable obsidian vault")

# Action when user uploads a file
if st.sidebar.button("🚀 Add to Download List") and uploaded_file is not None:
    # Save the file into our website memory dynamically
    file_bytes = uploaded_file.getvalue()
    file_name = uploaded_file.name
    
    st.session_state.database[category_select].append({
        "name": file_name,
        "data": file_bytes,
        "details": custom_details if custom_details else "No description provided."
    })
    st.sidebar.success(f"Successfully added: {file_name}")

# Main Screen - View and Download Categories
st.divider()
selected_category = st.selectbox("📂 Browse Category:", list(st.session_state.database.keys()))

st.header(f"{selected_category}")

if not st.session_state.database[selected_category]:
    st.info("No schematics uploaded in this category yet. Use the sidebar on the left to upload your own files!")
else:
    for index, schem in enumerate(st.session_state.database[selected_category]):
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(f"📄 {schem['name']}")
                st.write(f"ℹ️ **Description:** {schem['details']}")
            with col2:
                st.write("") # Spacing
                st.write("") 
                # SINGLE CLICK DOWNLOAD BUTTON
                st.download_button(
                    label="📥 Download Schematic",
                    data=schem["data"],
                    file_name=schem["name"],
                    mime="application/octet-stream",
                    key=f"{schem['name']}_{index}"
                )
            st.divider()

# Instructions footer
st.info("💡 **How to use downloaded files?** Drop the downloaded `.litematic` file into your `.minecraft/schematics` folder. Open Minecraft, use the Litematica mod GUI, and load your blueprint on Donut SMP!")
