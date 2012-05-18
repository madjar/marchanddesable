#!/usr/bin/python3
import argparse
import datetime
import subprocess
import time
import logging
import logging.handlers


AWAKE_FILE = '/tmp/marchanddesable'


# First, let's define how we act on the rest of the world

def online(server):
    return not subprocess.call(['ping', '-c3', server], stdout=subprocess.PIPE)


def shutdown():
    subprocess.call(['/sbin/halt'])


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
        logging.info('Internet connection has been lost, doing nothing.')
        return False

    if 7 < datetime.datetime.now().hour < 23:
        # I turn my computer off during the day, but I don't want the server to turn off
        logging.info("We're in the middle of the day, doing nothing.")
        return False

    if any(online(machine) for machine in machines):
        logging.info('A machine is up, doing nothing.')
        return False
    return True


def tick(machines):
    if should_turn_off(machines):
        time_since_condition_met = (datetime.datetime.now() - last_awake()).seconds
        logging.info('All conditions for shutdown have been met for %s seconds.', time_since_condition_met)
        if time_since_condition_met > 5*60:
            shutdown()
    else:
        save_awake()


# Finally, some command line stuff

def loop(machines):
    while True:
        tick(machines)
        time.sleep(60)


def configure_logging(handler):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def main():
    parser = argparse.ArgumentParser(description='Halt the current machine 5 minutes after all the given machines are down.')
    parser.add_argument('machines', metavar='machine', nargs='+',
        help='A machine to check')
    parser.add_argument('--loop', '-l', action='store_true',
        help='Repeat the check every minutes instead of checking once')
    parser.add_argument('--file', '-f', action='store',
        help='a file to log to. If no file is specified, logs to stderr')

    args = parser.parse_args()

    if args.file:
        configure_logging(logging.handlers.TimedRotatingFileHandler(args.file, when='midnight', backupCount=7))
    else:
        configure_logging(logging.StreamHandler())

    if args.loop:
        loop(args.machines)
    else:
        tick(args.machines)


if __name__ == '__main__':
    main()
