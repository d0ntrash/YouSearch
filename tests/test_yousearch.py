from yousearch import __version__
from yousearch import youtube_api

video_url = "https://www.youtube.com/watch?v=5y_SbnPx_cE"
expected_vid = "5y_SbnPx_cE"
expected_title = "Hackers (10/13) Movie CLIP " \
    + "- Hack the Planet (1995) HD - YouTube"
expected_transcript = [{'text': "alright I'm trashing the floor like that",
                        'start': 27.439, 'duration': 10.21},
                       {'text': 'oh thanks rushing rushing rushing like',
                        'start': 31.23, 'duration': 12.23},
                       {'text': 'the planet hide up get in the car',
                        'start': 37.649, 'duration': 5.811},
                       {'text': 'hello',
                        'start': 52.309, 'duration': 5.921},
                       {'text': "we caught red-handed you won't be having",
                        'start': 53.55, 'duration': 7.849},
                       {'text': 'any more trouble from them',
                        'start': 58.23, 'duration': 3.169}]


def test_version():
    assert __version__ == '0.1.0'


def test_extract_vid():
    assert youtube_api.extract_vid(video_url) == expected_vid


def test_get_video_title():
    assert youtube_api.get_video_title(video_url) == expected_title


def test_get_transcript():
    assert youtube_api.get_transcript(
        expected_vid, ["en"]) == expected_transcript
