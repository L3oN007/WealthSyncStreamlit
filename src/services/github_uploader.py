import os
import subprocess
import tempfile
import shutil
from git import Repo
from src.utils.logger import setup_logger

logger = setup_logger("github_uploader")

class GitHubUploader:
    """Class to upload data to GitHub repository"""
    def __init__(self, username, email, repo_url, access_token):
        self.username = username
        self.email = email
        self.repo_url = repo_url
        self.access_token = access_token
        self.temp_dir = None
        
    def push_to_github(self, files_to_push):
        """Push files to GitHub repository"""
        if not files_to_push:
            logger.warning("No files to push")
            return False
            
        if not all([self.username, self.email, self.repo_url, self.access_token]):
            logger.error("GitHub credentials not configured")
            return False
            
        try:
            # Create a temporary directory for the repository
            self.temp_dir = tempfile.mkdtemp()
            logger.info(f"Created temporary directory: {self.temp_dir}")
            
            # Clone the repository
            repo_url_with_token = self.repo_url.replace('https://', f'https://{self.username}:{self.access_token}@')
            repo = Repo.clone_from(repo_url_with_token, self.temp_dir)
            logger.info(f"Cloned repository: {self.repo_url}")
            
            # Configure Git
            repo.config_writer().set_value("user", "name", self.username).release()
            repo.config_writer().set_value("user", "email", self.email).release()
            
            # Copy files to the repository
            files_copied = []
            for file_path in files_to_push:
                if os.path.exists(file_path):
                    # Determine the relative path in the repository
                    file_name = os.path.basename(file_path)
                    target_path = os.path.join(self.temp_dir, "data", file_name)
                    
                    # Ensure the target directory exists
                    os.makedirs(os.path.dirname(target_path), exist_ok=True)
                    
                    # Copy the file
                    shutil.copy2(file_path, target_path)
                    files_copied.append(file_name)
                    logger.info(f"Copied file: {file_name}")
            
            if not files_copied:
                logger.warning("No files were copied")
                return False
                
            # Commit and push changes
            repo.git.add(all=True)
            commit_message = f"Update data files: {', '.join(files_copied)}"
            repo.index.commit(commit_message)
            origin = repo.remote(name='origin')
            origin.push()
            
            logger.info(f"Successfully pushed {len(files_copied)} files to GitHub")
            return True
            
        except Exception as e:
            logger.error(f"Error pushing to GitHub: {e}")
            return False
            
        finally:
            # Clean up temporary directory
            if self.temp_dir and os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
                logger.info("Cleaned up temporary directory") 