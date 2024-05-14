import { Text, Box, Button, List, ListItem, Modal, ModalBody, ModalCloseButton, ModalContent, ModalFooter, ModalHeader, ModalOverlay, Skeleton, Progress } from "@chakra-ui/react";
import Upload from "./Upload";
import { useInsightsMutation } from "../app/services/auth";
import MyIcon from "./Icon";

type Props = {
  onClose: () => void,
  isOpen: boolean
}

function Insights({ onClose, isOpen }: Props) {
  const [generateInsights, { data, isLoading, isSuccess }] = useInsightsMutation();

  const handleSubmit: React.FormEventHandler<HTMLFormElement> = (evt) => {
    console.log('%chello', 'background:red;');
    evt.preventDefault();
    const formdata = new FormData(evt.currentTarget);
    if (!formdata.get('file').name) return;
    generateInsights(formdata);
  };

  return (
    <Modal onClose={onClose} isOpen={isOpen} size='4xl' isCentered>
      <ModalOverlay />
      <ModalContent>
        <ModalHeader>Scan Resume</ModalHeader>
        <ModalCloseButton />
        <ModalBody>
          {!isSuccess
            ? <form id='insight' onSubmit={handleSubmit}>
              <Upload />
            </form>
            : <Skeleton isLoaded={isSuccess}>
              <Text>ATS Score:</Text>
		<Text mr={2}>{(data.data.ats_insights.ats_score * 100).toFixed(2)}%</Text>
		<Progress className="progress-bar" value={data.data.ats_insights.ats_score * 100} />
              <List spacing='3'>
                {data.data.ats_insights.suggestions.map((s, idx) =>
                  <ListItem key={idx} className='flex gap-3'>
                    <Box>
                      <MyIcon href='/sprite.svg#insight' className='w-6 h-6' />
                    </Box>
                    <Text>
                      {s}
                    </Text>
                  </ListItem>)}
              </List>
            </Skeleton>
          }

        </ModalBody>
        <ModalFooter className='space-x-4'>
          <Button onClick={onClose}>Close</Button>
          <Button
            form='insight'
            type='submit'
            isLoading={isLoading}
          >
            scan
          </Button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
}

export default Insights;
