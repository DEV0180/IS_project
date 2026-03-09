import os
import shutil

# Clean up stuck git merge files
git_dir = r"d:\IIT KHARAGPUR\Sem6\IS Project\.git"

merge_files = ['MERGE_HEAD', 'MERGE_MODE', 'MERGE_MSG', 'COMMIT_EDITMSG', 'AUTO_MERGE']

for file in merge_files:
    file_path = os.path.join(git_dir, file)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            print(f"Removed {file}")
        except Exception as e:
            print(f"Failed to remove {file}: {e}")

print("Git state cleaned successfully")
