import argparse
import datetime
import pickle
import subprocess
import time


AWAKE_FILE = '/tmp/marchanddesable'


# First, let's define how we act on the rest of the world

def online(server):
    return not subprocess.call(['ping', '-c3', server], stdout=subprocess.PIPE)


def shutdown():
    subprocess.call(['halt'])


# Then, let's define how we keep our state

def save_awake():
    with open(AWAKE_FILE, 'w') as f:
        f.write(str(time.time()))


def last_awake():
    try:
        with open(AWAKE_FILE) as f:
            return datetime.datetime.fromtimestamp(float(f.read()))
    except IOError:
        return datetime.datetime.fromtimestamp(0)


# At last, the show can start

def should_turn_off(machines):
    if not online('8.8.8.8'):
        # If I can access google, maybe I'm off the network. Better do nothing this time
        return False

    if 7 < datetime.datetime.now().hour < 23:
        # I turn my computer off during the day, but I don't want the server to turn off
        return False

    if any(online(machine) for machine in machines):
        return False
    return True


def tick(machines):
    if should_turn_off(machines):
        if (datetime.datetime.now() - last_awake()).seconds > 5*60:
            shutdown()
    else:
        save_awake()


# Finally, some command line stuff

def loop(machines):
    while True:
        tick(machines)
        time.sleep(60)


def main():
    parser = argparse.ArgumentParser(description='Halt the current machine 5 minutes after all the given machines are down.')
    parser.add_argument('machines', metavar='machine', nargs='+',
        help='A machine to check')
    parser.add_argument('--loop', '-l', action='store_true',
        help='Repeat the check every minutes instead of checking once')

    args = parser.parse_args()
    if args.loop:
        loop(args.machines)
    else:
        tick(args.machines)


if __name__ == '__main__':
    main()