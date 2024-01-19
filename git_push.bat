@echo off
setlocal

REM Your commit message with timestamp
set "commit_message=Automated commit - %date% %time%"

REM Add all changes to the staging area
git add .

REM Commit changes with the generated message
git commit -m "%commit_message%"

REM Push changes to the remote repository
git push origin main  REM Replace 'main' with your branch name if applicable

echo Changes committed and pushed successfully.
pause
