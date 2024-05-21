import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useLazyVerfiyQuery } from '../app/services/auth';
import { useAppDispatch } from '../hooks/store';
import { setCredentials } from '../features/auth';
import { SkeletonText } from '@chakra-ui/react';

function Verify() {
  // extarct the query from url
  const parmas = new URLSearchParams(window.location.search);
  const navigate = useNavigate();
  const token = parmas.get('token');
  const [verify, { isLoading, isUninitialized }] = useLazyVerfiyQuery();
  const dispatch = useAppDispatch();

  useEffect(() => {
    verify({ token })
      .unwrap()
      .then(data => {
        console.log('------verify--------->', {data});
        setCredentials(data.data);
        navigate('/@me');
      })
      .catch(_ => navigate('/login'));
  }, [verify, token, dispatch, navigate]);

  if (isUninitialized || isLoading) {
    return (<SkeletonText mt='4' noOfLines={4} spacing='4' skeletonHeight='2' />);
  }
  return (null);
}

export default Verify;
