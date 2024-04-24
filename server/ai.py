#!/usr/bin/env python3
'''The module defines AI service that parses a pdf file,
generate a dictionary of info of the cv using gemini.
'''
from os import getenv, listdir, path
from json import loads, JSONDecodeError
from pdfminer.high_level import extract_text
from pdfminer.pdfparser import PDFSyntaxError
import google.generativeai as genai
import prompts


class AIService():
    '''class AIService

    Attrs:
        generation_config: gemini config
        safety_settings: safety settings
    '''
    # Set up the model
    generation_config = {
        'temperature': 0.9,
        'top_p': 1,
        'top_k': 1,
        'max_output_tokens': 2048,
    }

    safety_settings = [
        {
            'category': 'HARM_CATEGORY_HARASSMENT',
            'threshold': 'BLOCK_MEDIUM_AND_ABOVE'
        },
        {
            'category': 'HARM_CATEGORY_HATE_SPEECH',
            'threshold': 'BLOCK_MEDIUM_AND_ABOVE'
        },
        {
            'category': 'HARM_CATEGORY_SEXUALLY_EXPLICIT',
            'threshold': 'BLOCK_MEDIUM_AND_ABOVE'
        },
        {
            'category': 'HARM_CATEGORY_DANGEROUS_CONTENT',
            'threshold': 'BLOCK_MEDIUM_AND_ABOVE'
        },
    ]

    def __init__(self, cv='cv/moe.pdf'):
        '''Initialze the ai model

        Args:
            cv(str): path to resume file
        '''
        genai.configure(api_key=getenv('GOOGLE_API_KEY'))

        self.cv = cv
        self.model = genai.GenerativeModel(
            model_name='gemini-1.0-pro',
            generation_config=self.generation_config,
            safety_settings=self.safety_settings)

    def parse_cv(self):
        '''extract text from pdf'''
        try:
            txt = extract_text(self.cv).strip()
            return txt if txt else None
        except FileNotFoundError:
            print('File not found or path is incorrect')
            raise
        except PDFSyntaxError:
            print('Not a valid pdf file')
            raise

    def prompt(self, line):
        '''ask gemeni and generate a response.
        based on the pdf file.

        Args:
            line: prompt to provide for gemini
        Notes:
            the function assumes there's a pdf file called cv.pdf
            feel free to change this to obtain some info about the the cv
        '''
        input_ = self.parse_cv()
        if not input_:
            print(self.cv)
            raise ValueError('Text is empty')

        resp = self.model.generate_content([line, input_], stream=True)
        text = ''
        for chunk in resp:
            text += chunk.text
        return text

    def to_dict(self, prompt_enquery):
        '''The function translates gemeni response to a dictionary

        Args:
            prompt_enquery(str): question to feed it to gemini
        Returns:
            dictionary of gemini response
        '''
        text = self.prompt(prompt_enquery)
        try:
            # strips out any spaces or new lines or back-slashes
            txt_cp = ''.join([c for c in text if c not in '\n\\'])
            return loads(txt_cp)
        except JSONDecodeError as e:
            print('--------->', self.cv, e)
            raise


if __name__ == '__main__':
    for pdf in listdir('cv'):
        ai = AIService(cv=path.join('cv', pdf))
        dict_ = ai.to_dict(prompts.CANDID_PROMPT)
        print(dict_)
        print('---------->', type(dict_))
