import { useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import {
  Box,
  Heading,
  Text,
  Button,
  FormControl,
  FormLabel,
  Input,
} from "@chakra-ui/react";
import { useMeQuery } from "../../app/services/auth";
import { useCreateCandidateMutation } from "../../app/services/candidate";
import { useCreateRecruiterMutation } from "../../app/services/recruiter";
import { RootState } from "../../app/store";
import { Select } from "@chakra-ui/react";
import { college_majors } from "../../constants";

function Profile() {
  const { data: userData, error: userError } = useMeQuery();
  const [createCandidate, { isLoading: isCreatingCandidate }] =
    useCreateCandidateMutation();
  const [createRecruiter, { isLoading: isCreatingRecruiter }] =
    useCreateRecruiterMutation();
  const role = useSelector((state: RootState) => state.auth.user?.role);
  const dispatch = useDispatch();

  // State for the forms
  const [candidateForm, setCandidateForm] = useState({ major_id: "" });
  const [recruiterForm, setRecruiterForm] = useState({
    company_name: "",
    company_info: "",
  });

  // Handle form changes
  const handleCandidateFormChange = (e) =>
    setCandidateForm({ ...candidateForm, [e.target.name]: e.target.value });
  const handleRecruiterFormChange = (e) =>
    setRecruiterForm({ ...recruiterForm, [e.target.name]: e.target.value });

  // Handle form submissions
  const handleCandidateFormSubmit = (e) => {
    e.preventDefault();
    createCandidate({ user_id: userData.id, major_id: candidateForm.major_id });
  };
  const handleRecruiterFormSubmit = (e) => {
    e.preventDefault();
    createRecruiter({ user_id: userData.id, ...recruiterForm });
  };

  if (userError) {
    return <Text>Error: {userError.message}</Text>;
  }

  if (isCreatingCandidate || isCreatingRecruiter) {
    return <Text>Creating profile...</Text>;
  }

  return (
    <Box className="w-full max-w-xl">
      <Heading as="h1" size="3xl" className="mb-8 capitalize">
        Profile
      </Heading>
      {userData && (
        <>
          <Text>Email: {userData.data.email}</Text>
          <Text>Role: {userData.data.role}</Text>
          {!userData.candidate && userData.data.role === "candidate" && (
            <form onSubmit={handleCandidateFormSubmit}>
              <FormControl isRequired>
                <FormLabel>Major ID:</FormLabel>
                <Select
                  name="major_id"
                  value={candidateForm.major_id}
                  onChange={handleCandidateFormChange}
                >
                  {college_majors.map((major) => (
                    <option key={major} value={major}>
                      {major}
                    </option>
                  ))}
                </Select>
              </FormControl>
              <Button type="submit">Create Candidate Profile</Button>
            </form>
          )}
          {!userData.recruiter && userData.data.role === "recruiter" && (
            <form onSubmit={handleRecruiterFormSubmit}>
              <FormControl isRequired>
                <FormLabel>Company Name:</FormLabel>
                <Input
                  type="text"
                  name="company_name"
                  value={recruiterForm.company_name}
                  onChange={handleRecruiterFormChange}
                />
              </FormControl>
              <FormControl isRequired>
                <FormLabel>Company Info:</FormLabel>
                <Input
                  type="text"
                  name="company_info"
                  value={recruiterForm.company_info}
                  onChange={handleRecruiterFormChange}
                />
              </FormControl>
              <Button type="submit">Create Recruiter Profile</Button>
            </form>
          )}
          {userData.candidate && (
            <>
              <Text>Major: {userData.candidate.major}</Text>
              <Text>Skills: {userData.candidate.skills.join(", ")}</Text>
              <Text>Languages: {userData.candidate.languages.join(", ")}</Text>
            </>
          )}
          {userData.recruiter && (
            <>
              <Text>Company Name: {userData.recruiter.company_name}</Text>
              <Text>Company Info: {userData.recruiter.company_info}</Text>
            </>
          )}
        </>
      )}
    </Box>
  );
}

export default Profile;
