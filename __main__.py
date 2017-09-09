from sys import exit
from signal import signal, SIGTERM, SIGHUP
from locale import (setlocale, LC_ALL, Error as LocaleError)

from main import main

# -----------------   SYSTEM   ----------------- #


try:
    setlocale(LC_ALL, ('pl_PL', 'UTF-8'))
except LocaleError:
    print('pl_PL.UTF-8 locale not installed')

def sigterm_exeption(signum, frame):
    exit()


def sighup_exeption(signum, frame):
    exit()


signal(SIGTERM, sigterm_exeption)
signal(SIGHUP, sighup_exeption)


# ------------------   MAIN   ------------------ #


if __name__ == '__main__':
    try:
        while True:
            main()
    except KeyboardInterrupt:
        exit()
