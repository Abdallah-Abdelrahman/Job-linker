import {
  Box,
  Heading,
  Button,
  FormControl,
  FormLabel,
  Input,
  Select,
  Skeleton,
} from "@chakra-ui/react";
import { User, useMeQuery, useUpdateMeMutation, useUploadMutation } from "../app/services/auth";
import { useCreateCandidateMutation } from "../app/services/candidate";
import { useCreateRecruiterMutation } from "../app/services/recruiter";
import { useAppSelector } from "../hooks/store";

import { useAfterRefreshQuery } from "../hooks";
import { useCreateMajorMutation } from "../app/services/major";
import { selectCurrentUser } from "../features/auth";
import { Candidate } from "../components/profile";
import { Recruiter } from '../components/profile';
import { MyForm } from "../components/profile";



// Profile component
const Profile = () => {
  // network request
  const {
    data: userData = { data: {} },
    isLoading,
    isSuccess,
    isFetching,
    error,
  } = useAfterRefreshQuery<{ data: User }>(useMeQuery);
  const [updateUser] = useUpdateMeMutation();
  const [uploadCV, { isLoading: cvLoading }] = useUploadMutation();
  const [createCandidate, { isLoading: candidLoading }] =
    useCreateCandidateMutation();
  const [addMajor, { isLoading: majorLoading }] = useCreateMajorMutation();
  const [createRecruiter, { isLoading: recLoading }] =
    useCreateRecruiterMutation();
  const { role } = useAppSelector(selectCurrentUser);

  const handleCandidateFormSubmit = async (formdata: FormData) => {
    console.log(formdata.get('file'));
    try {
      addMajor({ name: formdata.get('major') })
        .unwrap()
        .then((data) => {
          createCandidate({ major_id: data.data.id })
            .unwrap()
            .then(_ => {
              uploadCV(formdata)
                .unwrap()
                .then(_ => {
                  updateUser({ profile_complete: true })
                    .then(_ => console.log('----------profile completed-------->'))
                    .catch(err => console.log('------not completed---->', { err }));
                })
                .catch()
            })
            .catch((err) => console.log({ err }));
        })
        .catch((err) => console.error({ err }));
    } catch (error) {
      console.error(error);
    }
  };

  const handleRecruiterFormSubmit = async (formdata: FormData) => {
  try {
    createRecruiter()
      .unwrap()
      .then(_ => {
        updateUser({ contact_info: Object.fromEntries(formdata) })
          .unwrap()
          .then(_ => {
            updateUser({ profile_complete: true })
              .then(_ => console.log('----------profile completed-------->'))
              .catch(err => console.log('------not completed---->', { err }));
          })
          .catch((error) => {
            console.error(error);
          });
      })
      .catch((error) => {
        console.error(error);
      });
  } catch (error) {
    console.error(error);
  }  
};

  if (role == 'candidate' && isSuccess && userData.data.profile_complete)
    return (<Candidate data={userData.data} />);

  if (role == 'recruiter' && isSuccess && userData.data.profile_complete)
    return (<Recruiter data={userData.data} />);

  return (
    <Box className='mx-auto max-w-2xl my-8'>
      <Skeleton isLoaded={!isLoading}>
        <Heading as="h2" size="xl" className="mb-8 capitalize">
          complete your Profile
        </Heading>
        <MyForm
          role={role}
          onSubmit={role == 'candidate'
            ? handleCandidateFormSubmit
            : handleRecruiterFormSubmit}
          isLoading={role == 'candidate'
            ? candidLoading || cvLoading || majorLoading
            : recLoading
          }
        />
      </Skeleton>
    </Box>
  );
};

export default Profile;
