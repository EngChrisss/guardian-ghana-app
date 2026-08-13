import os

print("🔍 Checking deployment readiness...")

required = ["app.py", "requirements.txt", ".gitignore", ".streamlit/config.toml"]
for file in required:
    if os.path.exists(file):
        print(f"✅ {file}")
    else:
        print(f"❌ {file} - NEEDS CREATION")

dangerous = ["secrets.toml", "private_pages/"]
for item in dangerous:
    if os.path.exists(item):
        print(f"⚠️  {item} - MAKE SURE THIS IS IN .gitignore!")
    else:
        print(f"✅ {item} - Not found (good)")

print("\n📦 Files to upload to GitHub:")
for root, dirs, files in os.walk("."):
    # Skip hidden folders and dangerous ones
    if any(x in root for x in [".git", "__pycache__", "private_pages"]):
        continue

    for file in files:
        if not file.endswith(".toml") and file != "secrets.toml":
            print(f"  {os.path.join(root, file)}")