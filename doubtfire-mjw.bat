@ECHO OFF

:: Activate env
@CALL "C:\ProgramData\Miniconda3\Scripts\activate.bat" base

:: Call script
python "%~dp0\doubtfire.py"
