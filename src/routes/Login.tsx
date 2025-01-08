import {
  Button,
  FormControl,
  FormLabel,
  Input,
  Box,
  Heading,
  Alert,
  AlertIcon,
  Text,
  InputLeftElement,
  Icon,
  InputGroup
} from '@chakra-ui/react';
import { useLoginMutation } from '../app/services/auth';
import { NavLink, useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { useState, useEffect } from 'react';
import { useAppSelector } from '../hooks/store';
import { selectCurrentUser, setCredentials } from '../features/auth';
import { MyIcon } from '../components';

function Login() {
  const [login, { isLoading }] = useLoginMutation();
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const user = useAppSelector(selectCurrentUser);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const handleSubmit = (evt) => {
    evt.preventDefault();
    if (!email || !password) {
      setErrorMessage('Please fill in all fields');
      return;
    }
    login({ email, password })
      .unwrap()
      .then(({ data }) => {
        if (data.jwt) {
          dispatch(setCredentials({ ...data, isRefreshed: true }));
          navigate('/@me');
        } else {
          setErrorMessage(data.message);
        }
      })
      .catch((err) => {
        let actualErrorMessage = err.data?.message || 'An error occurred';
        try {
          // Attempt to parse the error message
          const errorData = JSON.parse(err.data.message.replace(/'/g, '"'));
          actualErrorMessage = Object.values(errorData)[0][0];
        } catch (error) {
          // If parsing fails, do nothing and use the original error message
        }
        setErrorMessage(actualErrorMessage);
      });
  };

  // redirect the user to thier profile if already logged-in
  useEffect(() => {
    if (user.jwt || user.isRefreshed) {
      navigate('/@me');
    }
  }, [user, navigate]);

  return (
    <Box className="containter grid mx-auto my-8 flex-1">
      <Heading
        as="h1"
        size="3xl"
        className="mb-8 max-w-md w-full mx-auto capitalize"
      >
        login
      </Heading>

      <form
        className="max-w-md w-full mx-auto p-6 flex flex-col gap-4 bg-white shadow-lg rounded-lg"
        onSubmit={handleSubmit}
      >
        <InputGroup>
          <InputLeftElement pointerEvents="none">
            <MyIcon
              href="/sprite.svg#email-address"
              className="w-6 h-6 fill-sky-600"
            />
          </InputLeftElement>
          <Input
            required
            type="email"
            name="email"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </InputGroup>
        <InputGroup>
          <InputLeftElement pointerEvents="none">
            <MyIcon
              href="/sprite.svg#password"
              className="w-6 h-6 fill-sky-600"
            />
          </InputLeftElement>
          <Input
            required
            type="password"
            name="password"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </InputGroup>
        {errorMessage && (
          <Alert status="error">
            <AlertIcon />
            {errorMessage}
          </Alert>
        )}
        <Text>
          Dont't have an acount?
          <NavLink to="/signup" className="text-sky-600 mx-2">
            register
          </NavLink>
        </Text>
        <Button
          className="w-max !bg-sky-500 !text-sky-50"
          type="submit"
          isLoading={isLoading}
        >
          Login
        </Button>
      </form>
    </Box>
  );
}

export default Login;
