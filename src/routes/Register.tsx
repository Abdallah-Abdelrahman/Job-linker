import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Button,
  FormControl,
  FormLabel,
  Input,
  Select,
  Box,
  Heading,
  Alert,
  AlertIcon,
} from "@chakra-ui/react";
import { useRegisterMutation } from "../app/services/auth";

function Register() {
  const [signup, { isLoading }] = useRegisterMutation();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [role, setRole] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  const navigate = useNavigate();

  const handleSubmit = (evt) => {
    evt.preventDefault();
    if (!email || !password || !name || !role) {
      setErrorMessage("Please fill in all fields");
      return;
    }
    signup({ email, password, name, role })
      .unwrap()
      .then((data) => {
        console.log({ data });
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

  return (
    <Box className="w-full max-w-xl">
      <Heading as="h1" size="3xl" className="mb-8">
        {" "}
        Signup{" "}
      </Heading>
      <form className="w-full flex flex-col gap-4" onSubmit={handleSubmit}>
        <FormControl isRequired>
          <FormLabel> Name </FormLabel>
          <Input
            type="text"
            name="name"
            placeholder="Enter your username"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        </FormControl>
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
        <FormControl isRequired>
          <FormLabel> Role </FormLabel>
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
          width="full"
          mt={4}
          colorScheme="teal"
          type="submit"
          isLoading={isLoading}
        >
          Register
        </Button>
      </form>
    </Box>
  );
}

export default Register;
