import subprocess

def get_current_branch():
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"], 
        capture_output=True, text=True, check=True
    )
    return result.stdout.strip()