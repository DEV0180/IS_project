import subprocess

result = subprocess.run(
    ["C:\\Program Files\\Git\\bin\\git.exe", "log", "--oneline", "-3"],
    cwd=r"d:\IIT KHARAGPUR\Sem6\IS Project",
    capture_output=True,
    text=True
)

print("Recent commits:")
print(result.stdout)
