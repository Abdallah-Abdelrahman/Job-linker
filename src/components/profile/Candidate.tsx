import { Text, Heading, Box } from '@chakra-ui/react';
type Experience = {}
type Application = {
  title: string,
  company: string,
  start_date: Date,
  end_date: Date,
  description: string
}
type Data = {
  name: string,
  email: string,
  image_url: string,
  bio: string,
  candidate: {
    major: { name: string },
    skills: string[],
    applications: Application[],
    experiences: Experience[]
  },
}
interface CandidateProp {
  data: Data
}

function Candidate({ data }: CandidateProp) {
  return (
    <Box className='grid grid-cols-4 gap-6 container mt-4 mx-auto sm:grid-cols-12'>
      <div className='col-span-4 bg-white flex p-6 flex-col items-center gap-2 rounded-md shadow-md sm:col-span-4'>
        <div className='w-32 h-32 rounded-full overflow-hidden'>
          <img src='https://placehold.co/600x400' className='w-full h-full object-cover' />
        </div>
        <Heading as='h2' size='lg' className='capitalize'>{data.name}</Heading>
        <Text className='tracking-wide'>{data.candidate.major.name}</Text>
        <hr className='w-full' />

        <div className='w-full mt-2'>
          {/*Skills*/}
          <Heading as='h4' mb='2' size='lg' className='capitalize'>skills</Heading>
          <ul className='flex flex-wrap gap-4 max-h-40 overflow-auto'>
            {['baslfk', 'asldfkj', 'asldkfjasdlfkj', 'asldkfjasdlfkj', 'asldkfjasdlfkj', 'asldkfjasdlfkj', 'asldkfjasdlfkj', 'asldkfjasdlfkj', 'asldkfjasdlfkj', 'asldkfjasdlfkj', 'asldkfjasdlfkj', 'asldkfjasdlfkj', 'asldkfjasdlfkj']
              .map((skill, idx) => <li key={idx} className='p-2 bg-teal-50 text-teal-500 rounded-tl-lg rounded-br-lg'>{skill}</li>)}
          </ul>
        </div>
        <div className='w-full mt-2'>
          {/*Languages*/}
          <Heading as='h4' mb='2' size='lg' className='capitalize'>languages</Heading>
          <Box as='ul' className='flex flex-wrap gap-4 max-h-40 overflow-auto'>
            {['english', 'Rusia'].map((l, idx) =>
              <Box
                key={idx}
                as='li'
                className='p-2 bg-orange-50 text-orange-500 rounded-tl-lg rounded-br-lg'
              >
                {l}
              </Box>)}
          </Box>
        </div>
      </div>

      <div className='col-span-4 bg-white flex flex-col rounded-md shadow-md p-6 gap-4 sm:col-span-8'>
        {/*About*/}
        <div>
          <Heading as='h4' mb='2' size='lg' className='capitalize'>
            About me
          </Heading>
          <Text>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed finibus est vitae tortor ullamcorper, ut vestibulum velit convallis. Aenean posuere risus non velit egestas suscipit. Nunc finibus vel ante id euismod. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Aliquam erat volutpat. Nulla vulputate pharetra tellus, in luctus risus rhoncus id.
          </Text>
        </div>
        {/*Experience*/}
        <Box>
          <Heading as='h4' mb='4' size='lg' className='capitalize'>
            experience
          </Heading>
          <Box as='ul' className='flex flex-col gap-4'>
            {Array.from({ length: 3 }).map((xp, idx) =>
              <Box key={idx} as='li'>
                <Box className='flex justify-between flex-wrap gap-3 w-full'>
                  <Heading as='h6' size='md' className='capitalize'>web developer</Heading>
                  <Box>
                    <span className='mr-2'>at company name</span>
                    <span className='span-gray-500'>2017 - 2019</span>
                  </Box>
                </Box>
                <Text className='mt-2'>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed finibus est vitae tortor ullamcorper, ut vestibulum velit convallis. Aenean posuere risus non velit egestas suscipit.
                </Text>
              </Box>

            )}
          </Box>
        </Box>
      </div>
    </Box>
  );

}

export default Candidate;
