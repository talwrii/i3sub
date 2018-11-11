# Run with PYTHONUNBUFFERED=yes i3sub --workspace |  PYTHONUNBUFFERED=yes python3 workspace_spawn.py

import traceback
import i3sub.spawn

def main():
    run = i3sub.spawn.run
    for event in i3sub.spawn.read_events_stdin():
        try:
            if event["change"] == "init":
                elif event["current"]["name"] == "reading":
                    # Spawn a firefox with profile reading on the reading desktop
                    run(event, "firefox",  "--new-instance",  "-P", "reading")
                    continue
                elif event["current"]["name"] == "youtube":
                    # Spawn a firefox with profile youtube on the youtube desktop
                    run(event, "firefox",  "--new-instance",  "-P", "youtube")
                    continue
                elif event["current"]["name"] == "working":
                    # Spawn gvim on the gvim desktop
                    run(event, "gvim")
                    continue

        except:
            print(traceback.format_exc())

        #print("Not handling: {}".format(json.dumps(event)))


if __name__ == '__main__':
	main()
