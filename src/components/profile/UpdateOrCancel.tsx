import { CheckIcon, CloseIcon } from '@chakra-ui/icons';
import { ButtonGroup, IconButton } from '@chakra-ui/react';

type UpdateOrCancelProps = {
  cancel: () => void;
  update: () => void;
  isLoading: boolean;
} & { [k: string]: string };

function UpdateOrCancel({
  cancel,
  update,
  isLoading,
  ...props
}: UpdateOrCancelProps) {
  return (
    <ButtonGroup>
      <IconButton
        aria-label="button"
        icon={<CloseIcon />}
        onClick={cancel}
        {...props}
      />
      <IconButton
        aria-label="button"
        isLoading={isLoading}
        icon={<CheckIcon />}
        onClick={update}
        {...props}
      />
    </ButtonGroup>
  );
}
export default UpdateOrCancel;
