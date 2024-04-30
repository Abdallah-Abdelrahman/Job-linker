import { Button, FormControl, FormLabel, Input, Select, Box, Heading } from '@chakra-ui/react';
import { useRegisterMutation } from '../../app/services/auth';

function Register() {
  const [signup, { isLoading, isError, isSuccess }] = useRegisterMutation();

  const handleSubmit = (evt) => {
    evt.preventDefault();
    const form = new FormData(evt.currentTarget);
    console.log(Object.fromEntries(form))
    //signup(Object.fromEntries(form))
    //  .unwrap()
    //  .then(data => console.log({ data }))
    //  .catch(err => console.error({ err }))

  }

  return (

    <Box className='w-full'>
    <Heading as='h1' size='3xl' noOfLines={1} className='mb-8'> Signup </Heading>
      <form className='w-full flex flex-col gap-4' onSubmit={handleSubmit}>
        <FormControl isRequired>
          <FormLabel> Name </FormLabel>
          <Input type='text' name='name' placeholder='Enter your username' />
        </FormControl>
        <FormControl isRequired>
          <FormLabel> Email </FormLabel>
          <Input type='email' name='email' placeholder='Enter your email' />
        </FormControl>
        <FormControl isRequired>
          <FormLabel> Password </FormLabel>
          <Input type='password' name='password' placeholder='Enter your password' />
        </FormControl>
        <FormControl isRequired>
          <FormLabel> Role </FormLabel>
          <Select name='role' placeholder='Select role'>
            <option value='candidate'>Candidate</option>
            <option value='recruiter'>Recruiter</option>
          </Select>
        </FormControl>
        <Button width='full' mt={4} colorScheme='teal' type='submit'>Register</Button>
      </form>
    </Box>
  );
}

export default Register;
