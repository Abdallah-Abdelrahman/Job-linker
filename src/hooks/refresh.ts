import { useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { setCredentials } from '../features/auth/authSlice';

function useRefresh() {
  const dispatch = useDispatch();

  useEffect(() => {
    const reloadHandler = (evt) => {
      evt.preventDefault();
      // refresh token
      fetch('/api/v1/refresh', {
        method: 'POST',
        credentials: 'include',
        headers: { 'X-CSRF-TOKEN': document.cookie.split('=')[1] }
      })
        .then(resp => resp.json())
        .then(data => {
          console.log({ data });
          dispatch(setCredentials(data));
        })
        .catch(err => console.error({ err }));
    };

    window.addEventListener('load', reloadHandler);

    // cleanup
    return () => {
      window.removeEventListener('load', reloadHandler);
    };
  }, [dispatch]);
}

export default useRefresh;
