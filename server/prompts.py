'''Module defines prompts to feed it to gemini'''

CANDID_PROMPT = '''\
        gimme a dictionary from this cv in the form of:
    {
      name,
      email,
      major,
      skills:[],
      experiences:[
        {title,company,star_date, end_date,location,descpription:''}
      ],
      languages:[]
    }
    don't forget to enclose each property in double quotes
    '''

JOB_PROMPT = ''' '''
