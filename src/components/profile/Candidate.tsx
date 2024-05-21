import { Text, Heading, Box, Stack } from '@chakra-ui/react';
import MyIcon from '../Icon';
import * as T from './types';


function Candidate({ data }: T.CandidateProp) {
  return (
    <Box className='grid grid-cols-4 gap-6 container mt-4 mx-auto sm:grid-cols-12'>
      <Box className='col-span-4 bg-white flex p-6 flex-col items-center gap-2 rounded-md shadow-md sm:col-span-4'>
        <Box className='w-32 h-32  rounded-full overflow-hidden'>
          <img src='https://placehold.co/600x400' className='w-full h-full object-cover' />
        </Box>
        <Heading as='h2' size='lg' className='capitalize'>{data.name}</Heading>
        <Text className='tracking-wide'>{data.candidate.major.name}</Text>
        <hr className='w-full' />

        <Stack className='w-full mt-2 space-y-6'>
          <Contact_info data={data.contact_info} />
          <Box as='section' className='flex flex-col gap-4'>
            {/*Skills*/}
            <Heading as='h4' mb='2' size='lg' className='capitalize'>skills</Heading>
            <ul className='flex flex-wrap gap-4 max-h-64 overflow-auto'>
              {data.candidate.skills.map((skill, idx) =>
                <li key={idx} className='p-2 bg-teal-50 text-teal-500 rounded-tl-lg rounded-br-lg'>{skill.name}</li>
              )}
            </ul>
          </Box>
          <Box as='section' className='flex flex-col gap-4'>
            {/*Languages*/}
            <Heading as='h4' mb='2' size='lg' className='capitalize'>languages</Heading>
            <Box as='ul' className='flex flex-wrap gap-4 max-h-40 overflow-auto'>
              {data.candidate.languages.map((l, idx) =>
                <Box
                  key={idx}
                  as='li'
                  className='p-2 bg-orange-50 text-orange-500 rounded-tl-lg rounded-br-lg'
                >
                  {l.name}
                </Box>)}
            </Box>
          </Box>
        </Stack>
      </Box>

      <Box className='col-span-4 bg-white flex flex-col rounded-md shadow-md p-6 gap-4 sm:col-span-8'>
        {/*About*/}
        <Box>
          <Heading as='h4' mb='2' size='lg' className='capitalize'>
            About me
          </Heading>
          <Text>
            {data.bio}
          </Text>
        </Box>
        {/*Experience*/}
        <Box>
          <Heading as='h4' mb='4' size='lg' className='capitalize'>
            experience
          </Heading>
          <Box as='ul' className='flex flex-col gap-4'>
            {data.candidate.experiences.map((xp, idx) =>
              <Box key={idx} as='li'>
                <Box className='flex flex-col gap-3 w-full'>
                  <Heading as='h6' size='md' className='capitalize'>{xp.title.toLowerCase()}</Heading>
                  <Box className='space-y-2'>
                    <Box className='flex gap-2'>
                      <Box className='flex gap-1'>
                        <MyIcon href='/sprite.svg#company' className='w-5 h-5 fill-gray-500' />
                        <Text className='text-gray-500' children='at' />
                      </Box>
                      <Text className='capitalize font-semibold' children={xp.company.toLowerCase()} />
                    </Box>
                    <Box className='flex gap-2'>
                      <Box className='flex gap-1 text-gray-500'>
                        <MyIcon href='/sprite.svg#date' className='w-5 h-5 fill-gray-500' />
                        <Text children='date' />
                      </Box>
                      <Text
                        className='font-semibold'
                        children={`${formateDate(xp.start_date)} - ${formateDate(xp.end_date)}`}
                      />
                    </Box>
                  </Box>
                </Box>
                <Text className='mt-2'>{xp.description}</Text>
              </Box>

            )}
          </Box>
        </Box>
        {/*Education*/}
        <Box>
          <Heading as='h4' mb='4' size='lg' className='capitalize'>
            education
          </Heading>
          <Box as='ul' className='flex flex-col gap-4'>
            {data.candidate.education.map((ed, idx) => (
              <Box key={idx} as='li'>
                <Box className='flex flex-col gap-3 w-full'>
                  <Box className='flex gap-2'>
                    <Box className='flex gap-1'>
                      <MyIcon
                        href='/sprite.svg#field_of_study'
                        className='w-5 h-5 fill-gray-500'
                      />
                      <Text className='text-gray-500'>field</Text>
                    </Box>
                    <Text className='font-semibold'>{ed.field_of_study}</Text>
                  </Box>
                  <Box className='flex gap-2'>
                    <Box className='flex gap-1'>
                      <MyIcon
                        href='/sprite.svg#degree'
                        className='w-5 h-5 fill-gray-500'
                      />
                      <Text className='text-gray-500'>degree</Text>
                    </Box>
                    <Text className='font-semibold'>{ed.degree}</Text>
                  </Box>
                  <Box className='flex gap-2'>
                    <Box className='flex gap-1'>
                      <MyIcon
                        href='/sprite.svg#date'
                        className='w-5 h-5 fill-gray-500'
                      />
                      <Text className='text-gray-500'>date</Text>
                    </Box>
                    <Text className='font-semibold'>
                      {formateDate(ed.start_date)} - {formateDate(ed.end_date)}
                    </Text>
                  </Box>
                </Box>
              </Box>
            ))}
          </Box>
        </Box>
      </Box>
    </Box>
  );

}

export function Contact_info({ data }: { data: Contact }) {
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

/**
 * utility to format date
 * @param {Date} date - date object
 * @returns string format in `Month year`
 */
function formateDate(date: Date) {
  return new Date(date).toLocaleDateString('en', { year: 'numeric', month: 'short' });
}

export default Candidate;
