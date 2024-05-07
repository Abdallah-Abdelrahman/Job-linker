import {
  NavLink,
  Outlet,
} from 'react-router-dom';
import { useRefresh } from '../hooks';
import { MyIcon } from '../components';
import { useAppDispatch, useAppSelector } from '../hooks/store';
import { selectCurrentUser, unsetCredentials } from '../features/auth/authSlice';
import { useLogoutMutation } from '../app/services/auth';

function Layout() {
  const user = useAppSelector(selectCurrentUser);
  const dispatch = useAppDispatch();
  const [logout] = useLogoutMutation();
  const isAuthenticated = user.jwt || user.isRefreshed;
  // token refresher
  useRefresh();

  return (
    <>
      <header className='w-full pt-4 shadow-md rounded-md'>
        <nav className='nav flex justify-center gap-4 md:gap-10'>
          <NavLink className='py-3 px-4 md:px-5' to='/'>
            home
          </NavLink>
          {isAuthenticated && <NavLink className='py-3 px-5' to='@me'>
            profile
          </NavLink>
          }
          <NavLink
            className='py-3 px-4 md:px-5'
            to={isAuthenticated ? 'logout' : 'login'}
            onClick={() => {
              if (isAuthenticated) {
                logout()
                  .unwrap()
                  .then(_ => {
                    dispatch(unsetCredentials())
                  })
                  .catch(err => console.error({ err }))
              }
            }}
          >
            {isAuthenticated ? 'logout' : 'login'}
          </NavLink>
        </nav>
      </header>
      <main className='w-full flex justify-center'>
        <Outlet />
      </main>
      <footer className='footer relative z-10 w-full flex justify-center items-end mt-auto'>
        <MyIcon
          href='sprite.svg#wave-down'
          viewBox='0 0 1440 320'
          className='absolute left-0 right-0 -bottom-4 -z-10'
        />
        Joblinker &copy; 2024
      </footer>
    </>
  );
}

export default Layout;
