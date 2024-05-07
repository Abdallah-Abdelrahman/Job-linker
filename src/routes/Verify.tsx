import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useVerfiyQuery } from '../app/services/auth';
import { useAppDispatch } from '../hooks/store';
import { setCredentials } from '../features/auth';

function Verify() {
  // extarct the query from url
  const parmas = new URLSearchParams(window.location.search);
  const navigate = useNavigate();
  const token = parmas.get('token');
  const { data, isLoading, isSuccess, isUninitialized } = useVerfiyQuery({ token });
  const dispatch = useAppDispatch();

  useEffect(() => {
    if (isSuccess) {
      dispatch(setCredentials(data));
      navigate('/@me');
    }
  }, [token, isSuccess, dispatch, data, navigate]);

  if (isUninitialized || isLoading) {
    return (<h1>loading...</h1>);
  }
  return (null);
}

export default Verify;
