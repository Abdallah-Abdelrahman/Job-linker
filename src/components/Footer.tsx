import { Text, Box, Heading } from '@chakra-ui/react';
import MyIcon from './Icon';

const CONTACTS = [
  { icon: 'phone', details: '+1-123-456-7890' },
  { icon: 'email', details: 'support@joblinker.com' },
  { icon: 'location', details: 'Sillicon Valley' },
];

function Footer() {
  return (
    <footer className='footer container mx-auto flex justify-around gap-8 flex-col py-8 mt-auto bg-white md:flex-row'>
      {/* Contanct */}
      <Box
        as='section'
        className='basis-1/2 mt-14 border-b pb-8 -mb-8 sm:mb-0 sm:border-b-0  sm:border-r border-sky-200'
      >
        <Heading as='h4' className='w-full mb-8 capitalize text-gray-600 text-center'>reach out</Heading>
        <Box as='ul' className='flex flex-wrap px-4 lg:justify-center gap-4 lg:gap-20'>
          {CONTACTS.map(c =>
            <Box as='li' key={c.icon} className='flex md:flex-col justify-center gap-3'>
              <Box className='flex justify-center items-center p-3 border border-sky-200 w-max rounded-full'>
                <MyIcon href={`/sprite.svg#${c.icon}`} className='w-5 h-5 fill-sky-500' />
              </Box>
              <Box>
                <Text as='p' className='text-gray-400 capitalize'>{c.icon}</Text>
                <Text as='p'>{c.details}</Text>
              </Box>
            </Box>
          )}

        </Box>
      </Box>
      {/* About us */}
      <Box as='section' flexBasis='50%' mt='14'>
        <Heading as='h4' className='w-full mb-8 capitalize text-gray-600 text-center'>who we are ?
        </Heading>
        <Text>
          Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.

        </Text>
        <Box>
        <Heading as='h6' className='mt-4 !text-lg sm:!text-xl'>Meet our team</Heading>
        </Box>
      </Box>
    </footer>
  );
}

export default Footer;
