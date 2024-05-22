import {
  Box,
  Button,
  Heading,
  Input,
  InputGroup,
  InputLeftElement,
  Menu,
  MenuButton,
  MenuItemOption,
  MenuList,
  MenuOptionGroup,
  Skeleton,
  Text,
  useMediaQuery,
} from '@chakra-ui/react';
import { useGetAllJobsSortedByDateQuery, useLazySearchJobsQuery } from '../app/services/job';
import { MyIcon } from '../components';
import { Link, Outlet, useMatch } from 'react-router-dom';
import { useState } from 'react';
import { formatFromNow } from '../helpers';

function Explore() {
  const match = useMatch('/find_jobs/:job_id');
  const [isLargeThan640] = useMediaQuery('(min-width: 640px)');
  const [sort, setSort] = useState([]);
  const {
    data = { data: [] },
    isLoading: queryLoading,
    isSuccess
  } = useGetAllJobsSortedByDateQuery();
  const [
    searchJobs,
    { data: searchResults = { data: [] },
      isLoading: searchLoading,
      isSuccess: searchSuccess,
      isUninitialized
    }
  ] = useLazySearchJobsQuery();
  const renderedData = isUninitialized ? data.data : searchResults.data;

  const handleSubmit: React.FormEventHandler<HTMLFormElement> = (evt) => {
    evt.preventDefault();
    const formdata = new FormData(evt.currentTarget);
    formdata.append('sort', JSON.stringify(sort));
//    console.log({ form: Object.fromEntries(formdata) });
    searchJobs(Object.fromEntries(formdata));
  };


  return (
    <Box className='container mx-auto mt-4'>
      <Heading as='h1' className='mb-6'>Explore jobs</Heading>
      <form
        className='flex flex-col gap-3 sm:flex-wrap sm:flex-row'
        onSubmit={handleSubmit}
      >
        <Menu closeOnSelect={false}>
          <Box className='flex-shrink-0 basis-[100%] flex-grow'>
            <MenuButton
              ml='auto'
              w='max-content'
              as={Button}
              rightIcon={
                <MyIcon href='/sprite.svg#filter' className='w-6 h-6' />
              }
              children='filters'
            />
          </Box>
          <MenuList>
            <MenuOptionGroup title='Sort' type='checkbox' onChange={setSort}>
              <MenuItemOption value='date'>date</MenuItemOption>
            </MenuOptionGroup>
          </MenuList>
        </Menu>
        <InputGroup
          size='lg'
          className='bg-white sm:basis-[35%]'
          rounded={10}
        >
          <InputLeftElement
            pointerEvents='none'
            children={<MyIcon href='/sprite.svg#search' className='w-6 h-6 fill-gray-500' />}
          />
          <Input
            type='search'
            name='title'
            placeholder='job title, skill or keywords'
            rounded={10}
          />
        </InputGroup>
        <InputGroup
          rounded={10}
          size='lg'
          className='bg-white sm:basis-[35%]'
        >
          <InputLeftElement
            pointerEvents='none'
            children={<MyIcon href='/sprite.svg#location' className='w-6 h-6 fill-gray-500' />}
          />
          <Input
            type='search'
            name='location'
            placeholder='contry, city, state'
            rounded={10}
          />
        </InputGroup>
        <Button
          type='submit'
          size='lg'
          className='!bg-sky-400 !text-white sm:basis-[25%]'
          isLoading={searchLoading}
        >
          search
        </Button>
      </form>
      {/* jobs crumbs */}
      <Box as='section' className='relative mt-8'>
        {!isLargeThan640 && match
          ? <Link
            to='/find_jobs'
            className='!flex !absolute !right-0 !top-0 hover:border-sky-300'
          >
            <MyIcon href='/sprite.svg#back' className='w-6 h-6' />
            <Text as='span'>back</Text>
          </Link>
          : null}
        {isLargeThan640
          ? ( /* desktop view */
            <Box className='grid grid-cols-8 gap-6'>
              <Box as='ul' className='col-span-3 h-full max-h-[800px] overflow-auto grid gap-4'>
                {renderedData.length > 0
                  ? (
                    renderedData.map((job, idx) =>
                      <Box key={idx} as='li' className='h-min p-2 bg-white ring-1 ring-gray-300  rounded-md sm:col-span-3'>
                        <Box className='space-y-2'>
                          <Heading as='h6' size='md' className='capitalize'>{job.job_title}</Heading>
                          <Box className='flex gap-2'>
                            <Box className='flex gap-1 items-start'>
                              <MyIcon href='/sprite.svg#location' className='w-6 h-6 fill-gray-300' />
                              <Text className='text-gray-500'>Location</Text>
                            </Box>
                            <Text>{job.location}</Text>
                          </Box>
                          <Box className='flex gap-2'>
                            <Box className='flex items-end gap-1'>
                              <MyIcon href='/sprite.svg#money' className='w-6 h-6 fill-gray-300' />
                              <Text className='text-gray-500 leading-snug'>salary</Text>
                            </Box>
                            <Text>{job.salary}</Text>
                          </Box>
                          <JobDesc desc={job.job_description} id={job.id} />
                          <Text className='w-max ml-auto text-gray-500'>
                            {formatFromNow(job.created_at)}
                          </Text>
                        </Box>
                      </Box>)
                  )
                  : (
                    <Skeleton size='10' isLoaded={!queryLoading && !searchLoading}>
                      <MyIcon href='/sprite.svg#upload-error' className='w-full h-full' />
                    </Skeleton>
                  )
                }
              </Box>
              <Box className='col-span-5 min-h-96'>
                {match ? <Outlet /> : <MyIcon href='/sprite.svg#join-us' className='w-full h-full' />}
              </Box>
            </Box>
          )
          : (/* mobile view */
            <Box as='ul' className='grid gap-4'>
              {renderedData.length > 0
                ? match
                  ? (
                    <Box as='li'>
                      <Outlet />
                    </Box>
                  )
                  : (
                    renderedData.map((job, idx) =>
                      <Box key={idx} as='li' className='p-2 bg-white ring-1 ring-gray-300  rounded-md sm:col-span-3'>
                        <Box className='space-y-2'>
                          <Heading as='h6' size='md' className='capitalize'>{job.job_title}</Heading>
                          <Box className='flex gap-2'>
                            <Box className='flex gap-1 items-start'>
                              <MyIcon href='/sprite.svg#location' className='w-6 h-6 fill-gray-300' />
                              <Text className='text-gray-500'>Location</Text>
                            </Box>
                            <Text>{job.location}</Text>
                          </Box>
                          <Box className='flex gap-2'>
                            <Box className='flex items-end gap-1'>
                              <MyIcon href='/sprite.svg#money' className='w-6 h-6 fill-gray-300' />
                              <Text className='text-gray-500 leading-snug'>salary</Text>
                            </Box>
                            <Text>{job.salary}</Text>
                          </Box>
                          <JobDesc desc={job.job_description} id={job.id} />
                          <Text className='w-max ml-auto text-gray-500'>
                            {formatFromNow(job.created_at)}
                          </Text>
                        </Box>
                      </Box>)
                  )
                : (
                  <Skeleton size='10' isLoaded={!queryLoading && !searchLoading}>
                    <MyIcon href='/sprite.svg#upload-error' className='' />
                  </Skeleton>
                )
              }
            </Box>
          )
        }
      </Box>
    </Box>
  );
}

type DescProps = {
  desc: string
  id: string
}
function JobDesc({ id, desc }: DescProps) {
  const desc_sub = desc.substring(0, 200);

  return (
    <Box>
      <Text>
        {desc.length > 200
          ? desc_sub + '...'
          : desc + '...'
        }
        <Link className='text-sky-500' to={id}>
          see more
        </Link>
      </Text>
    </Box>
  );
}
export default Explore;
