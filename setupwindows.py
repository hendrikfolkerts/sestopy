#setup-File for cx_Freeze
from cx_Freeze import setup, Executable
import main
 
includefiles = ["config.txt", "Documentation/Doc_LaTeX/doc.pdf", "helptext.txt", "i2rightarrow.ico", "i2rightarrow.png", "iaddsiblingnode.png",
                "iaddsubnode.png", "ianode.png", "iback.png", "ibook.png", "icollapseall.png", "ideletenode.png",
                "idnode.png", "ieditadd.png", "ieditdelete.png", "ienode.png", "iexpandall.png", "ifileopen.png",
                "ifilesave.png", "ifilesaveas.png", "iflatten.png", "iforward.png", "ihelp.png", "imanode.png",
                "inode.png", "inok.png", "iok.png", "iprune.png", "iremove.png", "isnode.png"] # include files
includes = []
excludes = []
packages = []
version = main.__version__.replace(".", "_")

exe = Executable(
 # what to build
   script = "main.py", # the name of the main python script
   initScript = None,
   base = 'Win32GUI', # "Win32GUI" because no console app
   targetName = "SESToPy_" + version + ".exe", #name of exe
   copyDependentFiles = True,
   compress = True,
   appendScriptToExe = True,
   appendScriptToLibrary = True,
   icon = "i2rightarrow.ico" # the icon
)
 
setup(
    name = "SESToPy", # name of program
    version = main.__version__,
    description = 'SESToPy',
    author = "Hendrik Martin Folkerts",
    author_email = "hendrikmartinfolkerts@gmail.com",
    options = {"build_exe": {"excludes":excludes,"packages":packages,
      "include_files":includefiles}},
    executables = [exe]
)
