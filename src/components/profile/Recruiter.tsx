import {
  Text,
  Heading,
  Box,
  Stack,
  Button,
  useDisclosure,
  SkeletonText,
  useToast,
  Badge,
  Input,
  SkeletonCircle,
  ButtonGroup,
  InputGroup,
  InputLeftAddon,
} from '@chakra-ui/react';
import React, { Reducer, useReducer } from 'react';
import MyIcon from '../Icon';
import MyModal from '../MyModal';
import { AddJob } from '../job';
import { useState } from 'react';
import * as T from './types';
import {
  useUploadProfileImageMutation,
  useGetUploadedFileQuery,
  useUpdateMeMutation,
} from '../../app/services/auth';
import { Link, Outlet, useMatch, useNavigate } from 'react-router-dom';
import UpdateOrCancel from './UpdateOrCancel';
import Photo from './Photo';

type RecReducer = Reducer<
  T.RecruiterProp['data']['contact_info'] & { user_name: string },
  T.RecruiterProp['data']['contact_info'] & { user_name: string }
>;

function Recruiter({ data }: T.RecruiterProp) {
  const { isOpen, onClose, onOpen } = useDisclosure();
  const [isUploading, setUploading] = useState(false);
  const [isUninitialized, setUnInitialized] = useState(true);
  const match = useMatch('@me/jobs/:job_id');
  const [uploadProfileImage, { isLoading: isLoading_MUPLOAD }] = useUploadProfileImageMutation();
  const navigate = useNavigate();
  const [updateMe, { isLoading }] = useUpdateMeMutation();
  const [isEditing, setIsEditing] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [state, dispatch] = useReducer<RecReducer>(
    (prevState, newState) => {
      if (newState.type === 'reset') {
        const { contact_info, name } = data;
        return ({ ...contact_info, user_name: name });
      }
      return { ...prevState, ...newState };
    },
    {
      company_name: data.contact_info.company_name ?? '',
      company_address: data.contact_info.company_address ?? '',
      company_email: data.contact_info.company_email ?? '',
      user_name: data.name ?? '',
    },
  );

  // handlers
  const handleApplyClick = () => {
    // Call the API to update the field
    const formdata = new FormData();
    formdata.append('file', file);
    const { user_name: name, ...contact_info } = state;
    Promise.allSettled([
      updateMe({ contact_info, name }).unwrap(),
      uploadProfileImage(formdata).unwrap()
    ])
      .catch(err => console.log({ err }))
      .finally(() => {
        setIsEditing(false);
      });
  };

  const FileLinks = ({ user_files }) => {
    const fileLinks = user_files
      .map((file) => {
        const { filename, original_filename } = file;
        const { data: file_data, error } = useGetUploadedFileQuery({
          file_type: 'jobs',
          filename: filename.split('/').pop(),
        });

        if (error) {
          return null;
        }

        const fileUrl = file_data?.data?.url;
        if (!fileUrl) {
          return null;
        }

        return (
          <li key={file.id}>
            <a href={fileUrl} target='_blank' rel='noopener noreferrer'>
              {original_filename}
            </a>
          </li>
        );
      })
      .filter(Boolean);

    return (
      <Box className='w-full mt-6'>
        <Heading as='h3' size='md' mb={2}>
          My Files
        </Heading>
        <ul className='list-disc list-inside'>
          {fileLinks.length > 0 ? fileLinks : <Text>No files available</Text>}
        </ul>
      </Box>
    );
  };

  return (
    <Box className='grid grid-cols-4 gap-6 container mt-4 mx-auto sm:grid-cols-12'>
      <Box className='relative col-span-4 bg-white flex p-6 flex-col items-center gap-2 rounded-md shadow-md sm:col-span-4'>
        <Button
          className='!absolute top-6 right-6'
          onClick={() => setIsEditing(true)}
        >
          <MyIcon href='/sprite.svg#edit' className='w-6 h-6' />
        </Button>
        <Photo
          isLoading={isLoading_MUPLOAD}
          setFile={setFile}
          disabled={!isEditing}
          imageUrl={data.image_url}
        />
        {isEditing ? (
          <InputGroup>
            <InputLeftAddon children='user_name' />
            <Input
              value={state.user_name}
              onChange={(e) => dispatch({ user_name: e.target.value })}
            />
          </InputGroup>
        ) : (
          <Heading as='h2' size='lg' className='capitalize'>
            {data.name}
          </Heading>
        )}
        <hr className='w-full' />
        <Stack className='w-full mt-2 space-y-6'>
          {isEditing ? (
          <InputGroup>
            <InputLeftAddon children='company' />
            <Input
              value={state.company_name}
              onChange={(e) => dispatch({ company_name: e.target.value })}
            />
          </InputGroup>
          ) : (
            <Text>{data.contact_info.company_name}</Text>
          )}
          {isEditing ? (
          <InputGroup>
            <InputLeftAddon children='address' />
            <Input
              value={state.company_address}
              onChange={(e) => dispatch({ company_address: e.target.value })}
            />
          </InputGroup>
          ) : (
            <Text>{data.contact_info.company_address}</Text>
          )}
          {isEditing ? (
          <InputGroup>
            <InputLeftAddon children='email' />
            <Input
              value={state.company_email}
              onChange={(e) => dispatch({ company_email: e.target.value })}
            />
          </InputGroup>
          ) : (
            <Text>{data.contact_info.company_email}</Text>
          )}
          {isEditing && (
            <UpdateOrCancel
              isLoading={isLoading}
              update={handleApplyClick}
              cancel={() => {
                setIsEditing(false);
                dispatch({ type: 'reset' });
              }}
            />
          )}
        </Stack>
        {/* User files */}
        {/*<FileLinks user_files={data.user_files} />*/}
      </Box>

      {/*Jobs*/}
      <Box className='col-span-4 bg-white flex flex-col rounded-md shadow-md p-6 gap-4 sm:col-span-8'>
        <Box className='relative'>
          <Heading as='h4' mb='4' size='lg' className='capitalize'>
            Jobs
          </Heading>
          {match ? (
            <Button
              className='!flex !absolute !right-0 !top-0 hover:border-sky-300'
              onClick={() => navigate('/@me')}
            >
              <MyIcon href='/sprite.svg#back' className='w-6 h-6' />
              <Text as='span'>back</Text>
            </Button>
          ) : (
            <Button
              className='!absolute !right-0 !top-0 hover:border-sky-300'
              onClick={onOpen}
            >
              {/* job modal */}
              <MyModal
                title='add new job'
                isOpen={isOpen}
                onClose={() => {
                  onClose();
                  setUnInitialized(true);
                  setUploading(false);
                }}
                body={
                  isUninitialized ? (
                    <AddJob
                      setLoading={setUploading}
                      setUnInitialized={setUnInitialized}
                    />
                  ) : (
                    <SkeletonText isLoaded={!isUploading}>
                      <Text className='text-teal-500'>
                        your file has been parsed successfully
                      </Text>
                    </SkeletonText>
                  )
                }
                confirm={
                  <Button
                    isLoading={isUploading}
                    type='submit'
                    form='job'
                    disabled={isUploading}
                    className='!bg-sky-400 !text-white'
                  >
                    add
                  </Button>
                }
              />
              <MyIcon href='/sprite.svg#plus' className='w-6 h-6' />
            </Button>
          )}

          {data.recruiter.jobs.length > 0 ? (
            <Box as='ul' className='flex flex-col gap-4'>
              {match ? (
                <Box as='li'>
                  <Outlet />
                </Box>
              ) : (
                data.recruiter.jobs.map((job, idx) => {
                  return (
                    <Box
                      key={idx}
                      as='li'
                      className='p-2 ring-1 ring-gray-300 rounded-md relative'
                    >
                      <Badge
                        position='absolute'
                        top='2'
                        right='2'
                        colorScheme='fill-gray-300'
                        variant='outline'
                      >
                        {job.application_count} Applications
                      </Badge>
                      <Box className='relative space-y-2'>
                        <Heading as='h6' size='md' className='capitalize max-w-[80%]'>
                          {job.job_title}
                        </Heading>
                        <Text
                          className={`py-1 px-2 absolute top-4 right-0 rounded-md
                            ${job.is_open
                              ? 'bg-teal-100 text-teal-700'
                              : 'bg-purple-100 text-purple-700'
                            }`}
                        >
                          {job.is_open ? 'open' : 'closed'}
                        </Text>
                        <Box className='flex gap-2'>
                          <Box className='flex gap-1 items-start'>
                            <MyIcon
                              href='/sprite.svg#location'
                              className='w-6 h-6 fill-gray-300'
                            />
                            <Text className='text-gray-500'>Location</Text>
                          </Box>
                          <Text>{job.location}</Text>
                        </Box>
                        <Box className='flex gap-2'>
                          <Box className='flex items-end gap-1'>
                            <MyIcon
                              href='/sprite.svg#money'
                              className='w-6 h-6 fill-gray-300'
                            />
                            <Text className='text-gray-500 leading-snug'>
                              salary
                            </Text>
                          </Box>
                          <Text>{job.salary}</Text>
                        </Box>
                        <JobDesc desc={job.job_description} id={job.id} />
                      </Box>
                    </Box>
                  );
                })
              )}
            </Box>
          ) : (
            <>
              <Text color='gray.500'>
                you haven't created any job yet, hit the plus sign to add new
                one
              </Text>
            </>
          )}
        </Box>
      </Box>
    </Box>
  );
}

type DescProps = {
  desc: string;
  id: string;
};
function JobDesc({ id, desc }: DescProps) {
  const desc_sub = desc.substring(0, 200);

  return (
    <Box>
      <Text className='p-1'>
        {desc.length > 200 ? desc_sub + '...' : desc + '...'}
        <Link className='text-sky-500' to={`jobs/${id}`}>
          see more
        </Link>
      </Text>
    </Box>
  );
}

export default Recruiter;
