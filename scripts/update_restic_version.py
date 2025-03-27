#!/usr/bin/env python3
import json
import os
import re
import subprocess
import sys
from urllib.request import urlopen

DOCKERFILE = "Dockerfile"
GITHUB_API_URL = "https://api.github.com/repos/restic/restic/releases/latest"

def get_current_version():
    with open(DOCKERFILE, "r") as f:
        for line in f:
            if line.startswith("ENV RESTIC_VERSION="):
                # Expecting: ENV RESTIC_VERSION=0.15.2
                return line.strip().split("=")[1]
    return None

def get_latest_version():
    with urlopen(GITHUB_API_URL) as response:
        data = json.loads(response.read().decode())
        # Expect tag name with a leading "v", e.g., "v0.15.2"
        tag_name = data.get("tag_name", "")
        return tag_name.lstrip("v")

def update_dockerfile(new_version):
    with open(DOCKERFILE, "r") as f:
        content = f.read()
    new_content = re.sub(r"(ENV RESTIC_VERSION=)(\S+)", r"\g<1>{}".format(new_version), content)
    with open(DOCKERFILE, "w") as f:
        f.write(new_content)
    print(f"Updated Dockerfile to version {new_version}")

def git_commit_and_push(new_version):
    try:
        subprocess.run(["git", "config", "--global", "user.email", "you@example.com"], check=True)
        subprocess.run(["git", "config", "--global", "user.name", "Your Name"], check=True)
        subprocess.run(["git", "add", DOCKERFILE], check=True)
        commit_msg = f"Update Restic version to {new_version}"
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
    except subprocess.CalledProcessError as e:
        print("Git command failed:", e)
        sys.exit(1)

def main():
    current_version = get_current_version()
    if not current_version:
        print("Current version not found in Dockerfile!")
        sys.exit(1)

    latest_version = get_latest_version()
    print(f"Current version: {current_version}")
    print(f"Latest version: {latest_version}")

    if current_version != latest_version:
        print("New version available. Updating Dockerfile...")
        update_dockerfile(latest_version)
        git_commit_and_push(latest_version)
    else:
        print("Restic is up to date.")

if __name__ == "__main__":
    main()
