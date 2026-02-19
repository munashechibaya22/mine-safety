@echo off
echo ========================================
echo Mine Safety System - GitHub Deployment
echo ========================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed!
    echo Please install Git from: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo Step 1: Creating .gitignore file...
echo.

REM Create .gitignore if it doesn't exist
if not exist .gitignore (
    (
        echo # Python
        echo __pycache__/
        echo *.py[cod]
        echo *$py.class
        echo *.so
        echo .Python
        echo venv/
        echo env/
        echo ENV/
        echo.
        echo # Database
        echo *.db
        echo *.sqlite
        echo *.sqlite3
        echo.
        echo # Environment
        echo .env
        echo.
        echo # IDE
        echo .vscode/
        echo .idea/
        echo *.swp
        echo *.swo
        echo.
        echo # Node
        echo node_modules/
        echo npm-debug.log*
        echo yarn-debug.log*
        echo yarn-error.log*
        echo dist/
        echo build/
        echo.
        echo # Uploads
        echo mine-safety-backend/uploads/*
        echo !mine-safety-backend/uploads/.gitkeep
        echo.
        echo # Model cache
        echo .mypy_cache/
        echo.
        echo # OS
        echo .DS_Store
        echo Thumbs.db
    ) > .gitignore
    echo ✓ .gitignore created
) else (
    echo ✓ .gitignore already exists
)

echo.
echo Step 2: Initializing Git repository...
echo.

REM Initialize git if not already initialized
if not exist .git (
    git init
    echo ✓ Git repository initialized
) else (
    echo ✓ Git repository already initialized
)

echo.
echo Step 3: Adding all files...
echo.
git add .
echo ✓ Files added

echo.
echo Step 4: Creating commit...
echo.
git commit -m "Initial commit: Mine Safety Detection System with PostgreSQL support"
if errorlevel 1 (
    echo Note: No changes to commit or already committed
)

echo.
echo Step 5: Setting up remote repository...
echo.

REM Check if remote already exists
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    git remote add origin https://github.com/munashechibaya22/mine-safety.git
    echo ✓ Remote repository added
) else (
    echo ✓ Remote repository already configured
)

echo.
echo Step 6: Renaming branch to main...
echo.
git branch -M main
echo ✓ Branch renamed to main

echo.
echo ========================================
echo IMPORTANT: Before pushing to GitHub
echo ========================================
echo.
echo 1. Go to GitHub: https://github.com/munashechibaya22
echo 2. Click "New repository" (green button)
echo 3. Repository name: mine-safety
echo 4. Description: Mine Safety Detection System with AI
echo 5. Keep it PUBLIC (for free deployment)
echo 6. DO NOT initialize with README, .gitignore, or license
echo 7. Click "Create repository"
echo.
echo After creating the repository on GitHub, press any key to push...
pause

echo.
echo Step 7: Pushing to GitHub...
echo.
git push -u origin main

if errorlevel 1 (
    echo.
    echo ========================================
    echo ERROR: Push failed!
    echo ========================================
    echo.
    echo Possible reasons:
    echo 1. Repository doesn't exist on GitHub yet
    echo 2. Authentication failed
    echo 3. Network issues
    echo.
    echo To fix authentication:
    echo - Use GitHub Desktop, OR
    echo - Set up SSH keys, OR
    echo - Use Personal Access Token
    echo.
    echo See: https://docs.github.com/en/authentication
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo SUCCESS! 🎉
echo ========================================
echo.
echo Your code is now on GitHub!
echo Repository: https://github.com/munashechibaya22/mine-safety
echo.
echo Next steps:
echo 1. Go to https://render.com
echo 2. Sign up with your GitHub account
echo 3. Click "New +" then "Blueprint"
echo 4. Select your mine-safety repository
echo 5. Click "Apply"
echo 6. Wait 5-10 minutes for deployment
echo.
echo Your app will be live at:
echo - Frontend: https://mine-safety-frontend.onrender.com
echo - Backend: https://mine-safety-backend.onrender.com
echo.
echo See RENDER_DEPLOYMENT.md for detailed instructions
echo.
pause
