@echo off
cd /d "d:\IIT KHARAGPUR\Sem6\IS Project"
echo Staging worl.ipynb...
"C:\Program Files\Git\bin\git.exe" add worl.ipynb
echo.
echo Committing changes...
"C:\Program Files\Git\bin\git.exe" commit -m "Final update: Sleep quality scoring with HRV, efficiency, deep sleep, and REM calculations"
echo.
echo Pulling latest from remote...
"C:\Program Files\Git\bin\git.exe" pull origin main --no-edit
echo.
echo Pushing to GitHub...
"C:\Program Files\Git\bin\git.exe" push origin main -v
echo.
echo Done!
pause
