import sys

def print_progress(iteration, total, prefix='', suffix='Complete', decimals=1, length=50, fill='█', print_end='\r', color="green"):
    """
    Call in a loop to create a progress bar in the console.
    'iteration'   - Required  : current iteration (Int)
    'total'       - Required  : total iterations (Int)
    'prefix'      - Optional  : prefix string (Str)
    'suffix'      - Optional  : suffix string (Str)
    'decimals'    - Optional  : number of decimals in percent complete (Int)
    'length'      - Optional  : character length of bar (Int)
    'fill'        - Optional  : bar fill character (Str)
    'print_end'   - Optional  : end character (e.g. "\r", "\r\n") (Str)
    'color'       - Optional  : color of progress bar (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    if color is not None:
        if iteration == total:
            bar = '\033[92m' + bar + '\033[0m' # green
        else:
            bar = '\033[93m' + bar + '\033[0m' # yellow
    sys.stdout.write('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix))
    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()


if __name__=="__main__":
    # example usage
    import time

    total = 103
    for i in range(total):
        # do some work here
        time.sleep(0.1)
        # update progress bar
        print_progress(i + 1, total, prefix='Progress:')
    # example usage
    import time

    total = 103
    for i in range(total):
        # do some work here
        time.sleep(0.1)
        # update progress bar
        print_progress(i + 1, total, prefix='Progress:')

