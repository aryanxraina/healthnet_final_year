#!/usr/bin/env python3
"""
HealthNet Backend Dependencies Installer
This script installs the required dependencies for the backend.
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install required dependencies"""
    print("Installing HealthNet Backend Dependencies...")
    print("="*50)
    
    # Check if we're in the right directory
    if not os.path.exists("healthnet-project/backend/requirements.txt"):
        print("requirements.txt not found!")
        print("Please run this script from the project root directory")
        return False
    
    try:
        # Install dependencies
        print("Installing Python packages...")
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "healthnet-project/backend/requirements.txt"
        ], check=True)
        
        print("All dependencies installed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Failed to install dependencies: {e}")
        return False
    except Exception as e:
        print(f"Error installing dependencies: {e}")
        return False

def main():
    """Main function"""
    print("HealthNet Backend Dependencies Installer")
    print("="*50)
    
    if install_dependencies():
        print("\nInstallation completed!")
        print("You can now start the backend with: python start_backend.py")
    else:
        print("\nInstallation failed!")
        print("Please check the error messages above and try again.")

if __name__ == "__main__":
    main()
