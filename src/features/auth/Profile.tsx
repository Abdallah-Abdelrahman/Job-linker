import { useState, useEffect } from "react";
import { useSelector } from "react-redux";
import {
  Box,
  Heading,
  Text,
  Button,
  FormControl,
  FormLabel,
  Input,
  Select,
} from "@chakra-ui/react";
import { useMeQuery, useLazyMeQuery } from "../../app/services/auth";
import { useCreateCandidateMutation } from "../../app/services/candidate";
import { useCreateRecruiterMutation } from "../../app/services/recruiter";
import { RootState } from "../../app/store";
import { college_majors } from "../../constants";

// Candidate form component
const CandidateForm = ({ onSubmit }) => {
  const [major_id, setMajorId] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(major_id);
  };

  return (
    <form onSubmit={handleSubmit}>
      <FormControl isRequired>
        <FormLabel>Major ID:</FormLabel>
        <Select
          name="major_id"
          value={major_id}
          onChange={(e) => setMajorId(e.target.value)}
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
  );
};

// Recruiter form component
const RecruiterForm = ({ onSubmit }) => {
  const [company_name, setCompanyName] = useState("");
  const [company_info, setCompanyInfo] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({ company_name, company_info });
  };

  return (
    <form onSubmit={handleSubmit}>
      <FormControl isRequired>
        <FormLabel>Company Name:</FormLabel>
        <Input
          type="text"
          name="company_name"
          value={company_name}
          onChange={(e) => setCompanyName(e.target.value)}
        />
      </FormControl>
      <FormControl isRequired>
        <FormLabel>Company Info:</FormLabel>
        <Input
          type="text"
          name="company_info"
          value={company_info}
          onChange={(e) => setCompanyInfo(e.target.value)}
        />
      </FormControl>
      <Button type="submit">Create Recruiter Profile</Button>
    </form>
  );
};

// Profile component
const Profile = () => {
  const [fetchMe, { data: userData, isLoading, error }] = useLazyMeQuery();
  const [createCandidate] = useCreateCandidateMutation();
  const [createRecruiter] = useCreateRecruiterMutation();
  const role = useSelector((state: RootState) => state.auth.user?.role);

  // Refetch user data when the role changes
  useEffect(() => {
    fetchMe();
  }, [fetchMe]);

  // Handle form submissions
  const handleCandidateFormSubmit = async (major_id) => {
    try {
      await createCandidate({ user_id: userData.id, major_id });
    } catch (error) {
      console.error(error);
    }
  };

  const handleRecruiterFormSubmit = async (formData) => {
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
    <Box>
      <Heading as="h1" size="3xl" className="mb-8 capitalize">
        Profile
      </Heading>
      {userData && (
        <>
          <Text>Email: {userData.data.email}</Text>
          <Text>Role: {userData.data.role}</Text>
          {userData.data.role === "candidate" && (
            <>
              {!userData.data.candidate ? (
                <CandidateForm onSubmit={handleCandidateFormSubmit} />
              ) : (
                <>
                  <Text>Major: {userData.data.candidate.major.name}</Text>
                  <Text>
                    Skills:{" "}
                    {userData.data.candidate.skills
                      .map((skill) => skill.name)
                      .join(", ")}
                  </Text>
                  <Text>
                    Languages:{" "}
                    {userData.data.candidate.languages
                      .map((language) => language.name)
                      .join(", ")}
                  </Text>
                  <Text>Experiences:</Text>
                  {userData.data.candidate.experiences.map(
                    (experience, index) => (
                      <Box key={index} p={5} shadow="md" borderWidth="1px">
                        <Text>Company: {experience.company}</Text>
                        <Text>Title: {experience.title}</Text>
                        <Text>Description: {experience.description}</Text>
                        <Text>Location: {experience.location}</Text>
                        <Text>Start Date: {experience.start_date}</Text>
                        <Text>End Date: {experience.end_date}</Text>
                      </Box>
                    ),
                  )}
                </>
              )}
            </>
          )}
          {userData.data.role === "recruiter" && (
            <>
              {!userData.data.recruiter ? (
                <RecruiterForm onSubmit={handleRecruiterFormSubmit} />
              ) : (
                <>
                  <Text>
                    Company Name: {userData.data.recruiter.company_name}
                  </Text>
                  <Text>
                    Company Info: {userData.data.recruiter.company_info}
                  </Text>
                  <Text>Jobs:</Text>
                  {userData.data.recruiter.jobs.map((job, index) => (
                    <Box key={index} p={5} shadow="md" borderWidth="1px">
                      <Text>Title: {job.job_title}</Text>
                      <Text>Description: {job.job_description}</Text>
                      <Text>Location: {job.location}</Text>
                      <Text>Salary: {job.salary}</Text>
                      <Text>Skills: {job.skills.join(", ")}</Text>
                    </Box>
                  ))}
                </>
              )}
            </>
          )}
        </>
      )}
      {!userData && noProfileError && (
        <>
          {role === "candidate" && (
            <CandidateForm onSubmit={handleCandidateFormSubmit} />
          )}
          {role === "recruiter" && (
            <RecruiterForm onSubmit={handleRecruiterFormSubmit} />
          )}
        </>
      )}
    </Box>
  );
};

export default Profile;
