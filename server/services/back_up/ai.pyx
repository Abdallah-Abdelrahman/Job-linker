# ai.pyx
#!/usr/bin/env python3
"""The module defines AI service that parses a pdf, doc, or docx file,
generate a dictionary of info using gemini.
"""
from datetime import datetime
from json import JSONDecodeError, loads
from os import getenv, getcwd
from typing import Any, Dict, List, Optional

import google.generativeai as genai
from dateutil.parser import ParserError, parse
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv

from server.exception import UnreadableCVError
from server.prompts import CANDID_PROMPT, JOB_PROMPT
from server.services.text_extractor import extract_text

load_dotenv()


class AIService:
    """class AIService

    Attrs:
        generation_config: gemini config
        safety_settings: safety settings
    """

    # Set up the model
    generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }

    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
    ]

    def __init__(self, file_path: str = "") -> None:
        """Initialize the ai model

        Args:
            file_path(str): path to the resume or job description file
        """
        GOOGLE_API_KEY: Optional[str] = getenv("GOOGLE_API_KEY")
        genai.configure(api_key=GOOGLE_API_KEY)

        self.__insights: Optional[Dict[str, Any]] = None
        self.file_path: str = file_path
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=self.generation_config,
            safety_settings=self.safety_settings,
        )

    def prompt(self, line: str, input_txt: Optional[str] = None) -> str:
        """ask gemini and generate a response.
        based on the file content.

        Args:
            line: prompt to provide for gemini
            input_txt: input to extract the info from
        """
        input_: str = input_txt or extract_text(self.file_path)
        if not input_:
            print(self.file_path)
            raise UnreadableCVError()

        resp = self.model.generate_content([line, input_], stream=True)
        text: str = ""
        for chunk in resp:
            text += chunk.text
        return text

    def __handle_cv(self, dict_: Dict[str, Any]) -> Dict[str, Any]:
        """clean the dictionary received from ai"""
        xps: List[Dict[str, Any]] = dict_.get("experiences", [])
        eds: List[Dict[str, Any]] = dict_.get("educations", [])
        for xp in xps:
            for k, v in xp.items():
                if k == "description":
                    # replace bullet-points and new line character,
                    # with empty string.
                    # 8226 is the unicode for bullet point
                    xp[k] = v.replace("\n", "").replace(chr(8226), "")
                if k in ("start_date", "end_date"):
                    try:
                        xp[k] = parse(v).isoformat()
                    except (ParserError, TypeError):
                        xp[k] = datetime.utcnow().isoformat()
        for ed in eds:
            for k, v in ed.items():
                if k in ("start_date", "end_date"):
                    try:
                        ed[k] = parse(v).isoformat()
                    except (ParserError, TypeError):
                        ed[k] = datetime.utcnow().isoformat()
        return dict_

    def __handle_job(self, dict_: Dict[str, Any]) -> Dict[str, Any]:
        """clean the dictionary received from ai"""
        app_deadline: Optional[str] = dict_.get("application_deadline")
        desc: Optional[str] = dict_.get("job_description")
        if desc:
            dict_["job_description"] = desc.replace("\n", "")
        if app_deadline:
            try:
                dict_["application_deadline"] = parse(app_deadline).isoformat()
            except (ParserError, TypeError):
                one_month_ahead: datetime = datetime.utcnow() + relativedelta(months=1)
                dict_["application_deadline"] = one_month_ahead.isoformat()
        return dict_

    def clean_json_response(self, response_text: str) -> str:
        """Clean the JSON response by removing unwanted characters."""
        response_text = response_text.strip()

        if response_text.startswith("```json") and response_text.endswith("```"):
            response_text = response_text[7:-3].strip()
        elif response_text.startswith("```") and response_text.endswith("```"):
            response_text = response_text[3:-3].strip()

        return response_text

    def to_dict(self, prompt_enquiry: str, text: str = "", retries: int = 3) -> Dict[str, Any]:
        """The function translates gemini response to a dictionary

        Args:
            prompt_enquiry(str): question to feed it to gemini
            retries(int): number of retries in case of JSONDecodeError
        Returns:
            dictionary of gemini response
        """
        if not text:
            text = self.prompt(prompt_enquiry)

        cleaned_text: str = self.clean_json_response(text)

        try:
            dict_: Dict[str, Any] = loads(cleaned_text)
            if prompt_enquiry == CANDID_PROMPT:
                dict_ = self.__handle_cv(dict_)
            if prompt_enquiry == JOB_PROMPT:
                dict_ = self.__handle_job(dict_)
            return dict_
        except JSONDecodeError as e:
            print("---JSON issues------>", self.file_path, e)

            if retries > 0:
                return self.to_dict(prompt_enquiry, retries=retries - 1)
            else:
                return {"error": "Failed to parse JSON after retries"}

    def get_insights(self) -> str:
        """Retrieve insights about resume"""
        # TODO:
        prompt: str = """\
            As a professional applicant tracking system, please provide
            a detailed analysis of this CV. The analysis should include:
            {
            "ats_score": "<float: ATS friendliness score between 0.0 and 1.0>",
            "suggestions": ["<str: Suggestion 1>", "<str: Suggestion 2>", "..."],
            }

            Notes:
            - 'ats_score' should be a float between 0.0 and 1.0, where 1.0 means
            the CV is perfectly ATS-friendly and 0.0 means it's not ATS-friendly at all.
            - 'suggestions' should be a list of suggestions for improving the CV
            to make it more ATS-friendly.
            """
        return self.prompt(prompt)


if __name__ == "__main__":
    ai = AIService(
        file_path=f"{getcwd()}/server/cv/2024-05-13-01-02-49_Abdallah.pdf")
    dict_ = ai.to_dict(CANDID_PROMPT)
    print(dict_)
    # print(ai.get_insights())
    """
    for pdf in listdir('pdf'):
        ai = AIService(pdf=path.join('pdf', pdf))
        dict_ = ai.to_dict(prompts.CANDID_PROMPT)
        print(dict_)
        print('---------->', type(dict_))
        """
