import { useState } from 'react';
import { useSelector } from 'react-redux';
import {
  Button,
  FormControl,
  FormLabel,
  Input,
  Box,
  Heading,
  AlertIcon,
  Spinner,
} from '@chakra-ui/react';

import { useUpdateMeMutation } from '../../app/services/auth';
import { useUpdateCurrentCandidateMutation } from '../../app/services/candidate';
import { useUpdateCurrentRecruiterMutation } from '../../app/services/recruiter';

import { selectCurrentUser } from './authSlice';

function ProfileEdit() {
  const currentUser = useSelector(selectCurrentUser);
  const [updateCurrentUser] = useUpdateMeMutation;
  const [updateCandidate] = useUpdateCurrentCandidateMutation;
  const [updateRecruiter] = useUpdateCurrentRecruiterMutation;

  const [name, setName] = useState(currentUser.name);
  const [contactInfo, setContactInfo] = useState(currentUser.contact_info);
  const [bio, setBio] = useState(currentUser.bio);
  const [imageUrl, setImageUrl] = useState(currentUser.image_url);
  const [majorId, setMajorId] = useState(currentUser.candidate?.major_id);
  const [companyName, setCompanyName] = useState(
    currentUser.recruiter?.company_name,
  );
  const [companyInfo, setCompanyInfo] = useState(
    currentUser.recruiter?.company_info,
  );

  const handleSubmit = async (evt) => {
    evt.preventDefault();
    const userData = {
      name,
      contact_info: contactInfo,
      bio,
      image_url: imageUrl,
    };
    const candidateData = { major_id: majorId };
    const recruiterData = {
      company_name: companyName,
      company_info: companyInfo,
    };

    try {
      await updateCurrentUser(userData);
      if (currentUser.role === 'candidate') {
        await updateCandidate(candidateData);
      } else if (currentUser.role === 'recruiter') {
        await updateRecruiter(recruiterData);
      }
      alert('Profile updated successfully');
    } catch (err) {
      alert('An error occurred while updating the profile');
    }
  };

  return (
    <Box>
      <Heading>Edit Profile</Heading>
      <form onSubmit={handleSubmit}>
        {/* Fields for all users */}
        <FormControl>
          <FormLabel>Name</FormLabel>
          <Input value={name} onChange={(e) => setName(e.target.value)} />
        </FormControl>
        <FormControl>
          <FormLabel>Contact Info</FormLabel>
          <Input
            value={contactInfo}
            onChange={(e) => setContactInfo(e.target.value)}
          />
        </FormControl>
        <FormControl>
          <FormLabel>Bio</FormLabel>
          <Input value={bio} onChange={(e) => setBio(e.target.value)} />
        </FormControl>
        <FormControl>
          <FormLabel>Image URL</FormLabel>
          <Input
            value={imageUrl}
            onChange={(e) => setImageUrl(e.target.value)}
          />
        </FormControl>

        {/* Fields for candidates */}
        {currentUser.role === 'candidate' && (
          <FormControl>
            <FormLabel>Major ID</FormLabel>
            <Input
              value={majorId}
              onChange={(e) => setMajorId(e.target.value)}
            />
          </FormControl>
        )}

        {/* Fields for recruiters */}
        {currentUser.role === 'recruiter' && (
          <>
            <FormControl>
              <FormLabel>Company Name</FormLabel>
              <Input
                value={companyName}
                onChange={(e) => setCompanyName(e.target.value)}
              />
            </FormControl>
            <FormControl>
              <FormLabel>Company Info</FormLabel>
              <Input
                value={companyInfo}
                onChange={(e) => setCompanyInfo(e.target.value)}
              />
            </FormControl>
          </>
        )}

        <Button type="submit">Update Profile</Button>
      </form>
    </Box>
  );
}

export default ProfileEdit;
