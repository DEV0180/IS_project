#!/usr/bin/env python
import subprocess
import os

os.chdir(r"d:\IIT KHARAGPUR\Sem6\IS Project")

git_exe = r"C:\Program Files\Git\bin\git.exe"

print("1. Adding worl.ipynb...")
result = subprocess.run([git_exe, "add", "worl.ipynb"], capture_output=True, text=True)
print(result.stdout, result.stderr)

print("\n2. Committing changes...")
result = subprocess.run([git_exe, "commit", "-m", "Final update: Sleep quality scoring with all metrics"], capture_output=True, text=True)
print(result.stdout, result.stderr)

print("\n3. Pulling from remote...")
result = subprocess.run([git_exe, "pull", "origin", "main", "--no-edit"], capture_output=True, text=True)
print(result.stdout, result.stderr)

print("\n4. Pushing to GitHub...")
result = subprocess.run([git_exe, "push", "origin", "main", "-v"], capture_output=True, text=True)
print(result.stdout, result.stderr)

print("\nDone!")
