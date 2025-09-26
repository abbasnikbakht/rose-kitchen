#!/usr/bin/env python3
"""
GitHub Preparation Script for گل سرخ Rose Kitchen
This script helps prepare your app for GitHub and Render deployment
"""

import os
import subprocess
import sys

def check_git_status():
    """Check if git is initialized and files are ready"""
    print("🔍 Checking Git status...")
    
    try:
        # Check if git is initialized
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Git not initialized. Initializing now...")
            subprocess.run(['git', 'init'], check=True)
            print("✅ Git initialized")
        else:
            print("✅ Git repository found")
        
        # Check for uncommitted changes
        result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
        if result.stdout.strip():
            print("📝 Found uncommitted changes:")
            print(result.stdout)
            return False
        else:
            print("✅ All changes committed")
            return True
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Git error: {e}")
        return False
    except FileNotFoundError:
        print("❌ Git not installed. Please install Git first.")
        return False

def check_required_files():
    """Check if all required files for deployment exist"""
    print("\n📋 Checking required files...")
    
    required_files = [
        'app.py',
        'requirements.txt',
        'Procfile',
        'runtime.txt',
        'templates/',
        'demo_data.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    else:
        print("✅ All required files present")
        return True

def create_gitignore():
    """Create .gitignore file if it doesn't exist"""
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# Environment Variables
.env
.env.local
.env.production

# Database
*.db
*.sqlite
*.sqlite3

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Temporary files
*.tmp
*.temp
"""
    
    if not os.path.exists('.gitignore'):
        with open('.gitignore', 'w') as f:
            f.write(gitignore_content)
        print("✅ Created .gitignore file")
    else:
        print("✅ .gitignore already exists")

def prepare_for_github():
    """Main function to prepare for GitHub"""
    print("🚀 Preparing گل سرخ Rose Kitchen for GitHub and Render deployment...")
    print("=" * 70)
    
    # Check required files
    if not check_required_files():
        print("\n❌ Please ensure all required files are present before proceeding.")
        return False
    
    # Create .gitignore
    create_gitignore()
    
    # Check git status
    if not check_git_status():
        print("\n📝 You have uncommitted changes. Please commit them first:")
        print("   git add .")
        print("   git commit -m 'Prepare for Render deployment'")
        return False
    
    print("\n✅ Your app is ready for GitHub!")
    print("\n📋 Next steps:")
    print("1. Create a new repository on GitHub")
    print("2. Add the remote origin:")
    print("   git remote add origin https://github.com/YOUR_USERNAME/rose-kitchen.git")
    print("3. Push to GitHub:")
    print("   git push -u origin main")
    print("4. Deploy on Render following the RENDER_DEPLOYMENT.md guide")
    
    print("\n🌹 Your Persian kitchen app is ready to go live! 🍳")
    return True

def main():
    """Main function"""
    try:
        if prepare_for_github():
            print("\n🎉 Success! Your app is ready for deployment.")
        else:
            print("\n❌ Please fix the issues above before proceeding.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Preparation cancelled.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
