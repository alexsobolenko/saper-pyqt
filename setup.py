from cx_Freeze import setup, Executable
 
exe = Executable(
    script="saper.py",
    base="Win32GUI",
    )
   
setup(
    name = "wxSampleApp",
    version = "0.1",
    description = "saper",
    executables = [exe]
    )