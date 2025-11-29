import os
import glob
import subprocess

def get_installed_apps():
    """
    Scans system directories for .desktop files to find installed applications.
    Returns a dictionary mapping lowercase app names to their Exec commands.
    """
    apps = {}
    desktop_files = []
    
    # Common directories for .desktop files
    dirs = [
        '/usr/share/applications',
        os.path.expanduser('~/.local/share/applications'),
        '/var/lib/snapd/desktop/applications' # For Snap apps
    ]
    
    for d in dirs:
        if os.path.exists(d):
            desktop_files.extend(glob.glob(os.path.join(d, '*.desktop')))
            
    for file_path in desktop_files:
        try:
            with open(file_path, 'r', errors='ignore') as f:
                name = None
                exec_cmd = None
                hidden = False
                
                for line in f:
                    line = line.strip()
                    if line.startswith('Name=') and not name:
                        name = line[5:].strip()
                    elif line.startswith('Exec=') and not exec_cmd:
                        exec_cmd = line[5:].strip()
                    elif line.startswith('NoDisplay=true') or line.startswith('Hidden=true'):
                        hidden = True
                
                if name and exec_cmd and not hidden:
                    # Clean up Exec command (remove %u, %F, etc.)
                    exec_cmd = exec_cmd.split('%')[0].strip()
                    apps[name.lower()] = exec_cmd
        except Exception:
            continue
            
    return apps

def get_projects(root_dir):
    """
    Scans the given directory for subdirectories (projects).
    Returns a dictionary mapping lowercase project names to their full paths.
    """
    projects = {}
    if not os.path.exists(root_dir):
        return projects
        
    try:
        for item in os.listdir(root_dir):
            full_path = os.path.join(root_dir, item)
            if os.path.isdir(full_path):
                projects[item.lower()] = full_path
    except Exception:
        pass
        
    return projects

def open_application(app_name, apps_dict):
    """
    Opens an application by name using the provided dictionary.
    """
    if app_name in apps_dict:
        subprocess.Popen(apps_dict[app_name], shell=True)
        return True
    return False

def open_project(project_path):
    """
    Opens a project in VS Code.
    """
    subprocess.Popen(['code', project_path])
