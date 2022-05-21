from youtube_transcript_api import YouTubeTranscriptApi
#pip install python-certifi-win32

class YoutubeCaptions:
    def get_youtube_captions(video_code):
        return YouTubeTranscriptApi.get_transcript(video_code)

