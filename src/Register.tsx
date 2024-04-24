// Register.tsx
import React, { useState } from "react";
import { registerUser } from "./api";

const Register = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("");

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    const data = await registerUser(name, email, password, role);
    console.log(data);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Name"
      />
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
      />
      <select value={role} onChange={(e) => setRole(e.target.value)}>
        <option value="">Select role</option>
        <option value="candidate">Candidate</option>
        <option value="recruiter">Recruiter</option>
      </select>
      <button type="submit">Register</button>
    </form>
  );
};

export default Register;
