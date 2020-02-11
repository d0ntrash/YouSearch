import curses
from yousearch import youtube_api
from yousearch import mpv_api


class Cli():
    def __init__(self):
        self.screen = curses.initscr()
        self.rows, self.cols = self.screen.getmaxyx()
        self.exit_result_screen = False
        self.exit_search_screen = False
        curses.noecho()

    def refresh_window_size(self):
        self.rows, self.cols = self.screen.getmaxyx()

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

    def get_direction(self, pad):
        while True:
            key = pad.getch()
            if key == curses.KEY_UP or key == 16:
                return -1
            if key == curses.KEY_DOWN or key == 14:
                return 1
            if key == curses.KEY_ENTER or key == 10:
                return 2
            if key == ord('q'):
                self.exit_result_screen = True
                return 3

    def show_search_results(self, results):
        self.screen.clear()
        pad = curses.newpad(len(results)+2, self.cols)
        pad_rows, pad_cols = pad.getmaxyx()
        pad.addstr("Select a result to start the video!")
        pad.keypad(True)
        line_pointer = 2
        cursor_pointer = 2
        for result in results:
            pad.addstr(line_pointer, 1,
                       f"{line_pointer - 1}. {result['text']}")
            pad.addstr(line_pointer, self.cols - 20,
                       beautify_startpoint(result['start']))
            line_pointer += 1

        enter_flag = False
        while not enter_flag and not self.exit_result_screen:
            pad.move(cursor_pointer, 0)
            pad.chgat(curses.A_REVERSE)
            if cursor_pointer >= self.rows:
                pad.refresh(cursor_pointer - self.rows + 1, 0,
                            0, 0, self.rows - 1, self.cols - 1)
            else:
                pad.refresh(0, 0, 0, 0, self.rows - 1, self.cols - 1)
            key = self.get_direction(pad)
            pad.chgat(curses.A_NORMAL)
            if key == 2:
                enter_flag = True
            elif cursor_pointer + key in range(2, pad_rows):
                cursor_pointer += key
        return cursor_pointer - 2

    def start_video_screen(self):
        self.screen.clear()
        self.screen.addstr("Starting video...\n")
        self.screen.addstr("This might take a few seconds.")
        self.screen.refresh()

    def cli(self):
        while True:
            url = self.show_start_screen()
            video = youtube_api.Video(url)
            if video.vid is None:
                # Continue if the video id can't be extracted
                self.screen.clear()
                self.screen.addstr(1, 0, "Invalid URL!")
                self.screen.refresh()
                curses.napms(1000)
                continue

            video.fetch_transcript()
            # Continue if the transcript can be fetched
            if video.transcript_dict is None:
                self.screen.clear()
                self.screen.addstr(1, 0, "No transcript available!")
                self.screen.refresh()
                curses.napms(1000)
                continue

            while not self.exit_search_screen:
                self.refresh_window_size()
                keystring = self.show_browse_screen()
                search_result = video.search_string(keystring)
                if len(search_result) == 0:
                    # continue if no match is found
                    self.screen.clear()
                    self.screen.addstr("No match found!")
                    self.screen.refresh()
                    curses.napms(1000)
                    continue

                while not self.exit_result_screen:
                    self.refresh_window_size()
                    result_index = self.show_search_results(search_result)
                    if not self.exit_result_screen:
                        self.start_video_screen()
                        mpv_api.start_video(
                            url, search_result[result_index]["start"] - 1.5)
                        self.screen.clear()
                        self.screen.refresh()

                self.exit_result_screen = False
            self.exit_search_screen = False


def beautify_startpoint(seconds):
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"  {m:02d}:{s:02d}"


def main():
    cli = Cli()
    curses.wrapper(cli.cli())


if __name__ == '__main__':
    main()
