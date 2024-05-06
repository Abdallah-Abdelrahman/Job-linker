import {
  Button,
  FormControl,
  FormLabel,
  Input,
  Box,
  Heading,
  Text
} from '@chakra-ui/react';
import { useLoginMutation } from '../../app/services/auth';
import { selectCurrentUser, setCredentials } from './authSlice';
import { Link, useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { useEffect } from 'react';
import { useAppSelector } from '../../hooks/store';

function Login() {
  const [login, { isLoading, isError, isSuccess }] = useLoginMutation();
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const user = useAppSelector(selectCurrentUser);

  const handleSubmit = (evt) => {
    evt.preventDefault();
    const form = new FormData(evt.currentTarget);
    login(Object.fromEntries(form))
      .unwrap()
      .then(({ data }) => {
        if (data.jwt) {
          dispatch(setCredentials({ ...data, isRefreshed: true }));
          navigate('/@me');
        } else {
          console.log(data.message);
        }
      })
      .catch((err) => console.error({ err }));
  };

  // redirect the user to thier profile if logged-in
  useEffect(() => {
    if (user.jwt || user.isRefreshed) {
      navigate('/@me');
    }

  }, [user, navigate]);

  return (
    <Box className='w-full max-w-xl'>
      <Heading as='h1' size='3xl' className='mb-8 capitalize'>
        {' '}
        login{' '}
      </Heading>
      <form className='w-full flex flex-col gap-4' onSubmit={handleSubmit}>
        <FormControl isRequired>
          <FormLabel> Email </FormLabel>
          <Input type='email' name='email' placeholder='Enter your email' />
        </FormControl>
        <FormControl isRequired>
          <FormLabel> Password </FormLabel>
          <Input
            type='password'
            name='password'
            placeholder='Enter your password'
          />
        </FormControl>
        <Text as='p'>don't have an acount ?
          <Link to='/signup' className='mx-2 text-teal-500'>signup</Link>
        </Text>
        <Button width='full' mt={4} colorScheme='teal' type='submit'>
          Login
        </Button>
      </form>
    </Box>
  );
}

export default Login;
