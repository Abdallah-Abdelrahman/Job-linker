import { Text, Heading, Box, Stack, Button, Collapse, useDisclosure } from '@chakra-ui/react';
import MyIcon from '../Icon';
import MyModal from '../MyModal';
import { AddJob } from '../job';

type Job = {
  id: string;
  application_deadline: Date | null;
  exper_years: string;
  is_open: boolean;
  job_description: string;
  job_title: string;
  location: string;
  major: string;
  salary: number;
  skills: string[];
}

type Recruiter = {
  jobs: Job[];
}

type ContactInfo = {
  company_address: string;
  company_email: string;
  company_name: string;
}

type Data = {
  bio: string | null;
  contact_info: ContactInfo;
  email: string;
  image_url: string | null;
  name: string;
  recruiter: Recruiter;
}

interface RecruiterProp {
  data: Data;
}

function Recruiter({ data }: RecruiterProp) {
  const { isOpen, onClose, onOpen } = useDisclosure();

  return (
    <Box className='grid grid-cols-4 gap-6 container mt-4 mx-auto sm:grid-cols-12'>
      <Box className='col-span-4 bg-white flex p-6 flex-col items-center gap-2 rounded-md shadow-md sm:col-span-4'>
        <Box className='w-32 h-32  rounded-full overflow-hidden'>
          <img src={data.image_url || 'https://placehold.co/600x400'} className='w-full h-full object-cover' />
        </Box>
        <Heading as='h2' size='lg' className='capitalize'>{data.name}</Heading>
        <Text className='tracking-wide'>{data.contact_info.company_name}</Text>
        <hr className='w-full' />
        <Stack className='w-full mt-2 space-y-6'>
          <Contact_info data={data.contact_info} />
        </Stack>
      </Box>

      <Box className='col-span-4 bg-white flex flex-col rounded-md shadow-md p-6 gap-4 sm:col-span-8'>
        {/*Jobs*/}
        <Box className='relative'>
          <Heading as='h4' mb='4' size='lg' className='capitalize'>
            Jobs
          </Heading>
          <Button
            className='!absolute !right-0 !top-0 hover:border-sky-300'
            onClick={onOpen}
          >
            {/* job modal */}
            <MyModal
              title='add new job'
              isOpen={isOpen}
              onClose={onClose}
              body={<AddJob />}
              confirm={<Button type='submit' form='job'>add</Button>}
            />
            <MyIcon href='/sprite.svg#plus' className='w-6 h-6' />
          </Button>

          {data.recruiter.jobs.length > 0
            ? <Box as='ul' className='flex flex-col gap-4'>
              {data.recruiter.jobs.map((job, idx) =>
                <Box key={idx} as='li'>
                  <Box className='flex justify-between flex-wrap gap-3 w-full'>
                    <Heading as='h6' size='md' className='capitalize'>{job.job_title}</Heading>
                    <Box>
                      <span className='mr-2'>Location: {job.location}</span>
                      <span className='span-gray-500'>
                        Salary: {job.salary}
                      </span>
                    </Box>
                  </Box>
                  <Text className='mt-2'>{job.job_description}</Text>
                </Box>)}
            </Box>
            : <>
              <Text>you haven't created any job yet, hit the plus sign to add new one</Text>
            </>}

        </Box>
      </Box>
    </Box>
  );
}

function Contact_info({ data }: { data: ContactInfo }) {
  if (!data) {
    return (null);
  }

  return (
    <Box as='section' className='flex flex-col gap-4'>
      <Heading as='h4' mb='2' size='lg' className='capitalize'>contact info</Heading>
      {Object.entries(data).map(([k, v]) => {
        if (!v) return (null);
        return (<Box key={k} className='flex gap-3'>
          <MyIcon href={`/sprite.svg#${k}`} className='w-5 h-5' />
          {k == 'linkedin' || k == 'github'
            ? <a href={v} target='_blank' className='text-sky-500'>{k}</a>
            : <Text>{v}</Text>}
        </Box>
        );
      }
      )}
    </Box>
  );
}

export default Recruiter;
