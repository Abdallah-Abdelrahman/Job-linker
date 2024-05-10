import {
  NavLink,
  Outlet,
} from 'react-router-dom';
import { useRefresh } from '../hooks';
import { useAppDispatch, useAppSelector } from '../hooks/store';
import { selectCurrentUser, unsetCredentials } from '../features/auth/authSlice';
import { useLogoutMutation } from '../app/services/auth';
import Footer from './Footer';

function Layout() {
  const user = useAppSelector(selectCurrentUser);
  const dispatch = useAppDispatch();
  const [logout] = useLogoutMutation();
  const isAuthenticated = user.jwt || user.isRefreshed;
  // token refresher
  useRefresh();

  return (
    <>
      <header className='container mt-4 pt-4 border-t border-x bg-white rounded-lg'>
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
      <main className='w-full'>
        <Outlet />
      </main>
      <Footer />
    </>
  );
}

export default Layout;
