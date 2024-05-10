#!/usr/bin/env python3
'''The module defines AI service that parses a pdf file,
generate a dictionary of info of the pdf using gemini.
'''
from datetime import datetime
from os import getenv, listdir, path, getcwd
from json import loads, JSONDecodeError
from pdfminer.high_level import extract_text
from pdfminer.pdfparser import PDFSyntaxError
import google.generativeai as genai
from server.prompts import CANDID_PROMPT, JOB_PROMPT
from dateutil.parser import parse


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

    def __init__(self, pdf=''):
        '''Initialze the ai model

        Args:
            pdf(str): path to resume file
        '''
        genai.configure(api_key=getenv('GOOGLE_API_KEY'))

        self.__insights = None
        self.pdf = pdf
        self.model = genai.GenerativeModel(
            model_name='gemini-1.0-pro',
            generation_config=self.generation_config,
            safety_settings=self.safety_settings)

    def parse_pdf(self, pdf=''):
        '''extract text from pdf'''
        try:
            txt = extract_text(pdf or self.pdf).strip()
            return txt if txt else None
        except FileNotFoundError:
            print('File not found or path is incorrect')
            raise
        except PDFSyntaxError:
            print('Not a valid pdf file')
            raise

    def prompt(self, line, input_txt=None):
        '''ask gemeni and generate a response.
        based on the pdf file.

        Args:
            line: prompt to provide for gemini
            input_txt: input to extract the info from
        Notes:
            the function assumes there's a pdf file called pdf.pdf
            feel free to change this to obtain some info about the the pdf
        '''
        input_ = input_txt or self.parse_pdf()
        if not input_:
            print(self.pdf)
            raise ValueError('Text is empty')

        resp = self.model.generate_content([line, input_], stream=True)
        text = ''
        for chunk in resp:
            text += chunk.text
        return text

    def to_dict(self, prompt_enquiry, text=''):
        '''The function translates gemeni response to a dictionary

        Args:
            prompt_enquery(str): question to feed it to gemini
        Returns:
            dictionary of gemini response
        '''
        if not text:
            text = self.prompt(prompt_enquiry)
        try:
            # strips out any spaces or new lines or back-slashes
            txt_cp = ''.join([c for c in text if c not in '\n\\'])
            dict_ = loads(txt_cp)
            for k,v in dict_.items():
                if k == 'experiences':
                    for xp in dict_.get('experiences'):
                        print(xp['start_date'], '--------START------------->')
                        print(xp['end_date'], '--------END------------->')
                        xp['start_date'] = parse(str(xp.get('start_date') or datetime.utcnow()))
                        xp['end_date'] = parse(str(xp.get('end_date') or datetime.utcnow()))
            self.__insights = dict_
            return dict_
        except JSONDecodeError as e:
            # retry unitl we get valid json
            print('---JSON issues------>', self.pdf, e)
            return self.to_dict(prompt_enquiry)

    def get_insights(self):
        '''Retreive insights about resume'''
        # TODO:
        prompt = """\
            As a professional applicant tracking system, please provide a detailed analysis of this CV. The analysis should include:
            {
            "ats_score": "<float: ATS friendliness score between 0.0 and 1.0>",
            "suggestions": ["<str: Suggestion 1>", "<str: Suggestion 2>", "..."],
            }
        
            Notes:
            - 'ats_score' should be a float between 0.0 and 1.0, where 1.0 means the CV is perfectly ATS-friendly and 0.0 means it's not ATS-friendly at all.
            - 'suggestions' should be a list of suggestions for improving the CV to make it more ATS-friendly.
            """
        return self.prompt(prompt)


if __name__ == '__main__':
    ai = AIService(pdf=f'{getcwd()}/server/cv/Abdallah.pdf')
    #dict_ = ai.to_dict(CANDID_PROMPT)
    print(ai.get_insights())
    '''
    for pdf in listdir('pdf'):
        ai = AIService(pdf=path.join('pdf', pdf))
        dict_ = ai.to_dict(prompts.CANDID_PROMPT)
        print(dict_)
        print('---------->', type(dict_))
        '''
