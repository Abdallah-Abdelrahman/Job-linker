import {
  Button,
  FormControl,
  FormLabel,
  Input,
  Box,
  Heading,
  Alert,
  AlertIcon,
  Spinner,
} from "@chakra-ui/react";
import { useLoginMutation } from "../../app/services/auth";
import { setCredentials } from "./authSlice";
import { useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";
import { useState } from "react";

function Login() {
  const [login, { isLoading, isError, isSuccess }] = useLoginMutation();
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  const handleSubmit = (evt) => {
    evt.preventDefault();
    if (!email || !password) {
      setErrorMessage("Please fill in all fields");
      return;
    }
    login({ email, password })
      .unwrap()
      .then((data) => {
        if (data.data.jwt) {
          dispatch(setCredentials(data));
          navigate("/@me");
        } else {
          setErrorMessage(data.message);
        }
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

  return (
    <Box className="w-full max-w-xl">
      <Heading as="h1" size="3xl" className="mb-8 capitalize">
        {" "}
        login{" "}
      </Heading>
      <form className="w-full flex flex-col gap-4" onSubmit={handleSubmit}>
        <FormControl isRequired>
          <FormLabel> Email </FormLabel>
          <Input
            type="email"
            name="email"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </FormControl>
        <FormControl isRequired>
          <FormLabel> Password </FormLabel>
          <Input
            type="password"
            name="password"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </FormControl>
        {errorMessage && (
          <Alert status="error">
            <AlertIcon />
            {errorMessage}
          </Alert>
        )}
        <Button
          width="full"
          mt={4}
          colorScheme="teal"
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
