@echo off
setlocal

REM Set the branch name
set "branch_name=dailycommit"

REM Your commit message with timestamp
set "commit_message=Automated commit - %date% %time%"

REM Add all changes to the staging area
git add .

REM Commit changes with the generated message
git commit -m "%commit_message%"

REM Push changes to the remote repository
git push origin %branch_name%

echo Changes committed and pushed successfully.
pause

