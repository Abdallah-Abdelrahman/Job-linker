import {
  Accordion,
  AccordionButton,
  AccordionItem,
  AccordionPanel,
  Box,
  Button,
  Heading,
  Text,
  useDisclosure,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  SimpleGrid,
  Card,
  CardHeader,
} from '@chakra-ui/react';
import { Insights, MyIcon, MyModal } from '../components';
import { FAQS } from '../constants';
import { useGetJobCountsQuery } from '../app/services/job';
import { useGetHiredCountQuery } from '../app/services/application';
import { Link, useNavigate } from 'react-router-dom';
import { useAppSelector } from '../hooks/store';
import { selectCurrentUser } from '../features/auth';

function Home() {
  const user = useAppSelector(selectCurrentUser);
  const navigate = useNavigate();
  const { isOpen, onOpen, onClose } = useDisclosure();
  const { isOpen: isOpenPost, onOpen: onOpenPost, onClose: onClosePost } = useDisclosure();
  const { data: jobCounts, isLoading } = useGetJobCountsQuery();
  const { data: hiredCount, isLoading: isHiredCountLoading } =
    useGetHiredCountQuery();

  const CardHeader = ({ children }) => {
    return (
      <Box display='flex' flexDirection='column' alignItems='flex-start'>
        {children}
      </Box>
    );
  };

  const CardComponent = ({ iconHref, label, number, helpText }) => {
    return (
      <Box
        className='hover:scale-110 transition-transform duration-300 shadow-lg'
        p={5}
        borderRadius='md'
        boxShadow='md'
      >
        <Box display='flex' alignItems='flex-start'>
          <MyIcon href={iconHref} className='w-20 h-20 mr-4' />
          <Stat>
            <StatLabel>{label}</StatLabel>
            <StatNumber>{number}</StatNumber>
            <StatHelpText>{helpText}</StatHelpText>
          </Stat>
        </Box>
      </Box>
    );
  };

  return (
    <Box className='home container mx-auto w-full p-4 pt-8'>
      {/* Hero section */}
      <Box
        as='section'
        className='hero w-full h-[calc(100dvh-10rem)] flex flex-col gap-4 max-w-2xl sm:gap-8 mt-[20%]'
      >
        <Heading
          as='h1'
          size={{ base: 'lg', md: '2xl' }}
          className='capitalize'
        >
          simplify hiring, amplify growth
        </Heading>
        <Text className='sm:text-xl sm:leading-8'>
          Find skilled candidates, in-demand jobs and the solutions you need to
          help your cv stands out.
        </Text>
        <Box className='relative z-10 flex flex-col gap-6 sm:flex-row sm:mt-4'>
          <Insights isOpen={isOpen} onClose={onClose} />
          <Button
            size={{ base: 'sm', sm: 'lg' }}
            className='w-40  rounded-md !bg-white !text-sky-600 !outline-sky-400'
            onClick={onOpen}
          >
            ATS insight
          </Button>
          <Button
            size={{ base: 'sm', sm: 'lg' }}
            className='w-40  rounded-md !bg-white !text-sky-600 !outline-sky-400'
            onClick={() => {
              if (user.role == 'recruiter') {
                navigate('@me');
              }
              onOpenPost();
            }}
          >
            post a job
          </Button>
          <MyModal
            title='Post a job'
            isOpen={isOpenPost}
            onClose={onClosePost}
            body={
              !user.jwt
                ? <Text>you need to <Link to='login' className='text-sky-400' children='sign in ' /> as recruiter</Text>
                : <Text>you need to be a recruiter to be able to post a job</Text>
            }
          />
        </Box>
      </Box>
      {/* How it works section */}
      <Box as='section' className='how-it-work -mt-8 py-20 w-full bg-white'>
        <Heading
          as='h2'
          className='mb-8 capitalize text-center text-gray-600 sm:mb-14'
        >
          How it works
        </Heading>
        <Box className='flex flex-wrap gap-8 md:justify-between lg:justify-center lg:gap-24'>
          <Box className='space-y-4'>
            <Box className='grid place-content-center flex-shrink-0 w-12 h-12 rounded-lg bg-white shadow-md sm:w-20 sm:h-20'>
              <MyIcon
                href='/sprite.svg#stats'
                className='fill-sky-500 w-8 h-8 sm:w-12 sm:h-12'
              />
            </Box>
            <Text className='text-lg sm:text-2xl'>
              1. scan your cv with ATS
            </Text>
          </Box>
          <Box className='space-y-4'>
            <Box className='grid place-content-center flex-shrink-0 w-12 h-12 rounded-lg bg-white shadow-md sm:w-20 sm:h-20'>
              <MyIcon
                href='/sprite.svg#matching'
                className='fill-sky-500 w-8 h-8 sm:w-12 sm:h-12'
              />
            </Box>
            <Text className='text-lg sm:text-2xl'>
              2. View matching candidates
            </Text>
          </Box>
          <Box className='space-y-4'>
            <Box className='grid place-content-center flex-shrink-0 w-12 h-12 rounded-lg bg-white shadow-md sm:w-20 sm:h-20'>
              <MyIcon
                href='/sprite.svg#apply'
                className='fill-sky-500 w-8 h-8 sm:w-12 sm:h-12'
              />
            </Box>
            <Text className='text-lg sm:text-2xl'>3. Apply for a job</Text>
          </Box>
        </Box>
      </Box>
      {/* Jobs Counts */}
      {/*
      <Box as='section' className='job-counts py-20 w-full bg-white'>
        <Heading as='h2' className='mb-8 capitalize text-center text-gray-600'>
          Explore. Discover. Achieve.
        </Heading>
        
        {isLoading || isHiredCountLoading ? (
          <Text>Loading...</Text>
        ) : jobCounts && jobCounts.data.major_counts && hiredCount ? (
          <SimpleGrid columns={{ base: 1, md: 2 }} spacing={10}>
            <CardComponent
              iconHref='/sprite.svg#av_jobs'
              label='Total Posted Jobs'
              number={jobCounts.data.total_count}
              helpText='across all majors'
            />
            <CardComponent
              iconHref='/sprite.svg#hired'
              label='Hired Candidates'
              number={hiredCount.data.count}
              helpText='who found their dream jobs'
            />
            {Object.entries(jobCounts.data.major_counts).map(
              ([major, count]) => (
                <CardComponent
                  key={major}
                  iconHref='/sprite.svg#av_jobs'
                  label={major}
                  number={count}
                  helpText='jobs available'
                />
              ),
            )}
          </SimpleGrid>
        ) : (
          <Text>Error loading job counts.</Text>
        )}
      </Box>
      */}
      {/* FAQS section */}
      <Box as='section' className='py-20'>
        <Heading as='h2' className='mb-8 capitalize text-center text-gray-600'>
          FAQs
        </Heading>
        <Accordion allowToggle>
          {FAQS.map((faq, idx) => (
            <AccordionItem key={idx} className='min-h-20'>
              {({ isExpanded }) => (
                <>
                  <h2>
                    <AccordionButton className='!h-full'>
                      <Box
                        as='span'
                        className='flex-1 text-left font-bold sm:text-xl'
                      >
                        {Object.keys(faq)[0]}
                      </Box>
                      {isExpanded ? (
                        <MyIcon href='/sprite.svg#minus' className='w-5 h-5' />
                      ) : (
                        <MyIcon href='/sprite.svg#plus' className='w-5 h-5' />
                      )}
                    </AccordionButton>
                  </h2>
                  <AccordionPanel pb={4} className='text-lg'>
                    {Object.values(faq)[0]}
                  </AccordionPanel>
                </>
              )}
            </AccordionItem>
          ))}
        </Accordion>
      </Box>
    </Box>
  );
}

export default Home;
