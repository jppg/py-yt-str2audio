#!/usr/bin/env python3
"""
Example Python script that shows how to use edge-tts as a module
"""
import edge_tts
import time
import os

class Text2Speech:
    def __init__(self, voice) -> None:
        self.voice = voice
        self.communicate = edge_tts.Communicate()

    async def convert(self, text):
        OUTPUT_DIR = 'output'
        #try:
        filename = os.path.join(OUTPUT_DIR, 'record.mp3')
        with open(filename, 'ab') as temporary_file:
            async for i in self.communicate.run(text, voice=self.voice):
                if i[2] is not None:
                    temporary_file.write(i[2])
        #except Exception as e:
        #    print(e)
    

      