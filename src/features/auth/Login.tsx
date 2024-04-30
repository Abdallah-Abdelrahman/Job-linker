import { Button, FormControl, FormLabel, Input, Select, Box, Heading } from '@chakra-ui/react';
import { useLoginMutation } from '../../app/services/auth';

function Login() {
  const [login, { isLoading, isError, isSuccess }] = useLoginMutation();

  const handleSubmit = (evt) => {
    evt.preventDefault();
    const form = new FormData(evt.currentTarget);
    console.log(Object.fromEntries(form))
    //login(Object.fromEntries(form))
    //  .unwrap()
    //  .then(data => console.log({ data }))
    //  .catch(err => console.error({ err }))

  }

  return (

    <Box className='w-full max-w-xl'>
    <Heading as='h1' size='3xl' className='mb-8 capitalize'> login </Heading>
      <form className='w-full flex flex-col gap-4' onSubmit={handleSubmit}>
        <FormControl isRequired>
          <FormLabel> Email </FormLabel>
          <Input type='email' name='email' placeholder='Enter your email' />
        </FormControl>
        <FormControl isRequired>
          <FormLabel> Password </FormLabel>
          <Input type='password' name='password' placeholder='Enter your password' />
        </FormControl>
        <Button width='full' mt={4} colorScheme='teal' type='submit'>Login</Button>
      </form>
    </Box>
  );
}

export default Login;
