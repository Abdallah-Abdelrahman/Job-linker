import { Link, useParams } from 'react-router-dom';
import { useGetJobQuery, useUpdateJobMutation } from '../../app/services/job';
import {
  Box,
  Button,
  Heading,
  ListItem,
  Skeleton,
  Text,
  UnorderedList,
  useDisclosure,
} from '@chakra-ui/react';
import { useState } from 'react';
import MyIcon from '../Icon';
import { useAppSelector } from '../../hooks/store';
import { selectCurrentUser } from '../../features/auth';
import { useCreateApplicationMutation } from '../../app/services/application';
import MyModal from '../MyModal';

function Job() {
  const { job_id } = useParams();
  const user = useAppSelector(selectCurrentUser);
  const { onClose, isOpen, onOpen } = useDisclosure();
  const {
    data: job = { data: {} },
    isSuccess,

  } = useGetJobQuery({ job_id });
  const [apply, { isLoading, applySuccess, error }] =
    useCreateApplicationMutation();
  const [updateJob, { isLoading: toggleLoading }] = useUpdateJobMutation();

  const handleApply = () => {
    apply({ job_id })
      .unwrap()
      .catch((err) => {
        if (err.status == 401) {
          onOpen();
        }
      });
  };

  const handleToggleJob = () => {
    updateJob({
      job_id: job.data.id,
      updates: { is_open: !job.data.is_open },
    });
  };

  return (
    <Box>
      <Skeleton isLoaded={isSuccess}>
        <Box className='space-y-2'>
          <Heading as='h6' size='md' className='capitalize'>
            {job.data.job_title}
          </Heading>
          <Box className='flex gap-2'>
            <Box className='flex gap-1 items-start'>
              <MyIcon
                href='/sprite.svg#location'
                className='w-6 h-6 fill-gray-300'
              />
              <Text className='text-gray-500'>Location</Text>
            </Box>
            <Text>{job.data.location}</Text>
          </Box>
          <Box className='flex gap-2'>
            <Box className='flex items-end gap-1'>
              <MyIcon
                href='/sprite.svg#money'
                className='w-6 h-6 fill-gray-300'
              />
              <Text className='text-gray-500 leading-snug'>salary</Text>
            </Box>
            <Text>{job.data.salary}</Text>
          </Box>
          <Text children={job.data.job_description} />
          <Text className='my-2 capitalize font-semibold'>
            responsibilities
          </Text>
          <UnorderedList>
            {job.data.responsibilities?.map((re, idx) => (
              <ListItem key={idx} children={re} />
            ))}
          </UnorderedList>
        </Box>
        <MyModal
          title='error'
          isOpen={isOpen}
          body={
            <Text>
              you need to{' '}
              <Link className='text-sky-400' to='/login' children='sign in' />{' '}
              as candidate to be able to apply
            </Text>
          }
          onClose={onClose}
          confirm={<></>}
        />
        {user.role === 'recruiter' && (
          <Button
            className='mt-4'
            onClick={handleToggleJob}
            isLoading={toggleLoading}
          >
            {job.data.is_open ? 'Close Job' : 'Open Job'}
          </Button>
        )}
        {user.role != 'recruiter' ? (
          <Button
            isLoading={isLoading}
            size='lg'
            className='mt-4 !bg-white border border-sky-400'
            children='apply'
            onClick={handleApply}
          />
        ) : null}
      </Skeleton>
    </Box>
  );
}

export default Job;
