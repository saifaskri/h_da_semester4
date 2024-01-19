@echo off
setlocal

set "commit_message=Automated commit - %date% %time%"

git add .

git commit -m "%commit_message%"

git push origin main  

echo Changes committed and pushed successfully.
pause
