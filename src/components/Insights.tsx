import { Box, Button, Modal, ModalBody, ModalCloseButton, ModalContent, ModalFooter, ModalHeader, ModalOverlay } from "@chakra-ui/react";
import Upload from "./Upload";
import { Form } from "react-router-dom";

type Props = {
  onClose: () => void,
  isOpen: boolean
}

function Insights({ onClose, isOpen }: Props) {
  const handleClick = () => {
    // TODO: ajax request
    console.log('scanning...')
  };

  return (
    <Modal onClose={onClose} isOpen={isOpen} size='4xl' isCentered>
      <ModalOverlay />
      <ModalContent>
        <ModalHeader>Scan Resume</ModalHeader>
        <ModalCloseButton />
        <ModalBody>
          <Form>
            <Upload />
          </Form>
        </ModalBody>
        <ModalFooter className='space-x-4'>
          <Button onClick={onClose}>Close</Button>
          <Button onClick={handleClick}>scan</Button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
}

export default Insights;
