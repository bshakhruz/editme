#!/usr/bin/env python3
"""
Setup script for DV Lottery Photo Corrector Bot
"""

import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version}")
    return True

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Packages installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}")
        return False

def setup_env_file():
    """Set up environment file"""
    if os.path.exists('.env'):
        print("✅ .env file already exists")
        return True
    
    if os.path.exists('config.env'):
        try:
            import shutil
            shutil.copy('config.env', '.env')
            print("✅ Created .env file from config.env")
            print("⚠️  Please edit .env file with your actual API keys")
            return True
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    else:
        print("❌ config.env file not found")
        return False

def check_sample_image():
    """Check if sample image exists"""
    if os.path.exists('image.png'):
        print("✅ Sample image (image.png) found")
        return True
    else:
        print("⚠️  Sample image (image.png) not found")
        print("   Please add your reference image as 'image.png' in the project root")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up DV Lottery Photo Corrector Bot...")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install requirements
    if not install_requirements():
        return False
    
    # Setup environment file
    if not setup_env_file():
        return False
    
    # Check sample image
    check_sample_image()
    
    print("=" * 50)
    print("🎉 Setup completed!")
    print("\n📋 Next steps:")
    print("1. Edit .env file with your API keys")
    print("2. Add sample image as 'image.png'")
    print("3. Run: python telegram_bot.py")
    print("\n📖 See README.md for detailed instructions")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
