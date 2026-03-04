#!/usr/bin/env python3
"""
MongoDB Setup Script for HealthNet
This script helps set up MongoDB database for the HealthNet project.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_mongodb_installed():
    """Check if MongoDB is installed"""
    try:
        # Try the standard mongod command first
        result = subprocess.run(['mongod', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ MongoDB is installed!")
            print(f"   Version: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    # Try the Windows installation path
    try:
        mongod_path = r"C:\Program Files\MongoDB\Server\8.0\bin\mongod.exe"
        if os.path.exists(mongod_path):
            result = subprocess.run([mongod_path, '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ MongoDB is installed!")
                print(f"   Version: {result.stdout.strip()}")
                return True
    except Exception:
        pass
    
    return False

def install_mongodb_windows():
    """Install MongoDB on Windows"""
    print("📥 Installing MongoDB on Windows...")
    print("Please download and install MongoDB from: https://www.mongodb.com/try/download/community")
    print("Or use Chocolatey: choco install mongodb")
    print("Or use winget: winget install MongoDB.Server")
    return False

def start_mongodb_service():
    """Start MongoDB service"""
    try:
        if sys.platform == "win32":
            # Windows
            result = subprocess.run(['net', 'start', 'MongoDB'], capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ MongoDB service started!")
                return True
            else:
                print("⚠️ MongoDB service might already be running or needs manual start")
                return True
        else:
            # Linux/macOS
            result = subprocess.run(['sudo', 'systemctl', 'start', 'mongod'], capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ MongoDB service started!")
                return True
            else:
                print("⚠️ MongoDB service might already be running or needs manual start")
                return True
    except Exception as e:
        print(f"⚠️ Could not start MongoDB service: {e}")
        print("💡 Please start MongoDB manually")
        return False

def setup_environment():
    """Set up environment variables"""
    env_file = Path(".env")
    
    env_content = """# HealthNet MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017

# Security
SECRET_KEY=your-super-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Server Configuration
HOST=0.0.0.0
PORT=8000
RELOAD=true
"""
    
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print("✅ Environment file (.env) created!")

def main():
    """Main setup function"""
    print("🏥 HealthNet MongoDB Setup")
    print("=" * 40)
    
    # Check if MongoDB is installed
    if not check_mongodb_installed():
        print("❌ MongoDB is not installed!")
        if sys.platform == "win32":
            install_mongodb_windows()
        else:
            print("Please install MongoDB first:")
            print("Ubuntu/Debian: sudo apt-get install mongodb")
            print("macOS: brew install mongodb/brew/mongodb-community")
            print("Windows: Download from https://www.mongodb.com/try/download/community")
        return
    
    # Start MongoDB service
    print("\n🚀 Starting MongoDB service...")
    start_mongodb_service()
    
    # Setup environment
    print("\n⚙️ Setting up environment...")
    setup_environment()
    
    print("\n🎉 Setup completed!")
    print("\n📋 Next steps:")
    print("1. Ensure MongoDB is running")
    print("2. Run: pip install -r requirements.txt (to install dependencies)")
    print("3. Run: python run_server.py (to start the server)")
    print("4. Visit: http://localhost:8000/docs (to test the API)")
    print("\n💡 MongoDB will automatically create the 'healthnet' database when you first use it!")

if __name__ == "__main__":
    main()
