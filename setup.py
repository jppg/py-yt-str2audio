from setuptools import setup, find_packages

setup(
    name='py-yt-str2audio',
    version='0.1.0',
    packages=find_packages(include=['code', 'code.*']),
    install_requires=[
        'configparser',
        'deepl',
        'youtube_transcript_api'
    ]
)