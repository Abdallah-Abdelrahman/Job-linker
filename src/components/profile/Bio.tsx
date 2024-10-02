import { useState } from 'react';
import { useUpdateMeMutation } from '../../app/services/auth';
import {
  Button,
  ButtonGroup,
  IconButton,
  Stack,
  Text,
  Textarea,
} from '@chakra-ui/react';
import { CheckIcon, CloseIcon } from '@chakra-ui/icons';
import MyIcon from '../Icon';

type BioProps = {
  bio: string;
  isEditable: boolean;
};
function Bio({ bio, isEditable }: BioProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [value, setValue] = useState(bio);
  const [textareaH, setTextareaH] = useState(0);
  const [update, { isLoading }] = useUpdateMeMutation();
  const handleUpdate = () => {
    update({ bio: value })
      .unwrap()
      .then((_) => setIsEditing(false))
      .catch((err) => console.log({ err }));
  };

  return isEditing ? (
    /* render eiditing version */
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
        resize="vertical"
        h={textareaH + 'px'}
      />
      <ButtonGroup>
        <IconButton
          aria-label="button"
          icon={<CloseIcon />}
          onClick={() => {
            setIsEditing(false);
            setValue(bio);
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
    /* render normal version */
    <>
      {isEditable && (
        <Button
          className="!absolute !px-1 top-0 right-0"
          onClick={() => setIsEditing(true)}
        >
          <MyIcon href="/sprite.svg#edit" className="w-5 h-5" />
        </Button>
      )}
      <Text>{bio}</Text>
    </>
  );
}

export default Bio;
