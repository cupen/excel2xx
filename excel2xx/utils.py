import sys

__author__ = 'cupen'


def show_progress(progress, barLength=10):
    """
    show progressbar
    inspired by http://stackoverflow.com/questions/3160699/python-progress-bar/3162864
    """
    status = ""
    if isinstance(progress, int):
        progress = float(progress)

    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"

    if progress < 0:
        progress = 0
        status = "Halt...\r\n"

    if progress >= 1:
        progress = 1
        status = "Done...\r\n"

    block = int(round(barLength * progress))
    text = "\rPercent: [{0}] {1}% {2}".format("#" * block + "-" * (barLength - block), int(progress * 100), status)
    sys.stdout.write(text)
    sys.stdout.flush()
    pass
