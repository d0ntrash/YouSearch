import subprocess
from yousearch import config


def start_video(url, offset=0):
    """Starts video in a mpv subprocess

    More mpv options can be added by extending 'MPV_OPTIONS'
    in the config.py file. Type 'mpv --list-options' to list all options.

    :url: Youtube video ulr
    :offset: defines where to start the video

    TODO: Error Handling
    """
    subprocess.run(["mpv", url, f"--start={offset}"] + config.MPV_OPTIONS)
    return
