from path_root.path_a.path_aa.callee import callee_ping
from sys import path


# expect a pretty juiced up PYTHONPATH when we run this in an IDE,
# cuz that's what an idea does: fills in all the blanks so you don't have to go
# writing a ton of config

# the following paths are what we get when caller.py is run from this path:
#       /Users/jazzhammer/Documents/workspace_2013/mynoosha/path_root/path_b/path_ba

# /Users/jazzhammer/Documents/workspace_2013/mynoosha/path_root/path_b/path_ba
# /Users/jazzhammer/Documents/workspace_2013/mynoosha
# /Applications/PyCharm.app/Contents/plugins/python/helpers/pycharm_display
# /usr/local/Cellar/python@3.9/3.9.19_1/Frameworks/Python.framework/Versions/3.9/lib/python39.zip
# /usr/local/Cellar/python@3.9/3.9.19_1/Frameworks/Python.framework/Versions/3.9/lib/python3.9
# /usr/local/Cellar/python@3.9/3.9.19_1/Frameworks/Python.framework/Versions/3.9/lib/python3.9/lib-dynload
# /Users/jazzhammer/Library/Python/3.9/lib/python/site-packages
# /usr/local/lib/python3.9/site-packages
# /Applications/PyCharm.app/Contents/plugins/python/helpers/pycharm_matplotlib_backend

# it makes sense that the run of caller.py "just-works" in the idea, with the file in focus and,
# in my case: using pyCharm who appends a bunch of paths that 'make sense' to add to PYTHONPATH,
# that this path:
#       /Users/jazzhammer/Documents/workspace_2013/mynoosha
# is in the list.

# when we call from the command line, similarly in this folder:
#       /Users/jazzhammer/Documents/workspace_2013/mynoosha/path_root/path_b/path_ba
# we get something like this output:
"""
(.venv) 8:18:20 ~/Documents/workspace_2013/mynoosha/path_root/path_b/path_ba main $ python caller.py
Traceback (most recent call last):
  File "/Users/jazzhammer/Documents/workspace_2013/mynoosha/path_root/path_b/path_ba/caller.py", line 1, in <module>
    from path_root.path_a.path_aa.callee import callee_ping
ModuleNotFoundError: No module named 'path_root'
"""
# which is not too surprising when we look at the PYTHONPATH we have in the shell, without doing anything in particular
# to it:
"""
(.venv) 9:44:33 ~/Documents/workspace_2013/mynoosha/path_root/path_b/path_ba main $ echo "$PYTHONPATH"
/Users/jazzhammer/gnuhealth/tryton/server/trytond-6.0.44:/Users/jazzhammer/gnuhealth/tryton/server/config
"""
# so let's do something to it and see if can get some more effective behaviour:
# this is a demo-styled walk through of a possible solution to a common problem,
# it isn't a tutorial on writing *nix command lines so, if you're not familiar with shell env variables,
# take a minute to consult the webernet and come back.
# we'll try this:
"""
export PYTHONPATH="$PYTHONPATH:/Users/jazzhammer/Documents/workspace_2013/mynoosha"
(.venv) 9:55:58 ~/Documents/workspace_2013/mynoosha/path_root/path_b/path_ba main $ echo "$PYTHONPATH"
/Users/jazzhammer/gnuhealth/tryton/server/trytond-6.0.44:/Users/jazzhammer/gnuhealth/tryton/server/config:/Users/jazzhammer/Documents/workspace_2013/mynoosha
"""
# that's just might work. when we try again:
"""
(.venv) 9:56:34 ~/Documents/workspace_2013/mynoosha/path_root/path_b/path_ba main $ python caller.py
calling callee! with this PYTHONPATH from sys.path ...
/Users/jazzhammer/Documents/workspace_2013/mynoosha/path_root/path_b/path_ba
/Users/jazzhammer/gnuhealth/tryton/server/trytond-6.0.44
/Users/jazzhammer/gnuhealth/tryton/server/config
/Users/jazzhammer/Documents/workspace_2013/mynoosha
/Users/jazzhammer/.pyenv/versions/3.9.18/lib/python39.zip
/Users/jazzhammer/.pyenv/versions/3.9.18/lib/python3.9
/Users/jazzhammer/.pyenv/versions/3.9.18/lib/python3.9/lib-dynload
/Users/jazzhammer/.pyenv/versions/3.9.18/lib/python3.9/site-packages
i have been called !!
"""
# that's a pretty good result.  this can be automated of course with more exercises in shell-scripting,
# so any .py file you want to run will be provided with the env to find all the modules of yours that it needs
def call_callee():
    print(f"calling callee! with this PYTHONPATH from sys.path ...")
    for pathlet in path:
        print(f"{pathlet}")
    callee_ping()

if __name__=="__main__":
    call_callee()