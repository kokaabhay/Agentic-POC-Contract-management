import subprocess

result = subprocess.run(["ipconfig", "/flushdns"], capture_output=True, text=True)

print(result.stdout)
print(result.stderr)