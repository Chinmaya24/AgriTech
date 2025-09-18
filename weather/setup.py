#!/usr/bin/env python3
"""
Setup script for Crop Disease Forecaster
This script helps you set up the environment and get started quickly.
"""

import os
import subprocess
import sys

def create_env_file():
    """Create .env file with default values"""
    env_content = """# Flask Configuration
SECRET_KEY=your-secret-key-change-this-in-production

# OpenWeatherMap API Configuration
# Get your API key from: https://openweathermap.org/api
OPENWEATHER_API_KEY=your-openweathermap-api-key-here
"""
    
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Created .env file with default values")
    else:
        print("ℹ️  .env file already exists")

def install_requirements():
    """Install required packages"""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Installed all required packages")
    except subprocess.CalledProcessError:
        print("❌ Failed to install packages. Please run: pip install -r requirements.txt")

def main():
    print("🌱 Setting up Crop Disease Forecaster...")
    print("=" * 50)
    
    # Create .env file
    create_env_file()
    
    # Install requirements
    install_requirements()
    
    print("\n" + "=" * 50)
    print("🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Get your OpenWeatherMap API key from: https://openweathermap.org/api")
    print("2. Edit .env file and add your API key")
    print("3. Run: python app.py")
    print("4. Open: http://localhost:5000")
    print("\nHappy farming! 🌾")

if __name__ == "__main__":
    main()
