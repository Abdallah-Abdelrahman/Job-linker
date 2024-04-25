'''Module defines prompts to feed it to gemini'''

CANDID_PROMPT = '''\
        give me a dictionary from this cv in the form of:
    {
      name,
      email,
      major,
      skills:[],
      experiences:[
        {title,company,start_date,end_date,location,descpription:''}
      ],
      languages:[]
    }
    Notes:
    - don't forget to enclose each property in double quotes
    - start_date, end_date should respects this format '%Y-%m-%dT%H:%M:%S.%f'
    '''

JOB_PROMPT = '''\
    give me a dictionary from this job in the form of:
    {
      title,
      major,
      years_of_experience,
      responsibilites:[],
      skills:[],
      location,
      job_desc:''
    }
    Notes:
    - don't forget to enclose each property in double quotes
'''