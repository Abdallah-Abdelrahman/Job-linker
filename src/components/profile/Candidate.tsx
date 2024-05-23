import { Text, Heading, Box, Stack, Button, ButtonGroup, Input, InputGroup, InputLeftElement, Textarea, FormControl, List, ListItem, IconButton, Select } from '@chakra-ui/react';
import MyIcon from '../Icon';
import * as T from './types';
import { Reducer, useReducer, useState } from 'react';
import { useUpdateSkillMutation } from '../../app/services/skill';
import { useUpdateLanguageMutation } from '../../app/services/language';
import { useUpdateWorkExperienceMutation } from '../../app/services/work_experience';
import { CheckIcon, CloseIcon } from '@chakra-ui/icons';
import { useUpdateMeMutation, useUploadProfileImageMutation } from '../../app/services/auth';
import { useUpdateMajorMutation } from '../../app/services/major';
import { college_majors } from '../../constants';
import Photo from './Photo';

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


function Candidate({ data }: T.CandidateProp) {
  const [isEditing, setIsEditing] = useState(false);
  const [file, setFile] = useState<File|null>(null);
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
      name: data.name ?? '',
      email: data.email ?? '',
      image_url: data.image_url ?? '',
      contact_info: data.contact_info ?? '',
      major: data.candidate.major.name ?? ''
    }
  );
  const [update, { isLoading: isLoading_MME }] = useUpdateMeMutation();
  const [update_major, { isLoading: isLoading_MMAJOR }] = useUpdateMajorMutation();
  const [upload, {isLoading: isLoading_MUPLOAD}] = useUploadProfileImageMutation();
  const handleUpdate = () => {
    const { major, image_url, email, ...rest } = state;
    console.log({ state })
      const formdata = new FormData();
    formdata.append('file', file)
    
        Promise.all([
          update(rest)
            .unwrap(),
          update_major({
            major_id: data.candidate.major.id,
            major: { name: major }
          }).unwrap(),
          upload(formdata).unwrap
        ])
          .then(_ => setIsEditing(false))
          .catch(err => console.log({ err }))
          .finally(() => {
            setIsEditing(false);
          })
    
  };

  return (
    <Box className='grid grid-cols-4 gap-6 container mt-4 mx-auto sm:grid-cols-12'>
      {/* Contact & skills */}
      <Box
        className='relative  col-span-4 bg-white flex p-6 flex-col items-center gap-2 rounded-md shadow-md sm:col-span-4 sm:max-h-[900px] sm:overflow-auto'
      >
        <Button
          className='!absolute top-6 right-6'
          onClick={() => setIsEditing(true)}
        >
          <MyIcon href='/sprite.svg#edit' className='w-6 h-6' />
        </Button>
        <Photo
          disabled={!isEditing}
          isLoading={isLoading_MUPLOAD}
          imageUrl={data.image_url}
          setFile={setFile}
        />
        {isEditing
          ?
          <FormControl size='lg'>
            <Input
              value={state.name}
              onChange={(e) => dispatch(actionCreator({ name: e.target.value }))}
            />
          </FormControl>
          : <Heading as='h2' size='lg' className='capitalize'>{data.name}</Heading>
        }

        {isEditing
          ? <FormControl size='lg'>
            <Select
              value={state.major}
              onChange={(e) => dispatch(actionCreator({ major: e.target.value }))}
            >
              {college_majors.map((m, idx) => <option key={idx} value={m} children={m} />)}
            </Select>
          </FormControl>
          : <Text className='tracking-wide'>{data.candidate.major.name}</Text>
        }
        <hr className='w-full' />
        <Stack className='w-full mt-2 space-y-6'>
          <Contact_info
            isEditing={isEditing}
            dispatch={dispatch}
            data={data.contact_info}
            state={state}
          />
          {isEditing
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
              {data.candidate.skills.map((skill, idx) =>
                <Skill key={idx} skill={skill} />
              )}
            </ul>
          </Box>
          <Box as='section' className='flex flex-col gap-4'>
            {/*Languages*/}
            <Heading as='h4' mb='2' size='lg' className='capitalize'>languages</Heading>
            <List as='ul' className='flex flex-wrap gap-4 max-h-40 overflow-auto'>
              {data.candidate.languages.map((l, idx) =>
                <Language key={idx} language={l} />
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
          <Bio bio={data.bio} />
        </Box>
        {/*Experience*/}
        <Box>
          <Heading as='h4' mb='4' size='lg' className='capitalize'>
            experience
          </Heading>
          <List as='ul' className='flex flex-col gap-4'>
            {data.candidate.experiences.map((xp, idx) =>
              <Experience key={idx} xp={xp} />
            )}
          </List>
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

type BioProps = {
  bio: string
}
function Bio({ bio }: BioProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [value, setValue] = useState(bio);
  const [textareaH, setTextareaH] = useState(0);
  const [update, { isLoading }] = useUpdateMeMutation();
  const handleUpdate = () => {
    update({ bio: value })
      .unwrap()
      .then(_ => setIsEditing(false))
      .catch(err => console.log({ err }))
  }

  return (
    isEditing
      ? (/* render eiditing version */
        <Stack>
          <Textarea
            ref={(el) => {
              if (!el) return;
              if (!textareaH) {
                setTextareaH(el.scrollHeight);
              }
            }}
            value={value}
            onChange={(e) => {
              setValue(e.target.value);
              e.target.style.height = 'iherit';
              e.target.style.height = `${e.target.scrollHeight}px`;
            }}
            resize='vertical'
            h={textareaH + 'px'}
          />

          <ButtonGroup>
            <IconButton
              aria-label='button'
              icon={<CloseIcon />}
              onClick={() => {
                setIsEditing(false);
                setValue(bio);
              }}
            />
            <IconButton
              aria-label='button'
              isLoading={isLoading}
              icon={<CheckIcon />}
              onClick={handleUpdate}
            />
          </ButtonGroup>
        </Stack>
      )
      : (/* render normal version */
        <>
          <Button
            className='!absolute !px-1 top-0 right-0'
            onClick={() => setIsEditing(true)}
          >
            <MyIcon href='/sprite.svg#edit' className='w-5 h-5' />
          </Button>
          <Text>{bio}</Text>
        </>
      )
  );

}
type ExperProps = {
  xp: T.Experience
}
function Experience({ xp }: ExperProps) {
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
              <InputLeftElement children={<MyIcon href='/sprite.svg#company' className='w-5 h-5 fill-gray-500' />} />
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
              <Button onClick={() => setIsEditing(true)} className='!absolute !px-1 top-0 right-0'>
                <MyIcon href='/sprite.svg#edit' className='w-5 h-5' />
              </Button>
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
type SkillProps = {
  skill: T.Skill
}
function Skill({ skill }: SkillProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [value, setValue] = useState(skill.name);
  const [update, { isLoading }] = useUpdateSkillMutation();
  const handleUpdate = () => {
    update({ skill_id: skill.id, skill: { name: value } })
      .unwrap()
      .then(_ => setIsEditing(false))
      .catch(err => console.log({ err }))
  }

  return (
    <li className='relative p-2 pr-4 bg-teal-50 text-teal-500 rounded-tl-lg rounded-br-lg'>
      {isEditing
        ? <>
          <Input className='!w-max' value={value} onChange={(e) => setValue(e.target.value)} />
          <ButtonGroup>
            <Button
              size='sm'
              children='udpate'
              isLoading={isLoading}
              onClick={handleUpdate}
            />
            <Button
              size='sm'
              children='cancel'
              onClick={() => setIsEditing(false)}
            />
          </ButtonGroup>
        </>
        : <>
          <MyIcon
            href='/sprite.svg#edit' className='absolute top-0 right-0 w-3 h-3 cursor-pointer'
            onClick={() => setIsEditing(true)}
          />
          <Text>{value}</Text>
        </>
      }

    </li>

  );
}

type LangaugeProps = {
  language: T.Language
}
function Language({ language }: LangaugeProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [value, setValue] = useState(language.name);
  const [update, { isLoading }] = useUpdateLanguageMutation();

  const handleUpdate = () => {
    update({ language_id: language.id, language: { name: value } })
      .unwrap()
      .then(_ => setIsEditing(false))
      .catch(err => console.log({ err }))
      .finally(() => {
        setIsEditing(false)
      });
  };

  return (
    <ListItem
      className='relative p-2 bg-orange-50 text-orange-500 rounded-tl-lg rounded-br-lg'
    >
      {isEditing
        ? (/* render input field to edit value */
          <>
            <Input className='!w-max' value={value} onChange={(e) => setValue(e.target.value)} />
            <ButtonGroup>
              <Button
                size='sm'
                children='udpate'
                isLoading={isLoading}
                onClick={handleUpdate}
              />
              <Button
                size='sm'
                children='cancel'
                onClick={() => setIsEditing(false)}
              />
            </ButtonGroup>
          </>
        )
        : (/* render normal text component */
          <>
            <MyIcon
              href='/sprite.svg#edit' className='absolute top-0 right-0 w-3 h-3 cursor-pointer'
              onClick={() => setIsEditing(true)}
            />
            <Text>{value}</Text>
          </>
        )
      }
    </ListItem>
  );
}
type ContactProps = {
  data: Record<'address' | 'github' | 'linkedin' | 'whatsapp' | 'phone', string>,
  dispatch: React.Dispatch<A>,
  isEditing: boolean,
  state: S
}
export function Contact_info({ data, isEditing, state, dispatch }: ContactProps) {
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

/**
 * utility to format date
 * @param {Date} date - date object
 * @returns string format in `Month year`
 */
function formateDate(date: Date) {
  return new Date(date).toLocaleDateString('en', { year: 'numeric', month: 'short' });
}

export default Candidate;
