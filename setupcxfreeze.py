from cx_Freeze import setup, Executable
import sys

if sys.platform == 'win32':
	setup(
        name = "crvideo.exe",
        version = "1.0.0",
        description = "DDM Cache Reader",
        executables = [Executable("crvideo.pyw")])
else:
	includes = ['time', 'atexit']
	excludes = []
	path = []
	packages = []


	RemoteTarget = Executable (
		script = "crvideo.pyw",
		initScript = None,
		targetName = "crvideo",
		compress = True,
		copyDependentFiles = True,
		appendScriptToExe = False,
		appendScriptToLibrary = False,
		icon = None
		)

	setup(
	        name = "crvideo",
	        version = "1.0.0",
	        description = "DDM Cache Reader",
	
		options = {"build_exe": {"includes": includes,
					 "excludes": excludes,
					 "path": path,
					 "packages": packages}
		  },

	        executables = [RemoteTarget]
		)

