"""Contains the Email templates used in the app"""


def verification_email(name, token):
    """User verfication template"""
    return f"""
    <html>
    <body>
    Dear {name},<br><br>

    Click the following link to <a href='http://localhost:5173/verify?token={token}'>Verify</a> your email.<br><br>

    Best regards,<br>
    Joblinker Team
    </body>
    </html>
    """


def shortlisted_email(name, company_name, job_title):
    """Notify shortlisted Candidates"""
    return f"""
    Dear {name},

    We are pleased to inform you that your application for the position of {job_title} at {company_name} has been shortlisted. 

    Please prepare for the interview.

    Best regards,
    {company_name} Recruitment Team
    """
