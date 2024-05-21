import { Link, NavLink, useNavigate } from 'react-router-dom';
import { useAppDispatch, useAppSelector } from '../hooks/store';
import { useLogoutMutation } from '../app/services/auth';
import { useRefresh } from '../hooks';
import { selectCurrentUser } from '../features/auth';
import { unsetCredentials } from '../features/auth/authSlice';
import { Box, IconButton, Menu, MenuButton, MenuItem, MenuList } from '@chakra-ui/react';
import MyIcon from './Icon';
import logo from '../assets/logo.png';

function Header() {
  const user = useAppSelector(selectCurrentUser);
  const dispatch = useAppDispatch();
  const [logout] = useLogoutMutation();
  const navigate = useNavigate();
  const isAuthenticated = user.jwt || user.isRefreshed;
  // token refresher
  useRefresh();

  return (
    <header className='container mx-auto mt-4 pt-4 border-t border-x bg-white rounded-lg'>
      <nav className='nav relative flex justify-center gap-4 md:gap-10'>
        <Link
          to='/'
          className='absolute py-3 px-3 text-sky-400 left-0 -bottom-1 md:px-5'
          children={
            <Box className='w-12 h-12'>
              <img src={logo} className='inline-block w-full h-full object-fill' />
            </Box>
          }
        />
        <Menu>
          <MenuButton
            as={IconButton}
            className='!absolute right-3 focus:border-sky-300 hover:border-sky-300'
            aria-label='Options'
            icon={<MyIcon href='/sprite.svg#menu' className='w-5 h-5' />}
            variant='outline'
          />
          <MenuList>
            {isAuthenticated
              ? <MenuItem
                children='profile'
                icon={<MyIcon href='/sprite.svg#user' className='w-5 h-5' />}
                onClick={() => navigate('@me')}
              />
              : null}
            <MenuItem
              children={isAuthenticated ? 'logout' : 'sign in'}
              icon={<MyIcon href='/sprite.svg#logout' className='w-5 h-5' />}
              onClick={() => {
                if (isAuthenticated) {
                  logout()
                    .unwrap()
                    .then(_ => {
                      dispatch(unsetCredentials());
                      navigate('/');
                    })
                    .catch(err => console.error({ err }));
                } else {
                  navigate('/login');
                }
              }}
            />
          </MenuList>
        </Menu>
        <NavLink
          className='py-3 px-4 md:px-5'
          to='/'
          children='home'
        />
        <NavLink
          className='py-3 px-4 md:px-5'
          to='find_jobs'
          children='find jobs'
        />
      </nav>
    </header >

  );
}

export default Header;
