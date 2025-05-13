import subprocess
import requests
import datetime
import os

class GitHubUploader:
    """Class to push code and data to GitHub"""
    def __init__(self, username, email, repo_url, pat):
        self.username = username
        self.email = email
        self.repo_url = repo_url
        self.pat = pat

    def save_code_to_file(self, code_content, filename="wealthsync.py"):
        """Save code to a .py file"""
        try:
            # Add timestamp comment to ensure file changes
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            code_content = f"# Last updated: {timestamp}\n{code_content}"
            
            with open(filename, "w") as f:
                f.write(code_content)
            print(f"Created file {filename} in working directory")
            return True
        except Exception as e:
            print(f"Error saving code to file: {e}")
            return False

    def check_pat_validity(self):
        """Check PAT validity"""
        try:
            headers = {
                "Authorization": f"token {self.pat}",
                "Accept": "application/vnd.github.v3+json"
            }
            response = requests.get("https://api.github.com/user", headers=headers)
            
            if response.status_code == 200:
                print(f"PAT is valid. GitHub account: {response.json()['login']}")
                return True
            else:
                print(f"PAT is invalid. Error code: {response.status_code}, Message: {response.json().get('message', 'Unknown error')}")
                return False
        except Exception as e:
            print(f"Error checking PAT validity: {e}")
            return False

    def check_repo_access(self):
        """Check repository access"""
        try:
            headers = {
                "Authorization": f"token {self.pat}",
                "Accept": "application/vnd.github.v3+json"
            }
            repo_name = self.repo_url.split('/')[-1].replace('.git', '')
            response = requests.get(f"https://api.github.com/repos/{self.username}/{repo_name}", headers=headers)
            
            if response.status_code == 200:
                print(f"Repository {self.username}/{repo_name} exists and you have access.")
                return True
            else:
                print(f"Cannot access repository {self.username}/{repo_name}. Error code: {response.status_code}, Message: {response.json().get('message', 'Unknown error')}")
                return False
        except Exception as e:
            print(f"Error checking repository access: {e}")
            return False

    def check_network_connection(self):
        """Check network connection to GitHub"""
        try:
            response = requests.get("https://github.com", timeout=5)
            if response.status_code == 200:
                print("Network connection to GitHub successful.")
                return True
            else:
                print(f"Network connection to GitHub failed. Error code: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"Network connection to GitHub failed. Error: {e}")
            return False

    def push_to_github(self, files_to_push):
        """Push files to GitHub"""
        # Check prerequisites
        if not self.check_pat_validity():
            print("Error: Invalid PAT. Please check your PAT.")
            return False
            
        if not self.check_repo_access():
            print("Error: Cannot access repository. Please check access rights.")
            return False
            
        if not self.check_network_connection():
            print("Error: Cannot connect to GitHub. Please check network connection.")
            return False
        
        try:
            # Configure Git
            subprocess.run(["git", "config", "--global", "user.name", self.username])
            subprocess.run(["git", "config", "--global", "user.email", self.email])
            
            # Initialize Git repository if not already initialized
            if not os.path.exists(".git"):
                subprocess.run(["git", "init"])
                
            # Create main branch
            subprocess.run(["git", "branch", "-M", "main"])
            
            # Add remote origin
            try:
                subprocess.run(["git", "remote", "add", "origin", self.repo_url])
            except:
                # Remote might already exist
                subprocess.run(["git", "remote", "set-url", "origin", self.repo_url])
            
            # Ensure all files exist before adding
            existing_files = []
            for file_path in files_to_push:
                if os.path.exists(file_path):
                    existing_files.append(file_path)
                else:
                    print(f"Warning: File {file_path} does not exist and will be skipped.")
            
            if not existing_files:
                print("Error: No files to push.")
                return False
                
            # Add files to commit
            subprocess.run(["git", "add"] + existing_files)
            
            # Commit changes
            subprocess.run(["git", "commit", "-m", "WealthSync: Update code and data"])
            
            # Push to GitHub with force option to overwrite remote history
            result = subprocess.run(["git", "push", "-u", "origin", "main", "--force"], capture_output=True, text=True)
            
            print("Git push result:")
            print(result.stdout)
            print(result.stderr)
            
            if result.returncode == 0:
                print("Successfully pushed data to GitHub.")
                return True
            else:
                print("Failed to push data to GitHub. Please check errors above.")
                return False
                
        except Exception as e:
            print(f"Error pushing to GitHub: {e}")
            return False 