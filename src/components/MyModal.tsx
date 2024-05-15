import {
  Text,
  Box,
  Button,
  List,
  ListItem,
  Modal,
  ModalBody,
  ModalCloseButton,
  ModalContent,
  ModalFooter,
  ModalHeader,
  ModalOverlay,
  Skeleton,
  Progress,
  Heading
}
  from
  '@chakra-ui/react';

type Props = {
  onClose: () => void,
  isOpen: boolean,
  body: React.ReactNode
  title: string,
  confirm: React.ReactNode
}

function MyModal({ title, onClose, isOpen, body, confirm }: Props) {

  return (
    <Modal onClose={onClose} isOpen={isOpen} size='4xl' isCentered>
      <ModalOverlay />
      <ModalContent>
        <ModalHeader className='capitalize'>{title}</ModalHeader>
        <ModalCloseButton />
        <ModalBody>
          {body}
        </ModalBody>
        <ModalFooter className='space-x-4'>
          <Button onClick={onClose}>Close</Button>
          {confirm}
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
}

export default MyModal;
