import curses


class Cli():
    def __init__(self):
        self.screen = curses.initscr()
        self.rows, self.cols = self.screen.getmaxyx()
        self.pad = curses.newpad(self.rows, self.cols)
        self.current_line = 0

        curses.noecho()

    def create_new_pad(self, num_rows=None, num_cols=None):
        self.pad = curses.newpad(
            self.rows if num_rows is None else num_rows,
            self.cols if num_cols is None else num_cols
        )

    def show_start_screen(self):
        self.screen.clean()
        self.screen.addstr("Welcome to YouSearch!\n\n")
        self.screen.addstr("Enter a YouTube URL: ")
        self.screen.refresh()
        curses.echo()
        url = self.screen.getstr()
        curses.noecho()
        return url

    def show_browse_screen(self):
        self.screen.addstr("Search for: ")
        self.screen.refresh()
        curses.echo()
        s = self.screen.getstr()
        curses.noecho()
        return s

    def test_pad(self):
        self.pad.addstr(5, 0, "Hallo")
        self.pad.refresh(0, 0, 0, 0, self.rows, self.cols)
        curses.napms(2000)


cli = Cli()
cli.show_browse_screen()
