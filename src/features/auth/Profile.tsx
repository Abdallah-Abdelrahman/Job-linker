import { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';
import {
  Box,
  Heading,
  Text,
  Button,
  FormControl,
  FormLabel,
  Input,
  Select,
} from '@chakra-ui/react';
import { useMeQuery, useLazyMeQuery } from '../../app/services/auth';
import { useCreateCandidateMutation } from '../../app/services/candidate';
import { Recruiter, RecruiterResponse, useCreateRecruiterMutation } from '../../app/services/recruiter';
import { RootState } from '../../app/store';
import { college_majors } from '../../constants';
import { useAppSelector } from '../../hooks/store';
import { selectCurrentUser } from './authSlice';
import { useAfterRefreshQuery } from '../../hooks';
import { useCreateMajorMutation } from '../../app/services/major';

function MyForm({ onSubmit, role }) {
  const candidateJSX = (
    <FormControl isRequired>
      <FormLabel>Major ID:</FormLabel>
      <Select
        name='name'
      >
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
          type='text'
          name='company_name'
        />
      </FormControl>
      <FormControl isRequired>
        <FormLabel>Company Info:</FormLabel>
        <Input
          type='text'
          name='company_info'
        />
      </FormControl>
    </>
  );

  const handleSubmit = (evt) => {
    evt.preventDefault();
    const formData = new FormData(evt.currentTarget);
    onSubmit(Object.fromEntries(formData));
  };

  return (
    <form onSubmit={handleSubmit}>
      {role == 'candidate' ? candidateJSX : recruiterJSX}
      <Button type='submit'>Create Profile</Button>
    </form>
  );
}

// Profile component
const Profile = () => {
  // network request
  const { data: userData = { data: {} }, isLoading, error } = useAfterRefreshQuery(useMeQuery);
  const [createCandidate] = useCreateCandidateMutation();
  const [addMajor] = useCreateMajorMutation();
  const [createRecruiter] = useCreateRecruiterMutation();
  const { role } = useAppSelector(selectCurrentUser);


  console.log({ userData })
  // Handle form submissions
  const handleCandidateFormSubmit = async ({ name }) => {
    try {
      addMajor({ name }).unwrap()
        .then(data => {
          console.log('----Major---->', data)
          createCandidate({ user_id: userData.id, major_id: data.data.id })
            .unwrap()
            .then(data => console.log('-----Candidate---->', data))
            .catch(err => console.log({ err }))
        })
        .catch(err => console.error({err}));

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
    (error.message === 'User doesn\'t have a candidate profile' ||
      error.message === 'User doesn\'t have a recruiter profile');

  return (
    <Box>
      <Heading as='h1' size='3xl' className='mb-8 capitalize'>
        Profile
      </Heading>
      {userData && (
        <>
          <Text>Email: {userData.data.email}</Text>
          <Text>Role: {userData.data.role}</Text>
          {userData.data.role === 'candidate' && (
            <>
              {!userData.data.candidate ? (
                <MyForm role='candidate' onSubmit={handleCandidateFormSubmit} />
              ) : (
                <>
                  <Text>Major: {userData.data.candidate.major.name}</Text>
                  <Text>
                    Skills:{' '}
                    {userData.data.candidate.skills
                      .map((skill) => skill.name)
                      .join(', ')}
                  </Text>
                  <Text>
                    Languages:{' '}
                    {userData.data.candidate.languages
                      .map((language) => language.name)
                      .join(', ')}
                  </Text>
                  <Text>Experiences:</Text>
                  {userData.data.candidate.experiences.map(
                    (experience, index) => (
                      <Box key={index} p={5} shadow='md' borderWidth='1px'>
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
          {userData.data.role === 'recruiter' && (
            <>
              {!userData.data.recruiter ? (
                <MyForm role='recruiter' onSubmit={handleRecruiterFormSubmit} />
              ) : (
                <>
                  <Text>
                    Company Name: {userData.data.recruiter.company_name}
                  </Text>
                  <Text>
                    Company Info: {userData.data.recruiter.company_info}
                  </Text>
                  <Text>Jobs:</Text>
                  {!isLoading && userData.data.recruiter.jobs.map((job, index) => (
                    <Box key={index} p={5} shadow='md' borderWidth='1px'>
                      <Text>Title: {job.job_title}</Text>
                      <Text>Description: {job.job_description}</Text>
                      <Text>Location: {job.location}</Text>
                      <Text>Salary: {job.salary}</Text>
                      <Text>Skills: {job.skills.join(', ')}</Text>
                    </Box>
                  ))}
                </>
              )}
            </>
          )}
        </>
      )}
      {!userData && noProfileError && (
        <MyForm
          role={role}
          onSubmit={role == 'candidate'
            ? handleCandidateFormSubmit : handleRecruiterFormSubmit}
        />
      )}
    </Box>
  );
};

export default Profile;
