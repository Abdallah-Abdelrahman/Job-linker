import json

"""Contains the Email templates used in the app"""


def verification_email(name, token):
    """User verfication template"""
    return f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f0f0f0;
            }}
            .container {{
                width: 80%;
                margin: auto;
                background-color: #fff;
                padding: 20px;
                border-radius: 4px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
            .button {{
                display: inline-block;
                color: #fff;
                background-color: #3498db;
                padding: 10px 20px;
                text-decoration: none;
                border-radius: 4px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Dear {name},</h2>
            <p>
                Thank you for registering with Joblinker. We're excited to have you on board.
                To get started, please verify your email address by clicking the button below.
            </p>
            <a href='https://job-linker.netlify.app/verify?token={token}' class="button">Verify Email</a>
            <p>
                If you didn't create an account with Joblinker, you can safely ignore this email.
            </p>
            <p>
                Best regards,<br>
                The Joblinker Team
            </p>
        </div>
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


def shortlisted_candidates_email(recruiter_name, company_name, job_title, candidates):
    """Notify the recruiter about the shortlisted candidates"""
    # Create a string that lists all the shortlisted candidates
    candidates_list = ""
    for name, email, contact_info in candidates:
        contact_info_dict = json.loads(contact_info)
        phone = contact_info_dict.get("phone", "N/A")
        address = contact_info_dict.get("address", "N/A")
        linkedin = contact_info_dict.get("linkedin", "N/A")
        github = contact_info_dict.get("github", "N/A")
        candidates_list += f"<li>Name: {name}, Email: {email}, Phone Number: {phone}, Address: {address}, LinkedIn: {linkedin}, GitHub: {github}</li>"

    return f"""
    <html>
    <body>
    <p>Dear {recruiter_name},</p>

    <p>The job posting for the position of <b>{job_title}</b> at <b>{company_name}</b> has been closed. Here are the candidates that have been shortlisted:</p>

    <ul>
    {candidates_list}
    </ul>

    <p>You may now proceed with scheduling interviews with these candidates.</p>

    <p>Best regards,<br>
    Joblinker Team</p>
    </body>
    </html>
    """


def no_shortlisted_candidates_email(recruiter_name, company_name, job_title):
    """Notify the recruiter that no candidates have been shortlisted"""
    return f"""
    <html>
    <body>
    <p>Dear {recruiter_name},</p>

    <p>The job posting for the position of <b>{job_title}</b> at <b>{company_name}</b> has been closed. Unfortunately, no candidates have been shortlisted for this position.</p>

    <p>We encourage you to post new job openings to attract more candidates.</p>

    <p>Best regards,<br>
    Joblinker Team</p>
    </body>
    </html>
    """
