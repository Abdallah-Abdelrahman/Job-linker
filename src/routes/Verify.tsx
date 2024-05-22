import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useLazyVerfiyQuery } from '../app/services/auth';
import { useAppDispatch } from '../hooks/store';
import { setCredentials } from '../features/auth';
import { Skeleton, SkeletonText } from '@chakra-ui/react';

function Verify() {
  // extarct the query from url
  const navigate = useNavigate();
  const [verify, { isLoading, isUninitialized }] = useLazyVerfiyQuery();
  const dispatch = useAppDispatch();

  useEffect(() => {
    const parmas = new URLSearchParams(window.location.search);
    const token = parmas.get('token')!;
    console.log('-----token------>', { token });
    if (isUninitialized) {
      dispatch(setCredentials({ isRefreshing: true }));
    }
    verify({ token })
      .unwrap()
      .then(data => {
        console.log('------verify--------->', { data });
        dispatch(setCredentials(
          {
            ...data.data,
            isRefreshed: true,
            isRefreshing: false
          }));
        navigate('/@me');
      })
      .catch(_ => navigate('/login'))
      .finally(() => {
        dispatch(setCredentials({ isRefreshing: false }));
      });
  }, [verify, dispatch, navigate, isUninitialized]);

  return (
    <Skeleton size='lg' isLoaded={isUninitialized || !isLoading} />
  );
}

export default Verify;
