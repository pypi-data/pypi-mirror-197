"""__main__

Copyright (C) 2023 @mahtin - Martin J Levy - W6LHI/G8LHI - https://github.com/mahtin
"""

import sys
from wwvb import wwvb

def main(args=None):
    """ WWVB API via command line """
    if args is None:
        args = sys.argv[1:]
    wwvb.wwvb(args)

if __name__ == '__main__':
    main()
