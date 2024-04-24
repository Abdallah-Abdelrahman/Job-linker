import axios from "axios";

const API_URL = "http://localhost:5000";

export const getCurrentUser = async () => {
  const response = await axios.get(`${API_URL}/@me`);
  return response.data;
};

export const registerUser = async (
  name: string,
  email: string,
  password: string,
  role: string,
) => {
  const response = await axios.post(`${API_URL}/register`, {
    name,
    email,
    password,
    role,
  });
  return response.data;
};

export const loginUser = async (email: string, password: string) => {
  const response = await axios.post(`${API_URL}/login`, { email, password });
  return response.data;
};

export const logoutUser = async () => {
  const response = await axios.post(`${API_URL}/logout`);
  return response.data;
};
