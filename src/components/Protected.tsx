import { useEffect } from 'react';
import { Outlet, useNavigate } from 'react-router-dom';
import { useAppSelector } from '../hooks/store';
import { selectCurrentUser } from '../features/auth';
import { Skeleton } from '@chakra-ui/react';

function Private() {
  const { isRefreshing, jwt, isRefreshed } = useAppSelector(selectCurrentUser);
  const navigate = useNavigate();
  const isAuthenticated = jwt || isRefreshed;

  // if user not authenticated redirect to login page
  useEffect(() => {
    //    //console.log({user});
    if (!isAuthenticated && !isRefreshing) {
      navigate('/login');
    }
  }, [navigate, isAuthenticated, isRefreshing]);

  return (
    <Skeleton size="lg" isLoaded={!isRefreshing}>
      {isAuthenticated ? <Outlet /> : null}
    </Skeleton>
  );
}

export default Private;
