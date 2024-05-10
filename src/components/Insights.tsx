import { Button, Modal, ModalBody, ModalCloseButton, ModalContent, ModalFooter, ModalHeader, ModalOverlay } from "@chakra-ui/react";

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
          Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.
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
