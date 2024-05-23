import { Text, Heading, Box, Stack, Button, ButtonGroup, Input, InputGroup, InputLeftElement, Textarea, FormControl } from '@chakra-ui/react';
import MyIcon from '../Icon';
import * as T from './types';
import { Reducer, useReducer, useState } from 'react';
import { useUpdateSkillMutation } from '../../app/services/skill';

type ActionType = 'contact_info' | undefined
type S = Omit<T.CandidateProp['data'], 'candidate'> & { major: string }
type A = {
  type?: ActionType,
  payload: Partial<S>
}
/**
 * custom function to create action
 */
const actionCreator = (payload: A['payload'], type?: A['type']) => ({ payload, type });


function Candidate({ data }: T.CandidateProp) {
  const [isEditingInfo, setIsEditiing] = useState(false);
  const [state, dispatch] = useReducer<Reducer<S, A>>(
    (state, action) => {
      const { type, payload } = action;
      if (!type) {
        return { ...state, ...payload };
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
      bio: data.bio ?? '',
      major: data.candidate.major.name ?? ''
    }
  );

  return (
    <Box className='grid grid-cols-4 gap-6 container mt-4 mx-auto sm:grid-cols-12'>
      {/* Contact & skills */}
      <Box
        className='relative  col-span-4 bg-white flex p-6 flex-col items-center gap-2 rounded-md shadow-md sm:col-span-4 sm:max-h-[900px] sm:overflow-auto'
      >
        <Button
          className='!absolute top-6 right-6'
          onClick={() => setIsEditiing(true)}
        >
          <MyIcon href='/sprite.svg#edit' className='w-6 h-6' />
        </Button>
        <Box className='w-32 h-32 min-h-32 bg-red-200 rounded-full overflow-hidden'>
          <img
            src='https://placehold.co/600x400'
            className='w-full h-full object-cover'
          />
        </Box>
        {isEditingInfo
          ?
          <FormControl size='lg'>
            <Input
              value={state.name}
              onChange={(e) => dispatch(actionCreator({ name: e.target.value }))}
            />
          </FormControl>
          : <Heading as='h2' size='lg' className='capitalize'>{data.name}</Heading>}

        {isEditingInfo
          ? <FormControl size='lg'>
            <Input
              value={state.major}
              onChange={(e) => dispatch(actionCreator({ major: e.target.value }))}
            />
          </FormControl>
          : <Text className='tracking-wide'>{data.candidate.major.name}</Text>}

        <hr className='w-full' />
        <Stack className='w-full mt-2 space-y-6'>
          <Contact_info
            isEditingInfo={isEditingInfo}
            dispatch={dispatch}
            data={data.contact_info}
            state={state}
          />
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
        {isEditingInfo &&
          <ButtonGroup className='ml-auto'>
            <Button
              children='update'
            />
            <Button
              onClick={() => setIsEditiing(false)}
              children='cancel'
            />
          </ButtonGroup>
        }

      </Box>

      <Box className=' col-span-4 bg-white flex flex-col rounded-md shadow-md p-6 gap-4 sm:col-span-8 sm:max-h-[900px] sm:overflow-auto'>
        {/*About*/}
        <Box>
          <Heading as='h4' mb='2' size='lg' className='capitalize'>
            About me
          </Heading>
          {isEditingInfo
            ? <FormControl
              size='lg'
              children={
                <Textarea
                  value={state.bio}
                  onChange={(e) => dispatch(actionCreator({ bio: e.target.value }))}
                />}
            />
            : <Text>
              {data.bio}
            </Text>}

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
type ContactProps = {
  data: Record<'address' | 'github' | 'linkedin' | 'whatsapp' | 'phone', string>,
  dispatch: React.Dispatch<A>,
  isEditingInfo: boolean,
  state: S
}
export function Contact_info({ data, isEditingInfo, state, dispatch }: ContactProps) {
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
            {isEditingInfo
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
