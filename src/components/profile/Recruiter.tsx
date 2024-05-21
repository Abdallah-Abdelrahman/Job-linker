import {
  Text,
  Heading,
  Box,
  Stack,
  Button,
  useDisclosure,
  SkeletonText,
  Collapse,
  useToast,
} from '@chakra-ui/react';
import React from 'react';
import MyIcon from '../Icon';
import MyModal from '../MyModal';
import { AddJob } from '../job';
import { useState } from 'react';
import * as T from './types';
import { Contact_info } from './Candidate';
import {
  useUploadProfileImageMutation,
  useGetUploadedFileQuery,
} from '../../app/services/auth';
import { Link, Outlet, useMatch } from 'react-router-dom';

function Recruiter({ data }: T.RecruiterProp) {
  const { isOpen, onClose, onOpen } = useDisclosure();
  const [isUploading, setUploading] = useState(false);
  const [isUninitialized, setUnInitialized] = useState(true);
  const match = useMatch('@me/jobs/:job_id');
  const [uploadProfileImage] = useUploadProfileImageMutation();
  const filename = data.image_url?.split('/').pop();
  const toast = useToast();
  const [imageUrl, setImageUrl] = useState<string | undefined>();
  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    uploadProfileImage(formData)
      .unwrap()
      .then((response) => {
        // Handle successful upload
        toast({
          title: 'File uploaded successfully',
          status: 'success',
          duration: 3000,
          isClosable: true,
        });
      })
      .catch((error) => {
        // Handle failed upload
        toast({
          title: 'File upload failed',
          description: error.message,
          status: 'error',
          duration: 3000,
          isClosable: true,
        });
      });
  };

  // Fetch the image file
  const {
    data: imageBlob,
    isLoading,
    error,
  } = useGetUploadedFileQuery({
    file_type: 'images',
    filename: filename,
  });

  // Convert the image Blob to a URL
  React.useEffect(() => {
    if (imageBlob) {
      setImageUrl(URL.createObjectURL(imageBlob));
    } else if (error && error.message === 'File not found') {
      setImageUrl('https://placehold.co/600x400');
    }
  }, [imageBlob, error]);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  //if (error && error.message !== 'File not found') {
  //  return <div>Error: {error.message}</div>;
  //}

  return (
    <Box className='grid grid-cols-4 gap-6 container mt-4 mx-auto sm:grid-cols-12'>
      <Box className='col-span-4 bg-white flex p-6 flex-col items-center gap-2 rounded-md shadow-md sm:col-span-4'>
        <Box className='w-32 h-32 rounded-full overflow-hidden relative'>
          <img
            src={imageUrl || 'https://placehold.co/600x400'}
            className='w-full h-full object-cover'
          />
          <label
            htmlFor='file-upload'
            className='absolute inset-0 w-full h-full flex items-center justify-center opacity-0 cursor-pointer hover:opacity-80 transition duration-500 bg-white bg-opacity-30'
          >
            <svg
              xmlns='http://www.w3.org/2000/svg'
              height='48px'
              viewBox='0 0 24 24'
              width='48px'
              fill='#000000'
            >
              <path d='M0 0h24v24H0V0z' fill='none' />
              <path d='M18 20H4V6h9V4H4c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2v-9h-2v9zm-7.79-3.17l-1.96-2.36L5.5 18h11l-3.54-4.71zM20 4V1h-2v3h-3c.01.01 0 2 0 2h3v2.99c.01.01 2 0 2 0V6h3V4h-3z' />
            </svg>
          </label>

          <input
            id='file-upload'
            type='file'
            onChange={handleFileUpload}
            className='hidden'
          />
        </Box>
        <Heading as='h2' size='lg' className='capitalize'>
          {data.name}
        </Heading>
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
          {match ? (
            <Link
              to='/@me'
              className='!flex !absolute !right-0 !top-0 hover:border-sky-300'
            >
              <MyIcon href='/sprite.svg#back' className='w-6 h-6' />
              <Text as='span'>back</Text>
            </Link>
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
                      className='p-2 ring-1 ring-gray-300  rounded-md'
                    >
                      <Box className='space-y-2'>
                        <Heading as='h6' size='md' className='capitalize'>
                          {job.job_title}
                        </Heading>
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
      <Text>
        {desc.length > 200 ? desc_sub + '...' : desc + '...'}
        <Link className='text-sky-500' to={`jobs/${id}`}>
          see more
        </Link>
      </Text>
    </Box>
  );
}

export default Recruiter;
