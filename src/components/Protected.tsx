import { useEffect } from 'react';
import { Outlet, useNavigate } from 'react-router-dom';
import { useAppSelector } from '../hooks/store';
import { selectCurrentUser } from '../features/auth';
import { SkeletonText } from '@chakra-ui/react';

function Private() {
  const user = useAppSelector(selectCurrentUser);
  const navigate = useNavigate();
  const isAuthenticated = user.jwt || user.isRefreshed;

  useEffect(() => {
    if (!user.isRefreshing && !user.isRefreshed) {
      navigate('/login', { replace: true, state: user });
    }
  }, [user, navigate]);

  if (isAuthenticated) {
    return <Outlet />;
  }
  if (user.isRefreshing)
    return <SkeletonText mt='4' noOfLines={4} spacing='4' skeletonHeight='2' />;
  return null;
}

export default Private;
