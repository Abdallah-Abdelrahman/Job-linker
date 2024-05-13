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
from dateutil.parser import parse, ParserError
from server.exception import UnreadableCVError
from server.prompts import CANDID_PROMPT, JOB_PROMPT, ATS_FRIENDLY_PROMPT


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
            if not txt:
                raise UnreadableCVError()
            return txt
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
            raise UnreadableCVError()

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
            #txt_cp = ''.join([c for c in text if c not in '\n'])
            dict_ = loads(text)
            xps = dict_.get('experiences')
            eds = dict_.get('educations')
            for xp in xps:
                for k, v in xp.items():
                    if k == 'description':
                        # replace bullet-points and new line character,
                        # with empty string.
                        # 8226 is the unicode for bullet point
                        xp[k] = v.replace('\n', '').replace(chr(8226), '')
                    if k in ('start_date', 'end_date'):
                        try:
                            xp[k] = parse(v).isoformat()
                        except (ParserError, TypeError):
                            xp[k] = datetime.utcnow().isoformat()
            for ed in eds:
                for k, v in ed.items():
                    if k in ('start_date', 'end_date'):
                        try:
                            ed[k] = parse(v).isoformat()
                        except (ParserError, TypeError):
                            ed[k] = datetime.utcnow().isoformat()
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
    ai = AIService(pdf=f'{getcwd()}/server/cv/2024-05-13-01-02-49_Abdallah.pdf')
    dict_ = ai.to_dict(CANDID_PROMPT)
    print(dict_)
    #print(ai.get_insights())
    '''
    for pdf in listdir('pdf'):
        ai = AIService(pdf=path.join('pdf', pdf))
        dict_ = ai.to_dict(prompts.CANDID_PROMPT)
        print(dict_)
        print('---------->', type(dict_))
        '''
