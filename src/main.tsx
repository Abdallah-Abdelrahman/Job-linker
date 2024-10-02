import React from 'react';
import ReactDOM from 'react-dom/client';
import { RouterProvider } from 'react-router-dom';
import { Provider } from 'react-redux';
import { store } from './app/store.ts';
import { ChakraProvider } from '@chakra-ui/react';
import {
  Route,
  createBrowserRouter,
  createRoutesFromElements,
} from 'react-router-dom';
import { ErrorPage, Layout, Private } from './components';
import { Verify, Register, Login, Profile, Home, Explore } from './routes';
import './index.css';
import { Job } from './components/job';
import { Candidate } from './components/profile';

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route path="/" element={<Layout />} errorElement={<ErrorPage />}>
      <Route index element={<Home />} />
      <Route path="find_jobs" element={<Explore />}>
        <Route path=":job_id" element={<Job />} />
      </Route>
      <Route path="signup" element={<Register />} />
      <Route path="login" element={<Login />} />
      <Route path="verify" element={<Verify />} />
      <Route element={<Private />}>
        <Route
          path="jobs/applied_candidates/:id"
          element={<Candidate as="recruiter" />}
        />
        <Route path="@me" element={<Profile />}>
          <Route path="jobs/:job_id" element={<Job />} />
        </Route>
      </Route>
      <Route path="*" element={<ErrorPage />} />
    </Route>,
  ),
);

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <Provider store={store}>
      <ChakraProvider>
        <RouterProvider router={router} />
      </ChakraProvider>
    </Provider>
  </React.StrictMode>,
);
