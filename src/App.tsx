import { Register } from './features/auth';
import { Login } from './features/auth';
import { NavLink, Outlet, Route, createBrowserRouter, createRoutesFromElements } from 'react-router-dom';
import Verify from './features/auth/Verify';
import { useMeQuery } from './app/services/auth';
import { Upload } from './components';
import { useAfterRefreshQuery, useRefresh } from './hooks';
import './App.css';

const App = () => {
  return (
    <div className='App'>
      <h1>Job Linker</h1>
    </div>
  );
};


function Me() {
  // refresh token request
  const { data, isSuccess } = useAfterRefreshQuery(useMeQuery);

  return (
    <main className='flex flex-col'>
      {/* TODO: Complete registeration for user (candiate | recruiter)*/}
      <h1>me</h1>
      {/*<Upload />*/}
    </main>
  );
}

function Layout() {

  // token refresher
  useRefresh();

  return (
    <div className='w-full h-full p-4 flex flex-col items-center'>
      <header className='w-full pt-4 shadow-md rounded-md' >
        <nav className='nav flex justify-center gap-4 md:gap-10'>
          <NavLink className='py-3 px-4 md:px-5' to='/'> home </NavLink>
          <NavLink className='py-3 px-4 md:px-5' to='login'>login</NavLink>
          <NavLink className='py-3 px-4 md:px-5' to='signup'>signup</NavLink>
          {/* TODO: private route*/}
          <NavLink className='py-3 px-5' to='@me'>profile</NavLink>
        </nav>
      </header>
      <main className='w-full m-auto flex justify-center'>
        <Outlet />
      </main>
      <footer className='mt-auto'>ATS &copy; mohanad & abdallah</footer>

    </div>
  )
}

export const router = createBrowserRouter(createRoutesFromElements(
  <Route path='/' element={<Layout />}>
    <Route index element={<App />} />
    <Route path='signup' element={<Register />} />
    <Route path='login' element={<Login />} />
    <Route path='verify' element={<Verify />} />
    <Route path='@me' element={<Me />} />
  </Route>
));

export default App;
