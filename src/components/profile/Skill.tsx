import { useState } from 'react';
import * as T from './types';
import { useAddSkillToCurrentCandidateMutation, useRemoveSkillFromCurrentCandidateMutation } from '../../app/services/candidate';
import { useCreateSkillMutation } from '../../app/services/skill';
import { Input, Text } from '@chakra-ui/react';
import UpdateOrCancel from './UpdateOrCancel';
import MyIcon from '../Icon';

type SkillProps = {
  skill: T.Skill
  isEditable: boolean
}
function Skill({ skill, isEditable }: SkillProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [value, setValue] = useState(skill.name);
  const [removeCandidSkill, { isLoading: isLoading1 }] = useRemoveSkillFromCurrentCandidateMutation();
  const [add, { isLoading: isLoading2 }] = useCreateSkillMutation();
  const [addCandidSkill, { isLoading: isLoading3 }] = useAddSkillToCurrentCandidateMutation();
  const handleUpdate = () => {
    Promise.allSettled([
      removeCandidSkill({ skill_id: skill.id }).unwrap(),
      add({ name: value })
        .unwrap()
        .then(({ data }) => addCandidSkill({ skill_id: data.id }))
        .catch(err => console.log({ err }))
        .finally(() => {
          setIsEditing(false);
        })
    ]);
  };

  return (
    <li className='relative p-2 pr-4 bg-teal-50 text-teal-500 rounded-tl-lg rounded-br-lg'>
      {isEditing
        ? <>
          <Input className='!w-max' value={value} onChange={(e) => setValue(e.target.value)} />
          <UpdateOrCancel
            size='sm'
            rounded='full'
            isLoading={isLoading1 || isLoading2 || isLoading3}
            cancel={() => {
              setIsEditing(false);
              setValue(skill.name);

            }}
            update={handleUpdate}
          />
        </>
        : <>
          {isEditable && (
            <MyIcon
              href='/sprite.svg#edit' className='absolute top-0 right-0 w-3 h-3 cursor-pointer'
              onClick={() => setIsEditing(true)}
            />
          )}
          <Text>{value}</Text>
        </>
      }

    </li>
  );
}

export default Skill;
