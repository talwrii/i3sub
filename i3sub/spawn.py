import subprocess
import contextlib
import time
import subprocess
import tempfile
import sys
import json
import i3ipc

# On the use of polling.

#  I am using polling here rather than creating a connection.
#  This goes someway to illustrate *why* one would use i3ipc within an application rather on the command-line:
#       because in practice one must wait for events to avoid race conditions.
#  Should I make this use i3ipc. This might be odd. But I suppose it isn't really, you can have as many connections to i3ipc as you want
#  and 3 isn't that many. However, I am feeling lazy at the moment and this is convenience code so polling is fine. Nothing here is
#  performance or latency sensitive enough that I mind brain-dead polling.

def spawn_on(name, command, conn=None):
    "Run a command on a workspace."
    with with_conn(conn) as conn:
        with with_workspace(name, conn):
            pin_workspace(conn)
            spawn_on_raw(name, command)

def spawn_on_raw(name, command):
    subprocess.Popen('workspace web; exec {}'.format(pipe.quote(command), shell=True))

@contextlib.contextmanager
def with_workspace(name, conn=None):
    "Execute the context on a workspace."
    with with_conn(conn) as conn:
        previous = current_workspace(conn)
        goto_workspace(name, conn)
        try:
            yield
        finally:
            goto_workspace(previous, conn)

# snippet: withconn: with with_conn(conn) as conn:
# snippet: cen: conn=None

def wait_for_workspace(name, conn=None):
    "Wait until a given workspace is selected."
    for i in range(100):
        current = current_workspace(conn)
        if current == name:
            break
        time.sleep(0.01)
    else:
        raise Exception((name, current))

def goto_workspace(name, conn=None):
    "Go to a workspace called name."
    with with_conn(conn) as conn:
        subprocess.check_call(['i3-msg', 'workspace {}'.format(name)])
    wait_for_workspace(name)

def current_workspace(conn=None):
    "Return the name of the current workspace."
    with with_conn(conn) as conn:
        return conn.get_tree().find_focused().workspace().name

def pin_workspace(conn=None):
    "Ensure that a workspace does get deleted (Use a layout with a universal swallowing window)."
    layout = '''
// vim:ts=4:sw=4:et
{
    "border": "normal",
    "current_border_width": 5,
    "floating": "auto_off",
    "geometry": {
       "height": 698,
       "width": 1134,
       "x": 0,
       "y": 0
    },
    "name": "workspace placehold",
    "percent": 1,
    "swallows": [
       {
       // "class": "^Mate\\-terminal$",
       // "instance": "^mate\\-terminal$",
       "title": ".*"
       //"window_role": "^mate\\-terminal\\-window\\-11469\\-1549304528\\-1541954984$"
       }
    ],
    "type": "con"
}
    '''

    with with_conn(conn) as conn:
        workspace = current_workspace(conn)
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            temp.write(layout.encode('utf8'))
            temp.close()
            subprocess.check_call([b"i3-msg", "append_layout {}".format(temp.name).encode('utf8')])
        # stupid race condition on append_lay
        for i in range(100):
            # This could be done with a subscription... but that does kind of undermine the purpose of this tool!
            tree = conn.get_tree()
            if tree.descendents():
                break
            time.sleep(0.01)

@contextlib.contextmanager
def with_conn(given_conn=None):
    "Connect and clean up the connection."
    conn = given_conn or i3ipc.Connection()
    try:
        yield conn
    finally:
        if not given_conn:
            conn.cmd_socket.close()

def run(event, *args):
    "Run a command in the context of an event."
    pin_workspace()
    command = ["i3-msg", "workspace {}; exec {}".format(event["current"]["name"], ' '.join(args))]
    print("Running", command)
    subprocess.Popen(command)

def read_events_stdin():
    "Return an iterator that yields dictionaries representing an i3 bus event."
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        try:
            data = json.loads(line)
        except:
            raise Exception("Could not parse {}".format(line))
        yield data
