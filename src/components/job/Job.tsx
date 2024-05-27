import { Link, useMatch, useOutletContext, useParams } from 'react-router-dom';
import { useGetJobQuery, useUpdateJobMutation } from '../../app/services/job';
import {
  Box,
  Button,
  Flex,
  Heading,
  Input,
  InputGroup,
  InputLeftAddon,
  List,
  ListItem,
  Skeleton,
  Stack,
  Text,
  Textarea,
  UnorderedList,
  useDisclosure,
  useToast,
} from '@chakra-ui/react';
import MyIcon from '../Icon';
import { useAppSelector } from '../../hooks/store';
import { selectCurrentUser } from '../../features/auth';
import { useCreateApplicationMutation } from '../../app/services/application';
import MyModal from '../MyModal';
import { useEffect, useReducer, useState } from 'react';
import { type Job } from '../profile/types';
import { UpdateOrCancel } from '../profile';

type Context = { setAppliedCandidates?: React.Dispatch<React.SetStateAction<never[]>> }

const init = (data: Job) => {
  return (data);
};

function Job() {
  const { job_id } = useParams();
  const context = useOutletContext<Context>();
  const match = useMatch('/find_jobs/' + job_id);
  const user = useAppSelector(selectCurrentUser);
  const { onClose, isOpen, onOpen } = useDisclosure();
  const {
    data: job = { data: {} },
    isSuccess,

  } = useGetJobQuery({ job_id });
  const [apply, { isLoading, applySuccess, error }] =
    useCreateApplicationMutation();
  const [updateJob, { isLoading: toggleLoading }] = useUpdateJobMutation();
  const toast = useToast();
  const [isEditing, setIsEditing] = useState(false);
  const [textareaH, setTextareaH] = useState(0);
  const [state, dispatch] = useReducer(
    (prevState, newState) => {
      if (newState.type === 'reset') {
        return (job.data);
      }
      if (newState.type === 'init') {
        const { created_at,
          applied_candidates,
          id,
          is_open,
          ...rest
        } = newState.payload;
        return (rest);
      }
      if (newState.type === 'responsibilities') {
        let newResp = [...prevState.responsibilities];
        newResp[newState.payload.index] = newState.payload.value;

        return { ...prevState, responsibilities: newResp };
      }
      return ({ ...prevState, ...newState });
    },
    {
      job_title: job.data.job_title,
      location: job.data.location,
      salary: job.data.salary ?? 0,
      job_description: job.data.job_description,
      application_deadline: job.data.application_deadline,
      responsibilities: job.data.responsibilities
    },
    init
  );
  const handleApply = () => {
    apply({ job_id })
      .unwrap()
      .then(_ => toast({
        title: 'application',
        description: 'your application has been sent successfuly, check your email',
        status: 'success',
        isClosable: true,
        position: 'top',
        variant: 'left-accent'
      }))
      .catch((err) => {
        if (err.status == 401) {
          onOpen();
        }
        else {
          toast({
            title: 'application error',
            description: err.data.message,
            status: 'error',
            isClosable: true,
            position: 'top',
            variant: 'left-accent'
          });
        }
      });
  };
  const handleToggleJob = () => {
    updateJob({
      job_id: job.data.id,
      updates: { is_open: !job.data.is_open },
    });
  };
  const handleUpdate = () => {
    updateJob({
      job_id: job.data.id,
      updates: {
        ...state,
        application_deadline: new Date(state.application_deadline)
      }
    })
      .unwrap()
      .then()
      .catch(err => console.log({ err }))
      .finally(() => {
        setIsEditing(false);
      });
  };

  // effect to update the state when promise resloved
  useEffect(() => {
    if (isSuccess && job.data.job_title && !state.job_title) {
      dispatch({ type: 'init', payload: job.data });
      if (typeof context?.setAppliedCandidates == 'function') {
        context.setAppliedCandidates(job.data.applied_candidates);
      }
    }
  }, [context, isSuccess, job.data, state.job_title]);

  return (
    <Box className='relative p-1'>
      <Skeleton isLoaded={isSuccess}>
        <Box className='space-y-2'>
          {!match
            && (
              <Button
                onClick={() => setIsEditing(true)}
                className='!absolute !p-0 !m-0 top-0 right-0'
              >
                <MyIcon href='/sprite.svg#edit' className='w-5 h-5' />
              </Button>
            )}
          {isEditing
            ? (/* editing jsx */
              <Stack className='!mt-12'>
                <InputGroup>
                  <Input value={state.job_title} onChange={(e) => dispatch({ job_title: e.target.value })} />
                </InputGroup>
                <InputGroup>
                  <InputLeftAddon children='location' />
                  <Input value={state.location} onChange={(e) => dispatch({ location: e.target.value })} />
                </InputGroup>
                <InputGroup>
                  <InputLeftAddon children='salary' />
                  <Input
                    type='number'
                    min='0'
                    value={state.salary}
                    onChange={(e) => dispatch({ salary: e.target.value })}
                  />
                </InputGroup>
                <Textarea
                  ref={(el) => {
                    if (!el) return;
                    if (!textareaH) {
                      setTextareaH(el.scrollHeight);
                    }
                  }}
                  value={state.job_description}
                  onChange={(e) => {
                    dispatch({ job_description: e.target.value });
                    e.target.style.height = 'iherit';
                    e.target.style.height = `${e.target.scrollHeight}px`;
                  }}
                  resize='vertical'
                  h={textareaH + 'px'}
                />
                <List>
                  {state.responsibilities?.map((r, idx) =>
                    <ListItem key={idx}>
                      responsibility {idx + 1}
                      <InputGroup>
                        <Input
                          value={state.responsibilities[idx]}
                          onChange={(e) => dispatch({
                            type: 'responsibilities',
                            payload: { value: e.target.value, index: idx }
                          })}
                        />
                      </InputGroup>
                    </ListItem>
                  )}
                </List>
                <InputGroup>
                  <InputLeftAddon children='deadline' />
                  <Input
                    type='datetime-local'
                    value={new Date(state.application_deadline).toISOString().slice(0, 16)}
                    onChange={(e) => dispatch({ application_deadline: e.target.value })} />
                </InputGroup>
                <UpdateOrCancel
                  isLoading={isLoading}
                  update={handleUpdate}
                  cancel={() => {
                    setIsEditing(false);
                    dispatch({ type: 'reset' });
                  }}
                />
              </Stack>
            )
            : (/* normal jsx */
              <>
                <Heading as='h6' size='md' className='capitalize max-w-[85%]'>
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
                <Box>
                  <Flex alignItems='center' gap='1' mb='1'>
                    <MyIcon href='/sprite.svg#deadline' className='w-6 h-6' />
                    <Text
                      className='capitalize font-semibold leading-none'
                      children='deadline'
                    />
                  </Flex>
                  <Text
                    className=''
                    children={job.data.application_deadline}
                  />
                </Box>
              </>
            )
          }
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
        {user.role === 'recruiter' && !match && (
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
