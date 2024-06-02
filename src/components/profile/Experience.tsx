import { useReducer, useState } from 'react';
import * as T from './types';
import { useUpdateWorkExperienceMutation } from '../../app/services/work_experience';
import { Box, Button, ButtonGroup, Heading, IconButton, Input, InputGroup, InputLeftElement, ListItem, Stack, Text, Textarea } from '@chakra-ui/react';
import MyIcon from '../Icon';
import { CheckIcon, CloseIcon } from '@chakra-ui/icons';
import { formateDate } from '../../helpers';

type ExperProps = {
  xp: T.Experience
  isEditable: boolean
}
function Experience({ xp, isEditable }: ExperProps) {
  const [textareaH, setTextareaH] = useState(0);
  const [isEditing, setIsEditing] = useState(false);
  const [state, dispatch] = useReducer(
    (prevState, newState) => {
      if (newState.type === 'reset') return (prevState);
      return ({ ...prevState, ...newState });
    },
    {
      title: xp.title,
      company: xp.company,
      start_date: xp.start_date,
      end_date: xp.end_date,
      description: xp.description
    });
  const [update, { isLoading }] = useUpdateWorkExperienceMutation();
  const handleUpdate = () => {
    update({
      work_experience_id: xp.id, xp: {
        ...state,
        start_date: new Date(state.start_date),
        end_date: new Date(state.end_date)
      }
    })
      .unwrap()
      .then(_ => setIsEditing(false))
      .catch(err => console.log({ err }))
      .finally(() => { setIsEditing(false); });
  };

  return (
    <ListItem>
      {isEditing
        ? (/* render editing fields */
          <Stack>
            <InputGroup>
              <Input
                value={state.title}
                onChange={(e) => dispatch({ title: e.target.value })}
              />
            </InputGroup>
            <InputGroup>
              <InputLeftElement
                children={<MyIcon href='/sprite.svg#company' className='w-5 h-5 fill-gray-500' />}
              />
              <Input
                value={state.company}
                onChange={(e) => dispatch({ company: e.target.value })}
              />
            </InputGroup>
            <InputGroup>
              <InputLeftElement children={<MyIcon href='/sprite.svg#date' className='w-5 h-5 fill-gray-500' />} />
              <Input
                type='datetime-local'
                value={new Date(state.start_date).toISOString().slice(0, 16)}
                onChange={(e) => dispatch({ start_date: e.target.value })}
              />
            </InputGroup>
            <InputGroup>
              <InputLeftElement children={<MyIcon href='/sprite.svg#date' className='w-5 h-5 fill-gray-500' />} />
              <Input
                type='datetime-local'
                value={new Date(state.end_date).toISOString().slice(0, 16)}
                onChange={(e) => dispatch({ end_date: e.target.value })}
              />
            </InputGroup>
            <InputGroup>
              <Textarea
                ref={(el) => {
                  if (!el) return;
                  if (!textareaH) {
                    setTextareaH(el.scrollHeight);
                  }
                }}
                value={state.description}
                onChange={(e) => {
                  dispatch({ description: e.target.value });
                  e.target.style.height = 'iherit';
                  e.target.style.height = `${e.target.scrollHeight}px`;
                }}
                resize='vertical'
                h={textareaH + 'px'}
              />
            </InputGroup>
            <ButtonGroup>
              <IconButton aria-label='button' icon={<CloseIcon />} onClick={() => {
                setIsEditing(false);
                dispatch({ type: 'reset' });
              }} />
              <IconButton
                aria-label='button'
                isLoading={isLoading}
                icon={<CheckIcon />}
                onClick={handleUpdate}
              />
            </ButtonGroup>
          </Stack>
        )
        : (/* render normal fields */
          <>
            <Box className='relative flex flex-col gap-3 w-full'>
              {isEditable && (
                <Button onClick={() => setIsEditing(true)} className='!absolute !px-1 top-0 right-0'>
                  <MyIcon href='/sprite.svg#edit' className='w-5 h-5' />
                </Button>
              )}
              <Heading as='h6' size='md' className='capitalize max-w-[80%]'>{xp.title.toLowerCase()}</Heading>
              <Box className='space-y-2'>
                <Box className='flex gap-2'>
                  <Box className='flex gap-1'>
                    <MyIcon href='/sprite.svg#company' className='w-5 h-5 fill-gray-500' />
                    <Text className='text-gray-500' children='at' />
                  </Box>
                  <Text className='!max-w-[70%] capitalize font-semibold' children={xp.company.toLowerCase()} />
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

          </>
        )
      }
    </ListItem>

  );
}

export default Experience;
