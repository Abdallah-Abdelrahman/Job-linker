import { useReducer } from "react";
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
import {
  Recruiter,
  useCreateRecruiterMutation,
} from "../app/services/recruiter";
import { college_majors } from "../constants";
import { useAppSelector } from "../hooks/store";

import { useAfterRefreshQuery } from "../hooks";
import { useCreateMajorMutation } from "../app/services/major";
import { selectCurrentUser } from "../features/auth";
import { Candidate } from "../components/profile";
import { Upload } from "../components";

type TFormdata = {
  file: File,
} & Record<'major' | 'company_info' | 'company_name', string>;
const initialErrorState = {
  candidate: { file: false, major: false },
  recruiter: {}
};
/**
 * manages the error state
 * @param {object} state - error state
 * @param {object} action - object of which the state depends on to update
 *
 * @returns the new state
 */
const reducer = (state, action) => {
  switch (action.type) {
    case 'candidate':
      return { ...state, candidate: { ...state.candidate, ...action.payload } };
    case 'recruiter':
      break;
  }
};

function MyForm({ onSubmit, role, isLoading }) {
  const [formError, dispatch] = useReducer(reducer, initialErrorState);

  const handleSubmit = (evt) => {
    const formdata = new FormData(evt.currentTarget);
    const { file, major, company_info, company_name }
      = Object.fromEntries(formdata) as TFormdata;
    let canSubmit = false;
    evt.preventDefault();
    formdata.append('role', role);

    if (role == 'candidate') {
      dispatch({
        type: 'candidate',
        payload: { file: !(file.name), major: !(major) }
      });
      canSubmit = Boolean(file.name && major);
    }

    if (role == 'recruiter') {
      dispatch({
        type: 'recruiter',
        payload: { company_name: !(company_name), company_info: !(company_info) }
      });
      canSubmit = Boolean(company_name && company_name);
    }

    if (canSubmit) {
      onSubmit(formdata);
    }

  };

  const candidateJSX = (
    <>
      <FormControl>
        <Select
          isInvalid={formError.candidate.major}
          name="major"
          placeholder='select your major'
          color='gray.600'
        >
          {college_majors.map((major) => (
            <option key={major} value={major}>
              {major}
            </option>
          ))}
        </Select>
      </FormControl>
      <Upload isError={formError.candidate.file} />
    </>
  );

  const recruiterJSX = (
    <>
      <FormControl>
        <FormLabel>Company Name:</FormLabel>
        <Input
          type="text"
          name="company_name"
        />
      </FormControl>
      <FormControl isRequired>
        <FormLabel>Company Info:</FormLabel>
        <Input
          type="text"
          name="company_info"
        />
      </FormControl>
    </>
  );

  return (
    <form
      autoComplete='off'
      onSubmit={handleSubmit}
      className='w-full p-6 space-y-4 bg-white rounded-lg shadow-md'
    >
      {role == "candidate" ? candidateJSX : recruiterJSX}
      <Button type="submit" isLoading={isLoading}>Create Profile</Button>
    </form>
  );
}

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
  const [createCandidate, { isSuccess: candidateSuccess, isLoading: candidLoading }] =
    useCreateCandidateMutation();
  const [addMajor, { isLoading: majorLoading }] = useCreateMajorMutation();
  const [createRecruiter, { isSuccess: recruiterSuccess }] =
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

  const handleRecruiterFormSubmit = async (formData: Recruiter) => {
    try {
      const { name, ...recruiterData } = formData;
      await createRecruiter({ user_id: userData.id, ...recruiterData });
    } catch (error) {
      console.error(error);
    }
  };

  const noProfileError =
    error &&
    (error.message === "User doesn't have a candidate profile" ||
      error.message === "User doesn't have a recruiter profile");

  console.log({ userData });
  if (isSuccess && userData.data.profile_complete)
    return (<Candidate data={userData.data} />);

  return (
    <Box className='mx-auto max-w-2xl my-8'>
      <Skeleton isLoaded={!isLoading}>
        <Heading as="h2" size="xl" className="mb-8 capitalize">
          complete your Profile
        </Heading>
        <MyForm
          role={role}
          onSubmit={handleCandidateFormSubmit}
          isLoading={majorLoading || candidLoading || cvLoading}
        />
      </Skeleton>
    </Box>
  );
};

export default Profile;
