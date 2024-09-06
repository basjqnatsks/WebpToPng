@echo off

:: Get the current directory of the batch script
set "script_dir=%~dp0"

:: Set the Python script path relative to the batch script location
set "python_script=%script_dir%WebpToPng.py"

:: Print the current directory and the Python script path for debugging
echo Batch script directory: %script_dir%
echo Python script path: %python_script%

:: Verify the Python script exists
if not exist "%python_script%" (
    echo Error: Python script "%python_script%" not found in the expected directory.
    pause
    exit /b 1
)

:: Define the task name and description
set "task_name=WebpToPngPY"

:: Check if the task already exists
schtasks /query /tn "%task_name%" >nul 2>&1
if "%errorlevel%"=="0" (
    echo Task "%task_name%" already exists. Deleting the old task...
    schtasks /delete /tn "%task_name%" /f >nul 2>&1
    if "%errorlevel%"=="0" (
        echo Old task deleted successfully.
    ) else (
        echo Failed to delete the old task. Exiting...
        pause
        exit /b 1
    )
)

:: Prepare the schtasks command for debugging
set "schtask_command=schtasks /create /tn "%task_name%" /tr "pyw \"%python_script%\"" /sc onlogon /rl highest /f"

:: Print the schtasks command for debugging
echo Debug: Executing the following schtasks command:
echo %schtask_command%

:: Execute the schtasks command
%schtask_command% >nul 2>&1

:: Check if the task creation was successful
if "%errorlevel%"=="0" (
    echo The scheduled task "%task_name%" has been created successfully.
    echo The Python script "%python_script%" will run at startup.
) else (
    echo Failed to create the scheduled task.
    pause
    exit /b 1
)

pause
exit /b 0
