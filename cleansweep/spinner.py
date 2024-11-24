import itertools
import time
import sys


def spinner(duration):
    spinner_cycle = itertools.cycle(['-', '/', '|', '\\'])
    end_time = time.time() + duration  # Run for the specified duration
    while time.time() < end_time:
        sys.stdout.write(f"\rLoading...{next(spinner_cycle)}")
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write("\r" + " " * 20 + "\r")  # Clear the line