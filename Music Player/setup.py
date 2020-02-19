import sys
from cx_Freeze import setup,Executable

#dependencies are automatically detected,but it might need fine tuning.
build_exe_options={"packages":["os"]}

#GUI applications require a different base on windows(the default is for a console application).
base=None
if sys.platform=="win32":
  base="Win32GUI"
  
setup(name="Melody",
      version="0.1",
	  description="Music Player",
	  options={"build_exe":build_exe_options},
	  executables=[Executable("melody.py",base=base)])