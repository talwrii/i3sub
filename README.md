<!-- This is generated by make-readme.py do not edit -->
# i3sub

A command-line program to output a stream of asynchronous events from the [i3](https://github.com/i3/i3) window manager using the [event api](https://i3wm.org/docs/ipc.html) via the [i3ipc](https://github.com/acrisci/i3ipc-python) library.

`i3sub` also provides a library, `i3sub.spawn`, to write tools that spawn programs in response to events among other actions.

You could use this tool to do things like: spawn programs when you visit a workspace, update a display when you move between windows, save a list of keybindings (which you care rerun), automatically save and restore the layout on a desktop (together with i3-clever-layout).

Requires [Python 3](https://www.python.org/download/releases/3.0/) but can co-exist with Python 2.

# See also (and self-promotion)

People interested in this tool might also be interested in:

* [i3parse](https://github.com/talwrii/i3parse) (by author) -- A tool to parse your i3 configuration and programmatically query it. List keybindings, find free keys, search commands.
* [i3-clever-layout](https://github.com/talwrii/i3-clever-layout) (by author) -- An extension of i3's layout saving and restoring feature that removes the need for per layout configuration (at the price of ahead-of-time general configuration)
* [i3-rofi-mark](https://github.com/talwrii/i3-rofi-mark) (by author) -- A tool to manual add marks to i3 windows

The author also maintains a list of potentially interesting tools they have written [here](https://github.com/talwrii/tools).

# Installing

```
pip3 install git+https://github.com/talwrii/i3sub#egg=i3sub
```

# Command-line application examples

```
# Show all i3 events
i3sub

# Show the type of i3 events (useful for filtering down to interesting events)
i3sub --quiet

# Show every keybinding that gets pressed. This illustrates the value of the "domain-specific language" that this tool provides
PYTHONUNBUFFERED=yes i3sub --run  | jq ' (.binding.mods | join(" + ")) + " + " + .binding.symbol ' -rc

# Record every command run (this could be useful for replaying commands)
PYTHONUNBUFFERED=yes i3sub --run | jq '.binding.command' -rc
```

# Library

A companion library, `i3sub.spawn`, is provided to read the output generated by the command-line program and perform actions.
This can, for example, spawn applications and move between workspaces.

Module spawn
------------

Functions
---------
current_workspace(conn=None)
    Return the name of the current workspace.

goto_workspace(name, conn=None)
    Go to a workspace called name.

pin_workspace(conn=None)
    Ensure that a workspace does get deleted (Use a layout with a universal swallowing window).

read_events_stdin()
    Return an iterator that yields dictionaries representing an i3 bus event.

run(event, *args)
    Run a command in the context of an event.

spawn_on(name, command, conn=None)
    Run a command on a workspace.

wait_for_workspace(name, conn=None)
    Wait until a given workspace is selected.

with_conn(*args, **kwds)
    Connect and clean up the connection.

with_workspace(*args, **kwds)
    Execute the context on a workspace.



# Cook book

Similar functionality can be created using `i3ipc` directly. It is hoped that utilities made with `i3sub` are easier to debug (as well as test) than the equivalent tools with `i3ipc`.

I would be very interesting in including scripts written by others.

* [Spawn in empty workspaces](examples/workspace_spawn.py) spawn commands the first time a workspace is visited.

# Implementing this tool using `i3-msg`

The utility `i3-msg` included with `i3` can perform similar functionality to this tool, with the caveat that `i3-msg` is more low-level and general-purpose (and hence difficult-to-understand and error-prone).

The following command will output every event to do with workspaces.

    i3-msg -t subscribe -m '[ "workspace" ]'

This command *should* output all events (events are documented [here](https://i3wm.org/docs/ipc.html#events)
)

    i3-msg -t subscribe -m '["workspace", "output", "mode", "window", "barconfig_update", "binding", "shutdown", "tick"]'

The advantages of `i3sub` over `i3-msg` are command line options,  preventing one from making (undetected) errors when typing.

# Usage

```
usage: i3sub [-h] [--quiet | --short] [--no-run | --run]
             [--no-focus | --focus] [--no-workspace | --workspace]

Subscribe to i3 events

optional arguments:
  -h, --help      show this help message and exit
  --quiet         Only show event types
  --short         Only show event types
  --no-run        Exclude actions events
  --run           Show only actions events
  --no-focus      Exclude focus events
  --focus         Show only focus events
  --no-workspace  Exclude action events
  --workspace     Show only action events

```

# Alternatives and prior work

## Code
* [i3ipc](https://github.com/acrisci/i3ipc-python) is the underlying library used by i3sub. The link provides an example application. It is hoped that this tool i) easier to debug; ii) more discoverable, since it is a command line tool; iii) language agnostic.
* [This question](https://faq.i3wm.org/question/5721/how-do-i-subscribe-to-i3-events-using-bash-easily.1.html) provides perl script for a similar purpose.
* [i3event](https://github.com/samuelotter/i3event.git) is a program that allows one to run commands in response to events from the i3. I found it difficult to work out which i3 events I should respond to, so I wrote this tool.
* [This reddit post](https://www.reddit.com/r/i3wm/comments/8iu51c/how_to_run_a_command_when_a_new_workspace_is/) talks about using `i3ipc` to run commands when a new workspace is created.
* [i3-msg](https://build.i3wm.org/docs/i3-msg.html) can be used in a very similar (if slightly less well documented) way to this tool (see


## Discussion
* [This reddit post](https://www.reddit.com/r/i3wm/comments/8iu51c/how_to_run_a_command_when_a_new_workspace_is/) discusses using `i3ipc` to run commands when a new workspace is created.
* [This reddit post](https://www.reddit.com/r/i3wm/comments/4b45p7/auto_start_applications_on_entering_empty/d16sj5w/) is on the same topic.
* [The i3 documentation](https://i3wm.org/docs/ipc.html#_subscribing_to_events) discusses subscribing to events.
* `i3-ipc` was the previous name of the `i3-msg` utility.

## Search terms
While researching similar tools, I used the following searches:

* ["i3 event" on GitHub](https://github.com/search?q=i3+event)
* ["i3 subscribe" on GitHub](https://github.com/search?utf8=%E2%9C%93&q=i3+subscribe&type=)
* ["i3 message" on GitHub](https://github.com/search?q=i3+message)
* ["i3wm event" on GitHub](https://github.com/search?q=i3+event)
* ["i3wm subscribe" on GitHub](https://github.com/search?utf8=%E2%9C%93&q=i3+subscribe&type=)
* ["i3wm message" on GitHub](https://github.com/search?q=i3+message)
* ["action on event" on the i3wm reddit](https://www.reddit.com/r/i3wm/search?q=action%20on%20event&restrict_sr=1)
* ["subscribe to event" on the i3wm reddit](https://www.reddit.com/r/i3wm/search?q=subscribe%20to%20event&restrict_sr=1)
* ["run new workspace" on the i3wm reddit](https://www.reddit.com/r/i3wm/search?q=run%20new%20workspace&restrict_sr=1)
* ["i3 subscribe" on Google](https://www.google.com/search?q=i3+subscribe)
* ["i3 event" on Google](https://www.google.com/search?q=i3+event)

# Testing

This tool is untested. Because this tool interacts with `i3` testing is rather intricate - though not impossible. It would not be particularly difficult to record and replay streams of event from `i3` or automate i3 with `i3-msg`.

## Installation

Some very basic testing is provided with tox.  This tests that the code loads.
