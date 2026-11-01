# Helper function to fetch database from GitHub
def get_github_db():
    # DOĞRU API ADRESİ: ://github.com...
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
    # DOĞRU API ADRESİ: ://github.com...
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
