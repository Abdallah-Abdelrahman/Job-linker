import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
  Button,
  FormControl,
  Input,
  Select,
  Box,
  Heading,
  Alert,
  AlertIcon,
  InputGroup,
  InputLeftElement,
  Text
} from "@chakra-ui/react";
import { useRegisterMutation } from "../app/services/auth";
import { MyIcon } from "../components";
import { useAppSelector } from "../hooks/store";
import { selectCurrentUser } from "../features/auth";

function Register() {
  const [signup, { isLoading }] = useRegisterMutation();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [role, setRole] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate();
  const user = useAppSelector(selectCurrentUser);

  const handleSubmit = (evt) => {
    evt.preventDefault();
    if (!email || !password || !name || !role) {
      setErrorMessage("Please fill in all fields");
      return;
    }
    signup({ email, password, name, role })
      .unwrap()
      .then((data) => {
        navigate("/login");
      })
      .catch((err) => {
        let actualErrorMessage = err.data?.message || "An error occurred";
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
    <Box className="containter mx-auto my-8 flex-1">
      <Heading as="h1" size="3xl" className="mb-8 max-w-md w-full mx-auto capitalize">
        Register
      </Heading>
      <form className="max-w-md w-full mx-auto p-6 flex flex-col gap-4 bg-white shadow-lg rounded-lg" onSubmit={handleSubmit}>
        <InputGroup>
          <InputLeftElement>
            <MyIcon
              href='/sprite.svg#username'
              className='w-6 h-6 fill-sky-500'
            />
          </InputLeftElement>
          <Input
            required
            type="text"
            name="name"
            placeholder="Enter your username"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        </InputGroup>
        <InputGroup>
          <InputLeftElement>
            <MyIcon
              href='/sprite.svg#email-address'
              className='w-6 h-6 fill-sky-500'
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
          <InputLeftElement>
            <MyIcon href='/sprite.svg#password' className='w-6 h-6 fill-sky-500' />
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
        <FormControl isRequired>
          <Select
            name="role"
            placeholder="Select role"
            value={role}
            onChange={(e) => setRole(e.target.value)}
          >
            <option value="candidate">Candidate</option>
            <option value="recruiter">Recruiter</option>
          </Select>
        </FormControl>
        {errorMessage && (
          <Alert status="error">
            <AlertIcon />
            {errorMessage}
          </Alert>
        )}
        <Button
          type="submit"
          className='w-max !bg-sky-500 !text-sky-50'
          isLoading={isLoading}
        >
          Register
        </Button>
        <Text className='flex gap-1'>
          have an account?
          <Link
            to='/login'
            className='text-sky-600'
            children=' sign in'
          />
        </Text>
      </form>
    </Box>
  );
}

export default Register;
