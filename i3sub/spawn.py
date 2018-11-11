import subprocess
import time
import subprocess
import tempfile
import sys
import json

def pin_workspace():
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
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        temp.write(layout.encode('utf8'))
        temp.close()
        subprocess.check_call([b"i3-msg", "append_layout {}".format(temp.name).encode('utf8')])
    time.sleep(0.5)
    # stupid race condition on append_lay


def run(event, *args):
    "Run a command in the context of an event"
    pin_workspace()
    command = ["i3-msg", "workspace {}; exec {}".format(event["current"]["name"], ' '.join(args))]
    print("Running", command)
    subprocess.Popen(command)

def read_events_stdin():
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        try:
            data = json.loads(line)
        except:
            raise Exception("Could not parse {}".format(line))
        yield data

