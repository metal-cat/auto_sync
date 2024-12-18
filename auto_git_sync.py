bl_info = {
    "name": "Auto Git Sync",
    "blender": (2, 80, 0),
    "category": "System",
    "version": (1, 0, 0),
    "description": (
        "Automatically syncs Blender projects to a Git repository. "
        "When you save the project, the plugin will add all changes, "
        "commit them with a timestamped message, and push to the remote origin."
    ),
    "author": "demon.homeless@gmail.com",
    "warning": "",
    "wiki_url": "https://github.com/metal-cat/auto_sync",
    "tracker_url": ""
}

import bpy
import os
import subprocess

def get_project_directory():
    return bpy.path.abspath("//")

def is_git_repo(directory):
    try:
        subprocess.check_output(["git", "-C", directory, "rev-parse"])
        return True
    except subprocess.CalledProcessError:
        return False

def get_git_branch(directory):
    try:
        branch = subprocess.check_output(["git", "-C", directory, "rev-parse", "--abbrev-ref", "HEAD"]).strip().decode("utf-8")
        return branch
    except subprocess.CalledProcessError:
        return None

def generate_commit_message():
    import datetime
    now = datetime.datetime.now()
    return f"Automatic commit on {now.strftime('%Y-%m-%d %H:%M:%S')}"

def auto_sync_to_git():
    project_directory = get_project_directory()
    
    if not is_git_repo(project_directory):
        print("This is not a Git repository.")
        return
    
    branch = get_git_branch(project_directory)
    commit_message = generate_commit_message()

    try:
        subprocess.check_output(["git", "-C", project_directory, "add", "."])
        subprocess.check_output(["git", "-C", project_directory, "commit", "-m", commit_message], stderr=subprocess.STDOUT)
        subprocess.check_output(["git", "-C", project_directory, "push", "origin", branch])
        print(f"Successfully committed and pushed to {branch}.")
    except subprocess.CalledProcessError as e:
        print("Git operation failed:", e.output.decode("utf-8"))

def save_handler(dummy):
    auto_sync_to_git()

def register():
    bpy.app.handlers.save_post.append(save_handler)

def unregister():
    bpy.app.handlers.save_post.remove(save_handler)

if __name__ == "__main__":
    register()
