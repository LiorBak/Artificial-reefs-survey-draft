@echo off
echo =====================================================
echo  Artificial Reefs - Git Repository Setup
echo =====================================================
echo.
cd /d "%~dp0"

echo [1/3] Initializing local git repository...
git init

echo [2/3] Adding files to git...
git add .

echo [3/3] Creating initial commit...
git commit -m "Initial commit: Artificial surf reefs survey website"

echo.
echo =====================================================
echo  Done! Your local repository is ready.
echo.
echo  NEXT STEPS TO GO LIVE ON GITHUB PAGES:
echo  1. Create a new repository on https://github.com/new
echo     (e.g., named 'artificial-reefs', set to Public)
echo  2. Copy and run the following two commands in this terminal:
echo.
echo     git remote add origin https://github.com/YOUR_USERNAME/artificial-reefs.git
echo     git branch -M main
echo     git push -u origin main
echo.
echo  3. On GitHub: go to Settings -^> Pages -^> Deploy from a branch (main / root) -^> Save.
echo =====================================================
pause
