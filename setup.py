import cx_Freeze

executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(
    name="Chicken Little",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":["data"]}},
    executables = executables

    )