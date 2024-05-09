import { useState } from "react";
import {
  Box,
  Heading,
  Text,
  Button,
  FormControl,
  FormLabel,
  Input,
  Select,
  Spinner,
  Alert,
  AlertIcon,
} from "@chakra-ui/react";
import { User, useMeQuery } from "../app/services/auth";
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

function MyForm({ onSubmit, role }) {
  const [formData, setFormData] = useState({
    name: "",
    company_name: "",
    company_info: "",
  });
  const [formError, setFormError] = useState(null);

  const validateForm = () => {
    if (role === "candidate" && !formData.name) {
      setFormError("Major is required");
      return false;
    }
    if (
      role === "recruiter" &&
      (!formData.company_name || !formData.company_info)
    ) {
      setFormError("Company Name and Company Info are required");
      return false;
    }
    setFormError(null);
    return true;
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (evt) => {
    evt.preventDefault();
    if (validateForm()) {
      onSubmit(formData);
    }
  };

  const candidateJSX = (
    <FormControl isRequired>
      <FormLabel>Major ID:</FormLabel>
      <Select name="name" value={formData.name} onChange={handleChange}>
        {college_majors.map((major) => (
          <option key={major} value={major}>
            {major}
          </option>
        ))}
      </Select>
    </FormControl>
  );

  const recruiterJSX = (
    <>
      <FormControl>
        <FormLabel>Company Name:</FormLabel>
        <Input
          type="text"
          name="company_name"
          value={formData.company_name}
          onChange={handleChange}
        />
      </FormControl>
      <FormControl isRequired>
        <FormLabel>Company Info:</FormLabel>
        <Input
          type="text"
          name="company_info"
          value={formData.company_info}
          onChange={handleChange}
        />
      </FormControl>
    </>
  );

  return (
    <form onSubmit={handleSubmit}>
      {formError && (
        <Alert status="error">
          <AlertIcon />
          {formError}
        </Alert>
      )}
      {role == "candidate" ? candidateJSX : recruiterJSX}
      <Button type="submit">Create Profile</Button>
    </form>
  );
}

// Profile component
const Profile = () => {
  // network request
  const {
    data: userData = { data: {} },
    isLoading, isSuccess,
    error,
  } = useAfterRefreshQuery<{ data: User }>(useMeQuery);

  const [createCandidate, { isSuccess: candidateSuccess }] =
    useCreateCandidateMutation();
  const [addMajor] = useCreateMajorMutation();
  const [createRecruiter, { isSuccess: recruiterSuccess }] =
    useCreateRecruiterMutation();
  const { role } = useAppSelector(selectCurrentUser);

  const handleCandidateFormSubmit = async ({ name }) => {
    try {
      addMajor({ name })
        .unwrap()
        .then((data) => {
          createCandidate({ user_id: userData.id, major_id: data.data.id })
            .unwrap()
            .catch((err) => console.log({ err }));
        })
        .catch((err) => console.error({ err }));
    } catch (error) {
      console.error(error);
    }
  };

  const handleRecruiterFormSubmit = async (formData: Recruiter) => {
    try {
      await createRecruiter({ user_id: userData.id, ...formData });
    } catch (error) {
      console.error(error);
    }
  };

  const noProfileError =
    error &&
    (error.message === "User doesn't have a candidate profile" ||
      error.message === "User doesn't have a recruiter profile");


  return (
    <Box className='flex-1 mt-8 containter mx-atuo border-2 border-red-500'>
      <Heading as="h2" size="xl" className="mb-8 capitalize">
        complete your Profile
      </Heading>
    </Box>
  );

};

export default Profile;
