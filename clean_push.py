import subprocess
import os

os.chdir(r'd:\IIT KHARAGPUR\Sem6\IS Project')

# Abort rebase
print("Aborting rebase...")
result = subprocess.run(["C:\\Program Files\\Git\\bin\\git.exe", "rebase", "--abort"], capture_output=True, text=True)
print(result.stdout, result.stderr)

# Reset to remote
print("\nFetching from remote...")
result = subprocess.run(["C:\\Program Files\\Git\\bin\\git.exe", "fetch", "origin"], capture_output=True, text=True)
print(result.stdout, result.stderr)

# Checkout main and reset
print("\nChecking out main...")
result = subprocess.run(["C:\\Program Files\\Git\\bin\\git.exe", "checkout", "main"], capture_output=True, text=True)
print(result.stdout, result.stderr)

print("\nResetting to origin/main...")
result = subprocess.run(["C:\\Program Files\\Git\\bin\\git.exe", "reset", "--hard", "origin/main"], capture_output=True, text=True)
print(result.stdout, result.stderr)

# Now add, commit, push
print("\nAdding worl.ipynb...")
result = subprocess.run(["C:\\Program Files\\Git\\bin\\git.exe", "add", "worl.ipynb"], capture_output=True, text=True)
print("Return code:", result.returncode)

print("\nCommitting...")
result = subprocess.run(["C:\\Program Files\\Git\\bin\\git.exe", "commit", "-m", "Final: Sleep quality scoring with HRV, efficiency, deep sleep, REM"], capture_output=True, text=True)
print(result.stdout)
print("Return code:", result.returncode)

print("\nPushing to GitHub...")
result = subprocess.run(["C:\\Program Files\\Git\\bin\\git.exe", "push", "origin", "main"], capture_output=True, text=True)
print(result.stdout, result.stderr)
print("Return code:", result.returncode)

print("\n✅ Complete!")
