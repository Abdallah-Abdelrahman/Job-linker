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
import { Verify, Register, Login, Profile, Home } from './routes';
import './index.css';

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route path='/' element={<Layout />} errorElement={<ErrorPage />}>
      <Route index element={<Home />} />
      <Route path='signup' element={<Register />} />
      <Route path='login' element={<Login />} />
      <Route path='verify' element={<Verify />} />
      <Route element={<Private />}>
        <Route path='@me' element={<Profile />} />
      </Route>
    </Route>
  ),
);

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <Provider store={store}>
      <ChakraProvider>
        <RouterProvider router={router} />
      </ChakraProvider>
    </Provider>
  </React.StrictMode>
);
