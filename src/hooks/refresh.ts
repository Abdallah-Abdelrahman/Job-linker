import { useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { setCredentials } from '../features/auth/authSlice';

function useRefresh() {
  const dispatch = useDispatch();

  useEffect(() => {
    const reloadHandler = (evt: Event) => {
      evt.preventDefault();
      // refresh token
      fetch('/api/v1/refresh', {
        method: 'POST',
        credentials: 'include',
        headers: { 'X-CSRF-TOKEN': document.cookie.split('=')[1] }
      })
        .then(resp => {
          dispatch(setCredentials({ isRefreshing: true, isRefreshed: resp.ok }));
          return resp.json();
        })
        .then(({ data }) => {
          console.log('----refresh---->', { data });
          dispatch(setCredentials({ ...data, isRefreshing: false }));
        })
        .catch(err => console.error({ err }))
        .finally(() => dispatch(setCredentials({ isRefreshing: false })));
    };

    window.addEventListener('load', reloadHandler);

    // cleanup
    return () => {
      window.removeEventListener('load', reloadHandler);
    };
  }, [dispatch]);
}

export default useRefresh;
