import {
  Text,
  Box,
  Button,
  List,
  ListItem,
  Skeleton,
  Progress,
  Heading
}
  from
  '@chakra-ui/react';
import Upload from './Upload';
import { useInsightsMutation } from '../app/services/auth';
import MyIcon from './Icon';
import { useEffect, useState } from 'react';
import MyModal from './MyModal';

type Props = {
  onClose: () => void,
  isOpen: boolean
}

function Insights({ onClose, isOpen }: Props) {
  const [score, setScore] = useState(0.0);
  const [isFileError, setFileError] = useState(false);
  const [generateInsights,
    { data = {}, isLoading, isSuccess, isUninitialized, isError, error, reset }]
    = useInsightsMutation();

  // effect to increase the ats score on intervals
  useEffect(() => {
    let timeoutID: number;

    if (isSuccess && (score < (data.data.ats_insights.ats_score * 100))) {
      timeoutID = setInterval(() => {
        setScore(score + 0.5);
      });
    }

    // cleanup
    return () => {
      clearInterval(timeoutID);
    };
  });

  const handleSubmit: React.FormEventHandler<HTMLFormElement> = (evt) => {
    evt.preventDefault();
    const formdata = new FormData(evt.currentTarget);
    if (!formdata.get('file').name) {
      setFileError(true);
      return;
    }
    generateInsights(formdata);
  };

  return (
    <MyModal
      title='Scan Resume'
      isOpen={isOpen}
      onClose={() => {
        onClose();
        reset();
        setFileError(false);
        setScore(0.0);
      }}
      body={
        isUninitialized
          ? <form id='insight' onSubmit={handleSubmit}>
            < Upload isError={isFileError} />
          </form>
          : <Skeleton isLoaded={!isLoading}>
            {isError
              ? <Box className='flex flex-col justify-center items-center gap-4'>
                <Text className='w-full p-3 border border-l-4 border-l-red-400 bg-red-100 text-red-400 rounded-md rounded-tl-none rounded-bl-none'>
                  {error?.data.message}
                </Text>
                <MyIcon href='/sprite.svg#upload-error' />
              </Box>
              : <>
                <Heading as='h3' className='!text-base !font-normal'>ATS Score:</Heading>
                <Text className='!font-semibold !text-2xl'>{(score).toFixed(2)}%</Text>
                <Progress
                  className='mb-4'
                  value={score}
                />
                <List spacing='3'>
                  {data.data?.ats_insights.suggestions.map((s, idx) =>
                    <ListItem key={idx} className='flex gap-3'>
                      <Box>
                        <MyIcon href='/sprite.svg#insight' className='w-6 h-6' />
                      </Box>
                      <Text className='sm:text-xl'>
                        {s}
                      </Text>
                    </ListItem>)}
                </List>
              </>
            }
          </Skeleton>
      }
      confirm={
        <Button
          form='insight'
          type='submit'
          isLoading={isLoading}
          disabled={!isUninitialized && (isSuccess || isError)}
          className={`!bg-white !border !border-sky-400 ${!isUninitialized && (isSuccess || isError) ? 'opacity-25' : ''}`}
        >
          scan
        </Button>

      }
    />
  );
}

export default Insights;
