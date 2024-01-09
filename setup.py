import os
import subprocess
import sys
import venv

def run_command(command, cwd=None):
    print(f"Running command: {' '.join(command)}")
    subprocess.check_call(command, cwd=cwd)

def main(commit_hash):
    repo_url = "https://github.com/Opentrons/opentrons"  # Replace with your repository URL
    repo_name = repo_url.split("/")[-1]

    print("Cloning the repository...")
    run_command(["git", "clone", repo_url, "--depth", "1", "--branch", commit_hash])

    print(f"Creating a virtual environment named '{commit_hash}'...")
    venv_dir = os.path.join(".venv_", commit_hash)  # Venv directory in the current folder
    venv.create(venv_dir, with_pip=True)

    pip_install_cmd = [os.path.join(venv_dir, "bin", "python"), "-m", "pip", "install", "-U"]

    print("Installing dependencies...")
    run_command(pip_install_cmd + ["./opentrons/shared-data/python"], cwd=repo_name)
    run_command(pip_install_cmd + ["./opentrons/hardware[flex]"], cwd=repo_name)
    run_command(pip_install_cmd + ["./opentrons/api"], cwd=repo_name)
    run_command(pip_install_cmd + ["pandas==1.4.3"], cwd=repo_name)

    print("Setup complete.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <commit_hash>")
        sys.exit(1)
    
    commit_hash = sys.argv[1]
    main(commit_hash)
