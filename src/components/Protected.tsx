import { useEffect } from 'react';
import { Outlet, useNavigate } from 'react-router-dom';
import { useAppSelector } from '../hooks/store';
import { selectCurrentUser } from '../features/auth';
import { SkeletonText } from '@chakra-ui/react';

function Private() {
  const user = useAppSelector(selectCurrentUser);
  const navigate = useNavigate();
  const isAuthenticated = user.jwt || user.isRefreshed;

  // if user not authenticated redirect to login page
  useEffect(() => {
      //console.log({user});
    if (!isAuthenticated && !user.isRefreshing) {
      navigate('/login', { replace: true, state: user });
    }
  }, [user, navigate, isAuthenticated]);

  return (
    <SkeletonText spacing={4} isLoaded={!user.isRefreshing}>
      {isAuthenticated ? <Outlet /> : null}
    </SkeletonText>
  );
}

export default Private;
