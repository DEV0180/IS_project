import subprocess
import sys
import os

os.chdir(r'd:\IIT KHARAGPUR\Sem6\IS Project')

# Commands to execute
commands = [
    (["C:\\Program Files\\Git\\bin\\git.exe", "pull", "origin", "main", "--rebase"], "Pulling from remote"),
    (["C:\\Program Files\\Git\\bin\\git.exe", "add", "worl.ipynb"], "Adding worl.ipynb"),
    (["C:\\Program Files\\Git\\bin\\git.exe", "commit", "-m", "Final: Sleep quality scoring notebook"], "Committing"),
    (["C:\\Program Files\\Git\\bin\\git.exe", "push", "-u", "origin", "main"], "Pushing to GitHub"),
]

for cmd, desc in commands:
    print(f"\n{desc}...")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    print("STDOUT:", result.stdout[:200] if result.stdout else "(empty)")
    print("STDERR:", result.stderr[:200] if result.stderr else "(empty)")
    print("Return code:", result.returncode)

print("\n✅ Done!")
