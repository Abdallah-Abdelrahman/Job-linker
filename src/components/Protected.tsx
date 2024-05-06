import { useEffect } from 'react';
import { Outlet, useNavigate } from 'react-router-dom';
import { useAppSelector } from '../hooks/store';
import { selectCurrentUser } from '../features/auth/authSlice';

function Private() {
  const user = useAppSelector(selectCurrentUser);
  const navigate = useNavigate();

  useEffect(() => {
    if (!user.isRefreshing && !user.isRefreshed) {
      navigate('/login', { replace: true, state: user });
    }
  }, [user, navigate]);

  if (user.jwt) {
    return <Outlet />;
  }
  if (user.isRefreshing)
    return <h1>loading...</h1>;
  return null;
}

export default Private;
