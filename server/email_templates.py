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


def application_submission_email(name, company_name, job_title):
    """Notify Candidates about successful application submission"""
    return f"""
    <html>
    <body>
    <p>Dear {name},</p>

    <p>Thank you for applying for the position of <b>{job_title}</b> at <b>{company_name}</b>.</p>

    <p>Your application is under review. We will notify you about the status of your application soon.</p>

    <p>Best regards,<br>
    {company_name} Recruitment Team</p>
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


def rejection_email(name, company_name, job_title):
    """Notify Candidates who were not selected"""
    return f"""
    <html>
    <body>
    <p>Dear {name},</p>

    <p>Thank you for your interest in the <b>{job_title}</b> position at <b>{company_name}</b> and for the time you've invested in the application process.</p>

    <p>We wanted to inform you that after careful consideration, we have decided to move forward with another candidate for this position. This decision was not an easy one and it was based on the specific needs of the role.</p>

    <p>We appreciate your interest in {company_name} and encourage you to apply for future openings that align with your skills and interests.</p>

    <p>Thank you again for your application. We wish you all the best in your job search and future professional endeavors.</p>

    <p>Best regards,<br>
    {company_name} Recruitment Team</p>
    </body>
    </html>
    """
