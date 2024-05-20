import { Box, Button, Heading, Input, InputGroup, InputLeftElement, ListItem, Menu, MenuButton, MenuItem, MenuItemOption, MenuList, MenuOptionGroup, Text, Skeleton, UnorderedList } from "@chakra-ui/react";
import { useGetAllJobsSortedByDateQuery } from "../app/services/job";
import { MyIcon } from "../components";
import { Link, Outlet, useMatch } from "react-router-dom";

function Explore() {
  const { data = { data: [] }, isSuccess } = useGetAllJobsSortedByDateQuery();
  const match = useMatch('/find_jobs/:job_id');

  console.log({ match });


  const handleSubmit: React.FormEventHandler<HTMLFormElement> = (evt) => {
    evt.preventDefault();
    const formdata = new FormData(evt.currentTarget);
    console.log({ form: Object.fromEntries(formdata) });
  }

  console.log({ data });

  return (
    <Box className='container mx-auto'>
      <Heading as='h1' className='mb-4'>Explore jobs</Heading>
      <form
        className='flex flex-col gap-3'
        onSubmit={handleSubmit}
      >
        <Menu closeOnSelect={false}>
          <MenuButton
            ml='auto'
            w='max-content'
            as={Button}
            rightIcon={<MyIcon href='/sprite.svg#filter' className='w-6 h-6' />}
          >
            filters
          </MenuButton>
          <MenuList>
            <MenuOptionGroup title='Sort' type='checkbox' onChange={(val)=>console.log({val})}>
              <MenuItemOption value='date'>date</MenuItemOption>
              <MenuItemOption value='name'>name</MenuItemOption>
            </MenuOptionGroup>
          </MenuList>
        </Menu>
        <InputGroup
          size='lg'
          className='bg-white'
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
          className='bg-white'
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
          className='!bg-sky-400 !text-white'
        >
          search
        </Button>
      </form>
      {/* jobs crumbs */}
      <Box as='section' className='relative mt-8'>
        {match
          ? <Link
            to='/find_jobs'
            className='!flex !absolute !right-0 !top-0 hover:border-sky-300'
          >
            <MyIcon href='/sprite.svg#back' className='w-6 h-6' />
            <Text as='span'>back</Text>
          </Link>
          : null}
        <Box as='ul' className='flex flex-col gap-4'>
          {data.data.length > 0
            ? match
              ? <Box>
                <Outlet />
              </Box>
              : data.data.map((job, idx) =>
                <Box key={idx} as='li' className='p-2 bg-white ring-1 ring-gray-300  rounded-md'>
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
                  </Box>
                </Box>
              )
            : null}
        </Box>
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
