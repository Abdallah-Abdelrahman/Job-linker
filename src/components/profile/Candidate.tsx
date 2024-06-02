import {
  Text,
  Heading,
  Box,
  Stack,
  Button,
  ButtonGroup,
  Input,
  InputGroup,
  InputLeftElement,
  FormControl,
  List,
  IconButton,
  Select,
  Divider
} from '@chakra-ui/react';
import MyIcon from '../Icon';
import * as T from './types';
import { Fragment, Reducer, useReducer, useState } from 'react';
import { CheckIcon, CloseIcon } from '@chakra-ui/icons';
import { useMeQuery, useUpdateMeMutation, useUploadProfileImageMutation } from '../../app/services/auth';
import { useCreateMajorMutation } from '../../app/services/major';
import { college_majors } from '../../constants';
import Photo from './Photo';
import {
  useUpdateCurrentCandidateMutation,
} from '../../app/services/candidate';
import { useMatch, useParams } from 'react-router-dom';
import Bio from './Bio';
import Education from './Education';
import Experience from './Experience';
import Skill from './Skill';
import Language from './Language';

type ActionType = 'reset' | 'contact_info' | undefined
type S = Omit<T.CandidateProp['data'], 'candidate' | 'bio'> & { major: string }
type A = {
  type?: ActionType,
  payload: Partial<S>
}
/**
 * custom function to create action
 */
const actionCreator = (payload: A['payload'], type?: A['type']) => ({ payload, type });


function Candidate({ data, as }: T.CandidateProp) {
  const { id } = useParams() as { id: string };
  const match = useMatch('@me');
  const { data: userData = { data: {} } } = useMeQuery({ id });
  const [isEditing, setIsEditing] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [state, dispatch] = useReducer<Reducer<S, A>>(
    (state, action) => {
      const { type, payload } = action;
      if (!type) {
        return { ...state, ...payload };
      }
      if (type === 'reset') {
        const { candidate, bio, ...rest } = data;
        return ({ ...rest, major: candidate.major.name });
      }

      return ({
        ...state,
        contact_info: { ...state.contact_info, ...payload }
      });
    },
    {
      name: data?.name ?? '',
      email: data?.email ?? '',
      image_url: data?.image_url ?? '',
      contact_info: data?.contact_info ?? '',
      major: data?.candidate.major.name ?? ''
    }
  );
  const [update, { isLoading: isLoading_MME }] = useUpdateMeMutation();
  const [add_major, { isLoading: isLoading_MMAJOR }] = useCreateMajorMutation();
  const [update_candid, { isLoading: isLoading_MCANDID }] = useUpdateCurrentCandidateMutation();
  const [upload, { isLoading: isLoading_MUPLOAD }] = useUploadProfileImageMutation();
  const handleUpdate = () => {
    const { major, image_url, email, ...rest } = state;
    console.log({ state });
    const formdata = new FormData();
    formdata.append('file', file!);

    Promise.allSettled([
      update(rest).unwrap(),
      add_major({ name: major })
        .unwrap()
        .then(({ data }) => update_candid({ major_id: data.id })),
      upload(formdata).unwrap(),
    ])
      .then(_ => setIsEditing(false))
      .catch(err => console.log({ err }))
      .finally(() => {
        setIsEditing(false);
      });
  };
  const renderedData = !as ? data : userData.data;


  return (
    <Box className='grid grid-cols-4 gap-6 container mt-4 mx-auto sm:grid-cols-12'>
      {/* Contact & skills */}
      <Box
        className='relative  col-span-4 bg-white flex p-6 flex-col items-center gap-2 rounded-md shadow-md sm:col-span-4 sm:max-h-[900px] sm:overflow-auto'
      >
        {as
          ? null
          : (
            <Button
              className='!absolute top-6 right-6'
              onClick={() => setIsEditing(true)}
            >
              <MyIcon href='/sprite.svg#edit' className='w-6 h-6' />
            </Button>
          )
        }

        <Photo
          disabled={!isEditing}
          isLoading={isLoading_MUPLOAD}
          imageUrl={renderedData?.imageUrl}
          setFile={setFile}
        />
        {isEditing && !as
          ?
          <FormControl size='lg'>
            <Input
              value={state.name}
              onChange={(e) => dispatch(actionCreator({ name: e.target.value }))}
            />
          </FormControl>
          : <Heading as='h2' size='lg' className='capitalize'>{renderedData?.name}</Heading>
        }

        {isEditing && !as
          ? <FormControl size='lg'>
            <Select
              value={state.major}
              onChange={(e) => dispatch(actionCreator({ major: e.target.value }))}
            >
              {college_majors.map((m, idx) => <option key={idx} value={m} children={m} />)}
            </Select>
          </FormControl>
          : <Text className='tracking-wide'>{renderedData?.candidate?.major.name}</Text>
        }
        <hr className='w-full' />
        <Stack className='w-full mt-2 space-y-6'>
          <Contact_info
            isEditing={isEditing}
            dispatch={dispatch}
            data={renderedData?.contact_info}
            state={state}
          />
          {isEditing && !as
            && (
              <ButtonGroup>
                <IconButton
                  aria-label='button'
                  icon={<CloseIcon />}
                  onClick={() => {
                    setIsEditing(false);
                    dispatch({ type: 'reset' });
                  }}
                />
                <IconButton
                  aria-label='button'
                  isLoading={isLoading_MME || isLoading_MMAJOR}
                  icon={<CheckIcon />}
                  onClick={handleUpdate}
                />
              </ButtonGroup>
            )
          }
          <Box as='section' className='flex flex-col gap-4'>
            {/*Skills*/}
            <Heading as='h4' mb='2' size='lg' className='capitalize'>skills</Heading>
            <ul className='flex flex-wrap gap-4 max-h-64 overflow-auto'>
              {renderedData?.candidate?.skills.map((skill, idx) =>
                <Skill key={idx} skill={skill} isEditable={Boolean(match)} />
              )}
            </ul>
          </Box>
          <Box as='section' className='flex flex-col gap-4'>
            {/*Languages*/}
            <Heading as='h4' mb='2' size='lg' className='capitalize'>languages</Heading>
            <List as='ul' className='flex flex-wrap gap-4 max-h-40 overflow-auto'>
              {renderedData?.candidate?.languages.map((l, idx) =>
                <Language key={idx} language={l} isEditable={Boolean(match)} />
              )}
            </List>
          </Box>
        </Stack>

      </Box>

      <Box className=' col-span-4 bg-white flex flex-col rounded-md shadow-md p-6 gap-4 sm:col-span-8 sm:max-h-[900px] sm:overflow-auto'>
        {/*About*/}
        <Box className='relative'>
          <Heading as='h4' mb='2' size='lg' className='capitalize'>
            About me
          </Heading>
          <Bio isEditable={Boolean(match)} bio={renderedData?.bio} />
        </Box>
        {/*Experience*/}
        <Box>
          <Heading as='h4' mb='4' size='lg' className='capitalize'>
            experience
          </Heading>
          <List as='ul' className='flex flex-col gap-4'>
            {renderedData?.candidate?.experiences.map((xp, idx) =>
              <Experience isEditable={Boolean(match)} key={idx} xp={xp} />
            )}
          </List>
        </Box>
        {/*Education*/}
        <Box>
          <Heading as='h4' mb='4' size='lg' className='capitalize'>
            education
          </Heading>
          <List as='ul' className='flex flex-col gap-4'>
            {renderedData?.candidate?.education.map((ed, idx, arr) => (
              <Fragment key={idx}>
                <Education isEditable={Boolean(match)} ed={ed} />
                {idx !== arr.length - 1
                  && (
                    <Divider colorScheme='blue' />
                  )}
              </Fragment>
            ))}
          </List>
        </Box>
      </Box>
    </Box>
  );
}



