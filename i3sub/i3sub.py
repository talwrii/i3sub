import argparse
import json
import pprint
import i3ipc
import types


def build_parser():
    parser = argparse.ArgumentParser(description='Subscribe to i3 events', prog='i3sub')
    filter_mx = parser.add_mutually_exclusive_group()

    filter_mx.add_argument('--quiet', action='store_true', default=False, help='Only show event types')
    filter_mx.add_argument('--short', action='store_true', default=False, help='Only show event types')

    run_mx = parser.add_mutually_exclusive_group()
    run_mx.add_argument('--no-run', action='store_const', help='Exclude actions events', const=False, dest='run')
    run_mx.add_argument('--run', action='store_const', help='Show only actions events', const=True, dest='run')

    focus_mx = parser.add_mutually_exclusive_group()
    focus_mx.add_argument('--no-focus', action='store_const', help='Exclude focus events', const=False, dest='focus')
    focus_mx.add_argument('--focus', action='store_const', help='Show only focus events', const=True, dest='focus')

    workspace_mx = parser.add_mutually_exclusive_group()
    workspace_mx.add_argument('--no-workspace', action='store_const', help='Exclude action events', const=False, dest='workspace')
    workspace_mx.add_argument('--workspace', action='store_const', help='Show only action events', const=True, dest='workspace')

    return parser

class Handler(object):
    def __init__(self, formatter, filter):
        self.formatter = formatter
        self.filter = filter

    def handle(self, connection, event):
        result = parse_event(event)
        if self.filter(result):
            print(self.formatter(result))

def parse_event(event):
    result = dict()
    for k, v in vars(event).items():
        new_k, new_value = encode(k, v)
        result[new_k] = new_value
    return result


def encode(key, value):
    try:
        if isinstance(value, list):
            return key, [encode('_', x)[1] for x in value]
        if value is not None and not isinstance(value, (float, str, int)):
            variables = dict(vars(value))
            variables.pop('parent', None)
            variables.pop('props', None)
            variables.pop('_pubsub', None)
            variables.pop('cmd_socket', None)
            variables.pop('sub_socket', None)
            variables.pop('_conn', None)
            return key, dict(encode(k, v) for k, v in variables.items())
        else:
            return key, value
    except EncodeFailure:
        raise
    except Exception as exc:
        raise EncodeFailure(key, value) from exc

class EncodeFailure(Exception):
    def __init__(self, key, value):
        Exception.__init__(self)
        self.key = key
        self.value = value

    def __str__(self):
        return 'Failed to parse: {}, {}, {}'.format(self.key, self.value, vars(self.value))


def quiet_formatter(result):
    return result['change']

def short_formatter(result):
    "A formatter that tries to give a good summary of an event"
    return '{}: {}'.format(result['change'])



def combine_filters(*filters):
    def result(x):
        return all(flt(x) for flt in filters)
    return result

def true_filter(_):
    return True


def change_filter(change_value, negate):
    def flt(event):
        result = not change_value or event['change'] == change_value
        if negate:
            return not result
        else:
            return result

    return flt

def main():
    args = build_parser().parse_args()
    i3 = i3ipc.Connection()

    event_filter = true_filter

    if args.run is not None:
        event_filter = combine_filters(event_filter, change_filter('run', not args.run))

    if args.focus is not None:
        event_filter = combine_filters(event_filter, change_filter('focus', not args.focus))

    if args.quiet:
        formatter = quiet_formatter
    else:
        formatter = json.dumps

    handler = Handler(formatter, event_filter)

    WORKSPACE = "workspace"

    types = set(("ipc_shutdown", WORKSPACE, "output", "mode", "window", "barconfig_update", "binding"))

    if args.workspace == True:
        types = set((WORKSPACE,))
    elif args.workspace == False:
        types.remove(WORKSPACE)

    for name in types:
        i3.on(name, handler.handle)

    i3.main()
