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
    <html>
    <body>
    <p>Dear {name},</p>

    <p>Congratulations! Your application for the position of <b>{job_title}</b> at <b>{company_name}</b> has been shortlisted.</p>

    <p>We were impressed with your skills and experiences and believe you could be a strong candidate for this role. The next step in our hiring process is the interview round. We will send you further details soon.</p>

    <p>Thank you for considering {company_name} as a potential employer. We look forward to the possibility of working together.</p>

    <p>Best regards,<br>
    {company_name} Recruitment Team</p>
    </body>
    </html>
    """
