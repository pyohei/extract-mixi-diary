"""Extract mixi diary

Created at 2014-07-06.
"""

import parser
import extract
import time


def main():
    diary_ids = parser.parse()
    for i in diary_ids:
        extract.get_diary(i)
        time.sleep(2)


main()
