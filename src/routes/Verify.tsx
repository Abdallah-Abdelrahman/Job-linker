import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useVerfiyQuery } from '../app/services/auth';
import { useAppDispatch } from '../hooks/store';
import { setCredentials } from '../features/auth';
import { SkeletonText } from '@chakra-ui/react';

function Verify() {
  // extarct the query from url
  const parmas = new URLSearchParams(window.location.search);
  const navigate = useNavigate();
  const token = parmas.get('token');
  const { data, isLoading, isSuccess, isUninitialized } = useVerfiyQuery({ token });
  const dispatch = useAppDispatch();
  console.log({token})

  useEffect(() => {
    if (isSuccess) {
      dispatch(setCredentials(data));
      navigate('/@me');
    }
  }, [token, isSuccess, dispatch, data, navigate]);

  if (isUninitialized || isLoading) {
    return (<SkeletonText mt='4' noOfLines={4} spacing='4' skeletonHeight='2' />);
  }
  return (null);
}

export default Verify;
