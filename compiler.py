import os

validation = input("In order to compile TimeManager in .exe you have to install Nuitka lib. Continue? Y or enter to cancel ")
working_dir = os.getcwd()
if validation == "Y".lower():
    try:
        import nuitka
        print("Module Nuitka already installed")
    except ModuleNotFoundError:
        print("Installing module Nuitka")
        os.system("pip install nuitka")
        pass

    os.system('nuitka '
              '--file-version=0.0.5.1 '
              '--product-name=Time_manager '
              '--enable-console '
              '--mingw64 '
              '--standalone '
              '--windows-icon-from-ico=coding.ico '
              f'--output-dir="{working_dir}" '
              '--remove-output main.py')
elif not validation:
    print("compilation canceled")
