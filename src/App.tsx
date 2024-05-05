import { Register } from './features/auth';
import { Login } from './features/auth';
import { Profile } from './features/auth';
import {
  NavLink,
  Outlet,
  Route,
  createBrowserRouter,
  createRoutesFromElements,
} from 'react-router-dom';
import Verify from './features/auth/Verify';
import './App.css';
import { useRefresh } from './hooks';
import { MyIcon } from './components';

const App = () => {
  return (
    <div className='App'>
      <h1>Job Linker</h1>
    </div>
  );
};

function Layout() {
  // token refresher
  useRefresh();

  return (
    <div className='w-full h-full p-4 flex flex-col items-center'>
      <header className='w-full pt-4 shadow-md rounded-md'>
        <nav className='nav flex justify-center gap-4 md:gap-10'>
          <NavLink className='py-3 px-4 md:px-5' to='/'>
            {' '}
            home{' '}
          </NavLink>
          <NavLink className='py-3 px-4 md:px-5' to='login'>
            login
          </NavLink>
          <NavLink className='py-3 px-4 md:px-5' to='signup'>
            signup
          </NavLink>
          {/* TODO: private route*/}
          <NavLink className='py-3 px-5' to='@me'>
            profile
          </NavLink>
        </nav>
      </header>
      <main className='w-full m-auto flex justify-center'>
        <Outlet />
      </main>
      <footer className='footer relative z-10 w-full flex justify-center items-end mt-auto'>
        <MyIcon
          href='sprite.svg#wave-down'
          viewBox='0 0 1440 320'
          className='absolute left-0 right-0 -bottom-4 -z-10'
        />
        ATS &copy; mohanad & abdallah
      </footer>
    </div>
  );
}

export const router = createBrowserRouter(
  createRoutesFromElements(
    <Route path='/' element={<Layout />}>
      <Route index element={<App />} />
      <Route path='signup' element={<Register />} />
      <Route path='login' element={<Login />} />
      <Route path='verify' element={<Verify />} />
      <Route path='@me' element={<Profile />} />
    </Route>,
  ),
);

export default App;
