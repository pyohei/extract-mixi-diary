"""Extract and Save mixi diary."""
import argparse
import os

import parser
from extract import Extractction
import time


def main():
    """Main script."""
    args = _parse_argument()
    # Load diary id(unique).
    for r, d, fs in os.walk(args.org):
        for f in fs:
            path = os.path.join(r, f)
            parser.parse(path)
    diary_ids = parser.values

    # Request and save diary.
    e = Extractction(9999, args.dst)
    for i in diary_ids:
        e.save_diary(i)
        time.sleep(2)


def _parse_argument():
    """Parse argument."""
    p = argparse.ArgumentParser(description='Mixi diary save script.')
    p.add_argument('--consumer', '-c', help='consumer key', required=True)
    p.add_argument('--secret', '-s', help='secret key', required=True)
    p.add_argument('--port', '-p', help='port number of access key', required=True, type=int)
    p.add_argument('--org', '-o', help='original mixi html dir', required=True)
    p.add_argument('--dst', '-d', help='output directory of diary', required=True)

    args = p.parse_args()
    if not os.path.isdir(args.org):
        print('Your mixi html directory is not found.')
        quit()
    return args

main()
