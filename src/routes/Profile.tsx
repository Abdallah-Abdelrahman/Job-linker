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
} & Record<'major' | 'company_email' | 'company_name' | 'company_address', string>;
const initialErrorState = {
  candidate: { file: false, major: false },
  recruiter: { company_name: false, company_email: false, company_address: false }
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
      return {
        ...state, candidate: { ...state.candidate, ...action.payload }
      };
    case 'recruiter':
      return {
        ...state, recruiter: { ...state.recruiter, ...action.payload }
      };
    default:
      return (state);
  }
};

function MyForm({ onSubmit, role, isLoading }) {
  const [formError, dispatch] = useReducer(reducer, initialErrorState);
  const recruiterJSX = (
    <>
      <FormControl isInvalid={formError.recruiter.company_name}>
        <Input
          placeholder='insert company name'
          type="text"
          name="company_name"
        />
      </FormControl>
      <FormControl isInvalid={formError.recruiter.company_email}>
        <Input
          placeholder='insert company email'
          type="text"
          name="company_email"
        />
      </FormControl>
      <FormControl isInvalid={formError.recruiter.company_address}>
        <Input
          placeholder='company address'
          type="text"
          name="company_address"
        />
      </FormControl>
    </>
  );
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


  const handleSubmit = (evt) => {
    const formdata = new FormData(evt.currentTarget);
    const { file, major, company_email, company_name, company_address }
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
        payload: {
          company_name: !(company_name),
          company_email: !(company_email),
          company_address: !(company_address),
        }
      });
      canSubmit = Boolean(company_name && company_address && company_email);
    }

    if (canSubmit) {
      console.log(Object.fromEntries(formdata))
      onSubmit(formdata);
    }

  };


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
  const [createRecruiter, { isSuccess: recruiterSuccess, isLoading: recLoading }] =
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
    createRecruiter()
      .unwrap()
      .then(_ => updateUser({ contact_info: Object.fromEntries(formdata) }))
      .catch((error) => {
        console.error(error);
      })
  };

  const noProfileError =
    error &&
    (error.message === "User doesn't have a candidate profile" ||
      error.message === "User doesn't have a recruiter profile");

  console.log({ userData });
  if (role == 'candidate' && isSuccess && userData.data.profile_complete)
    return (<Candidate data={userData.data} />);

  return (
    <Box className='mx-auto max-w-2xl my-8'>
      <Skeleton isLoaded={!isLoading}>
        <Heading as="h2" size="xl" className="mb-8 capitalize">
          complete your Profile
        </Heading>
        <MyForm
          role={role}
          onSubmit={handleRecruiterFormSubmit}
          isLoading={recLoading}
        />
      </Skeleton>
    </Box>
  );
};

export default Profile;
