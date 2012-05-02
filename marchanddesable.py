import argparse
import subprocess
import time


def online(server):
    return not subprocess.call(['ping', '-c3', server], stdout=subprocess.PIPE)


def shutdown():
    subprocess.call(['halt'])


class MarchandDeSable:
    def __init__(self, machines):
        self.machines = machines
        self.times_down = 0

    def tick(self):
        if not any(online(server) for server in self.machines):
            self.times_down += 1
            if self.times_down >= 5:
                shutdown()
        else:
            self.times_down = 0

    def loop(self):
        while True:
            self.tick()
            time.sleep(60)


def main():
    parser = argparse.ArgumentParser(description='Halt the current machine 5 minutes after all the given machines are down.')
    parser.add_argument('machines', metavar='machine', nargs='+',
        help='A machine to check')

    args = parser.parse_args()

    MarchandDeSable(args.machines).loop()


if __name__ == '__main__':
    main()