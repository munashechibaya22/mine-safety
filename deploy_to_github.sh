#!/bin/bash

echo "========================================"
echo "Mine Safety System - GitHub Deployment"
echo "========================================"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "ERROR: Git is not installed!"
    echo "Please install Git first:"
    echo "  Ubuntu/Debian: sudo apt-get install git"
    echo "  macOS: brew install git"
    exit 1
fi

echo "Step 1: Creating .gitignore file..."
echo ""

# Create .gitignore if it doesn't exist
if [ ! -f .gitignore ]; then
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Database
*.db
*.sqlite
*.sqlite3

# Environment
.env

# IDE
.vscode/
.idea/
*.swp
*.swo

# Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
dist/
build/

# Uploads
mine-safety-backend/uploads/*
!mine-safety-backend/uploads/.gitkeep

# Model cache
.mypy_cache/

# OS
.DS_Store
Thumbs.db
EOF
    echo "✓ .gitignore created"
else
    echo "✓ .gitignore already exists"
fi

echo ""
echo "Step 2: Initializing Git repository..."
echo ""

# Initialize git if not already initialized
if [ ! -d .git ]; then
    git init
    echo "✓ Git repository initialized"
else
    echo "✓ Git repository already initialized"
fi

echo ""
echo "Step 3: Adding all files..."
echo ""
git add .
echo "✓ Files added"

echo ""
echo "Step 4: Creating commit..."
echo ""
git commit -m "Initial commit: Mine Safety Detection System with PostgreSQL support" || echo "Note: No changes to commit or already committed"

echo ""
echo "Step 5: Setting up remote repository..."
echo ""

# Check if remote already exists
if ! git remote get-url origin &> /dev/null; then
    git remote add origin https://github.com/munashechibaya22/mine-safety.git
    echo "✓ Remote repository added"
else
    echo "✓ Remote repository already configured"
fi

echo ""
echo "Step 6: Renaming branch to main..."
echo ""
git branch -M main
echo "✓ Branch renamed to main"

echo ""
echo "========================================"
echo "IMPORTANT: Before pushing to GitHub"
echo "========================================"
echo ""
echo "1. Go to GitHub: https://github.com/munashechibaya22"
echo "2. Click 'New repository' (green button)"
echo "3. Repository name: mine-safety"
echo "4. Description: Mine Safety Detection System with AI"
echo "5. Keep it PUBLIC (for free deployment)"
echo "6. DO NOT initialize with README, .gitignore, or license"
echo "7. Click 'Create repository'"
echo ""
read -p "After creating the repository on GitHub, press Enter to continue..."

echo ""
echo "Step 7: Pushing to GitHub..."
echo ""
git push -u origin main

if [ $? -ne 0 ]; then
    echo ""
    echo "========================================"
    echo "ERROR: Push failed!"
    echo "========================================"
    echo ""
    echo "Possible reasons:"
    echo "1. Repository doesn't exist on GitHub yet"
    echo "2. Authentication failed"
    echo "3. Network issues"
    echo ""
    echo "To fix authentication:"
    echo "- Use GitHub Desktop, OR"
    echo "- Set up SSH keys, OR"
    echo "- Use Personal Access Token"
    echo ""
    echo "See: https://docs.github.com/en/authentication"
    echo ""
    exit 1
fi

echo ""
echo "========================================"
echo "SUCCESS! 🎉"
echo "========================================"
echo ""
echo "Your code is now on GitHub!"
echo "Repository: https://github.com/munashechibaya22/mine-safety"
echo ""
echo "Next steps:"
echo "1. Go to https://render.com"
echo "2. Sign up with your GitHub account"
echo "3. Click 'New +' then 'Blueprint'"
echo "4. Select your mine-safety repository"
echo "5. Click 'Apply'"
echo "6. Wait 5-10 minutes for deployment"
echo ""
echo "Your app will be live at:"
echo "- Frontend: https://mine-safety-frontend.onrender.com"
echo "- Backend: https://mine-safety-backend.onrender.com"
echo ""
echo "See RENDER_DEPLOYMENT.md for detailed instructions"
echo ""
