import { Text, Box, Heading } from '@chakra-ui/react';
import MyIcon from './Icon';
import logo from '../assets/logo.png';

const CONTACTS = [
  { icon: 'phone', details: '+1-123-456-7890' },
  { icon: 'email-address', details: 'support@joblinker.com' },
  { icon: 'location', details: 'Sillicon Valley' },
];
const TEAM_MEMBERS = [
  {
    icon: 'linkdedin',
    name: 'Abdallah Abdelrahman',
    link: 'https://www.linkedin.com/in/abdallah-alkaser/',
  },
  {
    icon: 'linkdedin',
    name: 'Mohannad Babeker',
    link: 'https://www.linkedin.com/in/mohannad-abdul-aziz-babeker-6bb984111/',
  },
];

function Footer() {
  return (
    <footer className="footer container mx-auto grid grid-cols-2 gap-8 pt-8 mt-auto bg-white md:flex-row">
      {/* About us */}
      <Box
        as="section"
        className="col-span-2 mt-14 border-b pb-8 px-4 -mb-8 sm:mb-0 sm:border-b-0  sm:border-r border-sky-200 md:col-span-1"
      >
        <Heading
          as="h4"
          className="w-full mb-8 capitalize text-gray-600 text-center"
        >
          who we are ?
        </Heading>
        <Box className="w-1/2 mx-auto sm:w-1/2">
          <img src={logo} className="w-full  object-cover" />
        </Box>
        <Text className="text-lg sm:text-xl">
          we're revolutionizing the hiring process by seamlessly connecting
          qualified candidates with recruiters, all within a single, intuitive
          platform. Our AI-powered project offers cutting-edge Applicant
          Tracking System (ATS) insights, streamlining recruitment workflows and
          enhancing efficiency.
        </Text>
        <Box>
          <Heading as="h6" className="my-4 !text-lg sm:!text-xl">
            Meet our team on linkedin
          </Heading>
          <Box as="ul" className="space-y-4">
            {TEAM_MEMBERS.map((m, idx) => (
              <Box key={idx} as="li" className="flex gap-4 items-end">
                <Box className="flex w-10 h-10 p-2 rounded-lg shadow-md">
                  <MyIcon
                    href={`/sprite.svg#${m.icon}`}
                    className="fill-sky-500"
                  />
                </Box>
                <a href={m.link} target="_blank">
                  {m.name}
                </a>
              </Box>
            ))}
          </Box>
        </Box>
      </Box>
      {/* Contanct */}
      <Box
        as="section"
        className="flex flex-col col-span-2 mt-14 px-4 md:col-span-1"
      >
        <Heading
          as="h4"
          className="w-full mb-8 capitalize text-gray-600 text-center"
        >
          reach out
        </Heading>
        <MyIcon href="/sprite.svg#reach-out" className="w-full h-1/2" />
        <Box as="ul" className="flex flex-wrap gap-4 lg:gap-20">
          {CONTACTS.map((c) => (
            <Box
              as="li"
              key={c.icon}
              className="flex md:flex-col justify-center gap-3"
            >
              <Box className="flex justify-center items-center p-3 border border-sky-200 w-max rounded-full">
                <MyIcon
                  href={`/sprite.svg#${c.icon}`}
                  className="w-5 h-5 fill-sky-500"
                />
              </Box>
              <Box>
                <Text as="p" className="text-gray-400 capitalize">
                  {c.icon}
                </Text>
                <Text as="p">{c.details}</Text>
              </Box>
            </Box>
          ))}
        </Box>
      </Box>
      {/* Copyright */}
      <Box className="copyright col-span-2 text-center p-4">
        joblinker &copy; 2024
      </Box>
    </footer>
  );
}

export default Footer;
