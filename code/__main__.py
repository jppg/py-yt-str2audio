from yt_captions import YoutubeCaptions
from translate import Translate
from text2speech import Text2Speech
from nltk.tokenize import sent_tokenize
import asyncio
import shutil
import os
import nltk

nltk.download('punkt')

OUTPUT_DIR = 'output'

if os.path.isdir(OUTPUT_DIR):
    shutil.rmtree(OUTPUT_DIR)
os.makedirs(OUTPUT_DIR, exist_ok=True)

deepl_translator = Translate()

#https://docs.microsoft.com/en-US/azure/cognitive-services/speech-service/language-support
voice_en = 'en-US-GuyNeural' #'en-US-BrandonNeural'
voice_pt = 'pt-PT-RaquelNeural'
text2speech_en = Text2Speech(voice_en)
text2speech_pt = Text2Speech(voice_pt)

video = '_OkTw766oCs'
captions = YoutubeCaptions.get_youtube_captions(video)

concat_captions = ''
for line in captions:
    concat_captions = concat_captions + "{}\n".format(line['text'])

with open('tokenizer.txt', 'w') as ftok: 
    for tk in sent_tokenize(concat_captions):
        orig_sentence = tk.replace("\n", " ")
        ftok.write("{}\n".format(orig_sentence))

        print("English:", orig_sentence)

        if not orig_sentence.startswith("["):
            asyncio.run(text2speech_en.convert(orig_sentence))
            
            pt_text = deepl_translator.toPt(orig_sentence)
            print("Portuguese:", pt_text)
            asyncio.run(text2speech_pt.convert(pt_text))

print("End")