import os.path
import sys
import requests
import json

from tkinter import *

checks = []
window = None

endpoint_work_types = 'http://localhost:8001/api/v0/work_types/'


def mynoosha():
    args = sys.argv
    if len(args) >= 2:
        if 'pythonpath' in args:
            python_path()
        elif 'seed' in args:
            seed()
        else:
            print_usage(None)
    else:
        print_usage(None)


def seed():
    # work_types
    for name in ["milestone", "piece", "time"]:
        confirmed = confirm_work_type(name)
        if confirmed:
            print(f"confirmed work type:{confirmed}")
        else:
            print(f"NOT confirmed work type:{name}")

def confirm_work_type(name):
    found = get_work_type(name)
    if not found:
        return create_work_type(name)
    return found

def create_work_type(name):
    response = requests.post(endpoint_work_types, data={"name": name})
    return json.loads(response.content.decode('utf8'))


def get_work_type(name):
    response = requests.get(endpoint_work_types, params={"name": name})
    founds = json.loads(response.content.decode('utf8'))
    if len(founds) > 0:
        return founds[0]
    return None


def python_path():
    command = 'pythonpath'
    args = sys.argv
    command_index = args.index(command)
    shell_config_files = []
    possibles = [
        '~/.profile',
        '~/.zshrc',
        '~/.bash_profile',
        '~/.bashrc',
        'some_other_file'
    ]
    founds = [possible for possible in [possible if file_exists(possible) else None for possible in possibles] if
              possible is not None]
    alreadys = [found for found in [found if found_has_pythonpath_entry(found) else None for found in founds] if
                found is not None]
    editables = [found for found in founds if found not in alreadys]

    questions = [
        {
            'type': 'checkbox',
            'name': 'config files',
            'message': 'select files to updated / confirmed for PYTHONPATH entry',
            'choices': editables
        }
    ]
    global window
    window = Tk()
    window.title("PYTHONPATH injector")
    window.geometry('245x180')
    window.resizable(width=False, height=False)
    window.tk.call('tk', 'scaling', 3.0)
    instruction = Label(window, text="choose shell config files to update:", justify=LEFT)
    instruction.place(x=10, y=10)
    HEADER_HEIGHT = 20
    LINE_HEIGHT = 20
    for ei, editable in enumerate(editables, start=1):
        var = BooleanVar()
        check = Checkbutton(window, text=editable, variable=var)
        check.place(x=10, y=HEADER_HEIGHT + (ei * LINE_HEIGHT))
        checks.append({
            'editable': editable,
            'check': check,
            'var': var
        })

    ok = Button(window, text="ok", command=update_config_files)
    ok.place(x=10, y=HEADER_HEIGHT + (len(editables) + 2) * LINE_HEIGHT)

    window.mainloop()


def update_config_files():
    print(f"to append to config files: \r\n{python_path_to_append}")
    for check in checks:
        append_path = check['var'].get()
        appendable = check['editable']
        count_appended = 0
        if append_path:
            print(f"appending to shell config file: {appendable}")

            count_appended += 1
            append_target = open(os.path.expanduser(appendable), 'a')
            append_target.write(f"\n{python_path_to_append}\n")
            append_target.close()
    window.destroy()


def found_has_pythonpath_entry(name):
    cwd = os.getcwd()
    pythonpath_expected = f'export PYTHONPATH="$PYTHONPATH:{cwd}"'
    global python_path_to_append
    python_path_to_append = pythonpath_expected
    if '~' in name:
        opened = open(os.path.expanduser(name))
    else:
        opened = open(name)
    with opened as candidate:
        if pythonpath_expected in candidate.read():
            return True
        else:
            return False


def file_exists(name):
    if '~' in name:
        return os.path.exists(os.path.expanduser('~/.profile'))
    else:
        return os.path.isfile(name)


def logo(command, details):
    # this ascii font face:
    #   https://patorjk.com/software/taag/#p=display&f=Tmplr&t=mynoosha
    #   use 'tmpmlr'
    print(f"""             
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                ┓   
    ┏┳┓┓┏┏┓┏┓┏┓┏┣┓┏┓
    ┛┗┗┗┫┛┗┗┛┗┛┛┛┗┗┻   {command if command is not None else '(no command provided)'} 
        ┛           
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    \n\n""")
    if details is not None:
        if isinstance(details, str):
            print(details)
        else:
            for detail in details:
                print(detail)
    if command is None:
        pass
        # print(f"    try $ mynoosha help for available commands ")


def print_usage(command):
    logo(command, None)
    if command is None:
        print("""
        $ mynoosha <command>

        where <command> is some combination of the following options:

        """)
    print_usage_command(command, None)


def print_usage_no_logo(command):
    if command is None:
        print("""
        $ mynoosha <command>

        where <command> is some combination of the following options:

        """)
    print_usage_command(command, None)


def print_usage_command(command, details):
    command_printers = {
        'pythonpath': print_usage_python_path
    }
    if command is None:
        for command in command_printers:
            command_printers[command](None)
    else:
        callable = command_printers[command]
        if callable is not None:
            callable(details)
        else:
            print(f"no help renderer for command: {command}")


def print_usage_python_path(details):
    if details is not None:
        print(details)
    print(f"""
    pythonpath <shellconfigfile>:       adds current directory to PYTHONPATH environment variable to <shellconfigfile>
                                        eg. ~/.profile  
    """)


if __name__ == "__main__":
    mynoosha()