type ContactProps = {
  data: Record<'address' | 'github' | 'linkedin' | 'whatsapp' | 'phone', string>,
  dispatch: React.Dispatch<A>,
  isEditing: boolean,
  state: S
}

function Contact_info({ data, isEditing, state, dispatch }: ContactProps) {
  if (!data) {
    return (null);
  }

  return (
    <Box as='section' className='flex flex-col gap-4'>
      <Heading as='h4' mb='2' size='lg' className='capitalize'>contact info</Heading>
      {Object.entries(data).map(([k, v]) => {
        if (!v) return (null);
        return (
          <Box key={k} className='flex gap-3'>
            {isEditing
              ? (
                <>
                  <InputGroup>
                    <InputLeftElement
                      children={<MyIcon href={`/sprite.svg#${k}`} className='w-5 h-5' />}
                    />
                    <Input
                      value={state.contact_info[k]}
                      onChange={(e) => dispatch(actionCreator({ [k]: e.target.value }, 'contact_info'))}
                    />
                  </InputGroup>
                </>
              )
              : (
                <>
                  <MyIcon href={`/sprite.svg#${k}`} className='w-5 h-5' />
                  {k == 'linkedin' || k == 'github'
                    ? <a href={v} target='_blank' className='text-sky-500'>{k}</a>
                    : <Text>{v}</Text>
                  }
                </>
              )
            }

          </Box>
        );
      }
      )}
    </Box>
  );
}


export { Candidate as default, Contact_info };
