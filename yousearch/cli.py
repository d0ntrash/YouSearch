import curses
from yousearch import youtube_api


class Cli():
    def __init__(self):
        self.screen = curses.initscr()
        self.rows, self.cols = self.screen.getmaxyx()

        curses.noecho()

    def show_start_screen(self):
        self.screen.clear()
        self.screen.addstr("Welcome to YouSearch!\n\n")
        self.screen.addstr("Enter a YouTube URL: ")
        self.screen.refresh()
        curses.echo()
        url = self.screen.getstr()
        curses.noecho()
        return url.decode()

    def show_browse_screen(self):
        self.screen.clear()
        self.screen.addstr("Search for: ")
        self.screen.refresh()
        curses.echo()
        keystring = self.screen.getstr()
        curses.noecho()
        return keystring.decode()

    def show_search_results(self, result):
        self.screen.clear()
        pad = curses.newpad(len(result)+2, self.cols)
        pad.addstr("Select a result to start the video!")
        line_pointer = 2
        pad.refresh(line_pointer, 0, 0, 0, self.rows - 1, self.cols - 1)
        curses.napms(2000)

    def cli(self):
        while True:
            url = self.show_start_screen()
            video = youtube_api.Video(url)
            keystring = self.show_browse_screen()
            search_result = video.search_string(keystring)
            if len(search_result) < 0:
                self.show_search_results(search_result)

    def test_pad(self):
        self.pad.addstr(5, 0, "Hallo")
        self.pad.refresh(0, 0, 0, 0, self.rows, self.cols)
        curses.napms(2000)


cli = Cli()
cli.cli()
