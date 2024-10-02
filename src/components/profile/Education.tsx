import { useReducer, useState } from 'react';
import { useUpdateEducationForCurrentCandidateMutation } from '../../app/services/candidate';
import {
  Box,
  Button,
  ButtonGroup,
  IconButton,
  Input,
  InputGroup,
  InputLeftAddon,
  ListItem,
  Stack,
  Text,
} from '@chakra-ui/react';
import { CheckIcon, CloseIcon } from '@chakra-ui/icons';
import MyIcon from '../Icon';
import { formateDate } from '../../helpers';

type EducationProps = {
  ed: Education;
  isEditable: boolean;
};
function Education({ ed, isEditable }: EducationProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [update, { isLoading }] =
    useUpdateEducationForCurrentCandidateMutation();
  const [state, dispatch] = useReducer(
    (prevState, newState) => {
      if (newState.type === 'reset') {
        return ed;
      }
      return { ...prevState, ...newState };
    },
    {
      degree: ed.degree,
      institute: ed.institute,
      field_of_study: ed.field_of_study,
      start_date: ed.start_date,
      end_date: ed.end_date,
    },
  );
  const handleUpdate = () => {
    update({
      education_id: ed.id,
      education: {
        ...state,
        start_date: new Date(state.start_date),
        end_date: new Date(state.end_date),
      },
    })
      .unwrap()
      .then((_) => setIsEditing(false))
      .catch((err) => console.log({ err }))
      .finally(() => {
        setIsEditing(false);
      });
  };

  return isEditing ? (
    /* render editing jsx */
    <Stack>
      <InputGroup>
        <InputLeftAddon>field</InputLeftAddon>
        <Input
          value={state.field_of_study}
          onChange={(e) => dispatch({ field_of_study: e.target.value })}
        />
      </InputGroup>
      <InputGroup>
        <InputLeftAddon>school</InputLeftAddon>
        <Input
          value={state.institute}
          onChange={(e) => dispatch({ institute: e.target.value })}
        />
      </InputGroup>
      <InputGroup>
        <InputLeftAddon>degree</InputLeftAddon>
        <Input
          value={state.degree}
          onChange={(e) => dispatch({ degree: e.target.value })}
        />
      </InputGroup>
      <InputGroup>
        <InputLeftAddon>start_date</InputLeftAddon>
        <Input
          type="datetime-local"
          value={new Date(state.start_date).toISOString().slice(0, 16)}
          onChange={(e) => dispatch({ start_date: e.target.value })}
        />
      </InputGroup>
      <InputGroup>
        <InputLeftAddon>end_date</InputLeftAddon>
        <Input
          type="datetime-local"
          value={new Date(state.end_date).toISOString().slice(0, 16)}
          onChange={(e) => dispatch({ end_date: e.target.value })}
        />
      </InputGroup>
      <ButtonGroup>
        <IconButton
          aria-label="button"
          icon={<CloseIcon />}
          onClick={() => {
            setIsEditing(false);
            dispatch({ type: 'reset' });
          }}
        />
        <IconButton
          aria-label="button"
          isLoading={isLoading}
          icon={<CheckIcon />}
          onClick={handleUpdate}
        />
      </ButtonGroup>
    </Stack>
  ) : (
    /* render normal jsx */
    <ListItem className="relative">
      {isEditable && (
        <Button
          onClick={() => setIsEditing(true)}
          className="!absolute !p-0 top-0 right-0"
        >
          <MyIcon href="/sprite.svg#edit" className="w-5 h-5" />
        </Button>
      )}
      <Box className="flex flex-col gap-3 w-full">
        <Box className="flex gap-2">
          <Box className="flex gap-1">
            <MyIcon
              href="/sprite.svg#field_of_study"
              className="w-5 h-5 fill-gray-500"
            />
            <Text className="text-gray-500">field</Text>
          </Box>
          <Text className="font-semibold">{ed.field_of_study}</Text>
        </Box>
        <Box className="flex gap-2">
          <Box className="flex gap-1">
            <MyIcon
              href="/sprite.svg#school"
              className="w-5 h-5 fill-gray-500"
            />
            <Text className="text-gray-500">school</Text>
          </Box>
          <Text className="font-semibold">{ed.institute}</Text>
        </Box>
        <Box className="flex gap-2">
          <Box className="flex gap-1">
            <MyIcon
              href="/sprite.svg#degree"
              className="w-5 h-5 fill-gray-500"
            />
            <Text className="text-gray-500">degree</Text>
          </Box>
          <Text className="font-semibold">{ed.degree}</Text>
        </Box>
        <Box className="flex gap-2">
          <Box className="flex gap-1">
            <MyIcon href="/sprite.svg#date" className="w-5 h-5 fill-gray-500" />
            <Text className="text-gray-500">date</Text>
          </Box>
          <Text className="font-semibold">
            {formateDate(ed.start_date)} - {formateDate(ed.end_date)}
          </Text>
        </Box>
      </Box>
    </ListItem>
  );
}

export default Education;
