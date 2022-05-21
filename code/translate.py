import deepl
import configparser
#TODO: Checkout this python module --> https://pypi.org/project/deep-translator/

class Translate:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        deepl_auth_code = config['DEEPL']['auth_key']
        self.translator = deepl.Translator(deepl_auth_code)
        
        

    def toPt(self, text):
        result = ''
        translation = self.translator.translate_text(text, target_lang="PT-PT")
        if translation is not None:
            result = translation.text
        return result

    def get_languages(self):
        for language in self.translator.get_target_languages():
            if language.supports_formality:
                print(f"{language.code} ({language.name}) supports formality")
            else:
                print(f"{language.code} ({language.name})")