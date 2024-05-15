import { NavLink } from 'react-router-dom';
import { useAppDispatch, useAppSelector } from '../hooks/store';
import { useLogoutMutation } from '../app/services/auth';
import { useRefresh } from '../hooks';
import { selectCurrentUser } from '../features/auth';
import { unsetCredentials } from '../features/auth/authSlice';

function Header() {
  const user = useAppSelector(selectCurrentUser);
  const dispatch = useAppDispatch();
  const [logout] = useLogoutMutation();
  const isAuthenticated = user.jwt || user.isRefreshed;
  // token refresher
  useRefresh();

  // TODO: logout should be a button not a page
  return (
    <header className='container mx-auto mt-4 pt-4 border-t border-x bg-white rounded-lg'>
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
                  dispatch(unsetCredentials());
                })
                .catch(err => console.error({ err }));
            }
          }}
        >
          {isAuthenticated ? 'logout' : 'login'}
        </NavLink>
      </nav>
    </header>

  );
}

export default Header;
