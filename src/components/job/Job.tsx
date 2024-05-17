import { useParams } from 'react-router-dom';
import { useGetJobQuery } from '../../app/services/job';
import { Box, Heading, ListItem, Skeleton, Text, UnorderedList } from '@chakra-ui/react';
import MyIcon from '../Icon';

function Job() {
  const { job_id } = useParams();
  const { data: job = { data: {} }, isSuccess } = useGetJobQuery({ job_id });

  return (
    <Box>
      <Skeleton isLoaded={isSuccess}>
        <Box className='space-y-2'>
          <Heading as='h6' size='md' className='capitalize'>{job.data.job_title}</Heading>
          <Box className='flex gap-2'>
            <Box className='flex gap-1 items-start'>
              <MyIcon href='/sprite.svg#location' className='w-6 h-6 fill-gray-300' />
              <Text className='text-gray-500'>Location</Text>
            </Box>
            <Text>{job.data.location}</Text>
          </Box>
          <Box className='flex gap-2'>
            <Box className='flex items-end gap-1'>
              <MyIcon href='/sprite.svg#money' className='w-6 h-6 fill-gray-300' />
              <Text className='text-gray-500 leading-snug'>salary</Text>
            </Box>
            <Text>{job.data.salary}</Text>
          </Box>
          <Text children={job.data.job_description} />
          <Text className='my-2 capitalize font-semibold'>responsibilities</Text>
          <UnorderedList>
            {job.data.responsibilities?.map((re, idx) =>
              <ListItem key={idx} children={re} />)}
          </UnorderedList>
        </Box>
      </Skeleton>
    </Box>
  );
}

export default Job;
