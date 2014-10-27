import sys
from colorama import init, deinit, Fore


class TerminalProgressBar():
    '''
    A terminal applet for displaying a progress bar.

    PROGRESS VARIABLES
            status

                    A string corresponding to the progress bar title.

            status_width

                    An integer detailing the maximum length of a bar title.

            bar_width

                    An integer detailing the length of the progress bar.

            bar_handles

                    A list of of length 2 containing strings.  Default ['[', ']']

            increment_char

                    A single character string detailing the character used for showing progress.
                    Default '='

            done

                    boolean value representing whether or not the process is complete.

    FUNCTIONS
            set(...)

                    set(property=setting, )

                    Sets progress bar property to desired setting and updates display.

            percentage(...)

                    percentage(x)

                    Sets the progress bar to x percentage of completion.
                    Expects a value between 0 and 100, inclusive.
    '''

    def __init__(self):
        # colorama
        init()
        self.statusfore = Fore.WHITE
        self.in_progress_status_color = Fore.YELLOW
        self.done_status_color = Fore.BLUE
        self.handlefore = Fore.GREEN
        self.incrfore = Fore.RED

        # number of increment characters
        self.progress = 0

        # progress variables
        self.pv = {
            'status': "Initializing...",
            'status_width': 25,
            'bar_width': 45,
            'bar_handles': ['[', ']'],
            'increment_char': '+',
            'done': False,
        }
        self.update()

    def update(self):
        sys.stdout.write(
            '\b' * (self.pv['status_width'] + self.pv['bar_width']))
        sys.stdout.write(
            ' ' * (self.pv['status_width'] + self.pv['bar_width']))
        sys.stdout.write(
            '\b' * (self.pv['status_width'] + self.pv['bar_width']))
        sys.stdout.write(
            Fore.RESET +
            self.statusfore +
            self.pv['status'][
                :self.pv['status_width']])
        sys.stdout.write(
            ' ' * (self.pv['status_width'] - len(self.pv['status'])))
        sys.stdout.write(
            Fore.RESET +
            self.handlefore +
            self.pv['bar_handles'][0])
        sys.stdout.write(
            Fore.RESET +
            self.incrfore +
            self.pv['increment_char'] *
            self.progress)
        sys.stdout.write(' ' * (self.pv['bar_width']
                                - self.progress
                                - len(self.pv['bar_handles'][0])
                                - len(self.pv['bar_handles'][1])))
        sys.stdout.write(
            Fore.RESET +
            self.handlefore +
            self.pv['bar_handles'][1])
        sys.stdout.flush()

    def set(self, **kwargs):
        self.pv.update(kwargs)
        if not self.pv['done']:
            self.statusfore = self.in_progress_status_color
        else:
            self.statusfore = self.done_status_color
            deinit()
        self.update()

    def percentage(self, perc):
        max_width = self.pv['bar_width'] - len(''.join(self.pv['bar_handles']))
        prog = int(max_width * perc * .01)
        self.progress=prog


def main():
    import time
    print 'Program will complete in 20 seconds'
    tpb = TerminalProgressBar()
    start = time.time()
    now = time.time()
    while now - start <= 20.:
        tpb.percentage(100. * (now - start) / 20.)
        tpb.set(status=str(now - start))
        now = time.time()
    tpb.percentage(100.)
    tpb.set(status='Finished!', done=True)
    print '\n\n'

if __name__ == '__main__':
    main()
