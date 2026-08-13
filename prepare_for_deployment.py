import os
import shutil

print("🔒 Preparing for secure deployment...")

# Create private folder if it doesn't exist
if not os.path.exists("private_pages"):
    os.makedirs("private_pages")

# Move sensitive pages
sensitive_pages = ["2_Investor_Pitch.py", "3_Government_Portal.py"]
for page in sensitive_pages:
    if os.path.exists(f"pages/{page}"):
        shutil.move(f"pages/{page}", f"private_pages/{page}")
        print(f"✅ Moved {page} to private folder")

# Rename One-Pager to be first page
if os.path.exists("pages/4_One_Pager.py"):
    os.rename("pages/4_One_Pager.py", "pages/1_📋_One_Pager.py")
    print("✅ Renamed One-Pager to be public page")

print("\n✅ Deployment ready!")
print("Public pages:")
print("  • app.py (Main demo)")
print("  • pages/1_📋_One_Pager.py (Marketing)")
print("\nPrivate pages (kept locally):")
print("  • private_pages/2_Investor_Pitch.py")
print("  • private_pages/3_Government_Portal.py")