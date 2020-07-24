import signal
import time
import sys
import os
import argparse
import logging
exit_flag = False
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formater = logging.Formatter(
    '%(asctime)s %(levelname)s %(threadName)s %(message)s')
handler.setFormatter(formater)
logger.addHandler(handler)


def signal_handler(sig_num, frame):
    """
    This is a handler for SIGTERM and SIGINT. Other signals can be mapped here as well (SIGHUP?)
    Basically, it just sets a global flag, and main() will exit its loop if the signal is trapped.
    :param sig_num: The integer signal number that was trapped from the OS.
    :param frame: Not used
    :return None
    """
    # log the associated signal name
    global exit_flag
    exit_flag = True
    logger.warning('Received ' +
                   signal.Signals(sig_num).name)


def log_close(end_time):
    logger.info('\n' + 40 * '-' + '\nStopped dirwatcher.py\nUptime was ' +
                str(end_time) + ' seconds' + '\n' + 40 * '-')


def log_start():
    logger.info('\n' + 40 * '-' +
                '\nStarting dirwatcher.py' + '\n' + 40 * '-')


def check_dir(dir):
    # watcher function
    pass


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', help='directory to watch')
    parser.add_argument('ext', help='file extension to filter')
    parser.add_argument('int', help='polling interval')
    parser.add_argument('magic', help='magic text to scan for')
    return parser


def main(args):
    # Hook into these two signals from the OS
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    # Now my signal_handler will get called if OS sends
    # either of these to my process.
    log_start()
    start_time = time.time()
    parser = create_parser()
    logging.basicConfig(filename='dirwatcher.log')
    if not args:
        parser.print_usage()
        log_close(time.time()-start_time)
        sys.exit(1)
    parsed_args = parser.parse_args(args)
    while not exit_flag:
        try:
            check_dir(parsed_args.dir)
            pass
        except Exception as e:
            logger.error(e)
            # This is an UNHANDLED exception
            # Log an ERROR level message here
            pass

        # put a sleep inside my while loop so I don't peg the cpu usage at 100%
        time.sleep(int(parsed_args.int))
    if exit_flag:
        log_close(time.time()-start_time)
        sys.exit(1)


    # final exit point happens here
    # Log a message that we are shutting down
    # Include the overall uptime since program start
if __name__ == '__main__':
    main(sys.argv[1:])
