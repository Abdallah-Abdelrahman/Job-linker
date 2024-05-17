import { useEffect } from 'react';
import { setCredentials } from '../features/auth/authSlice';
import { useAppDispatch } from './store';

function useRefresh() {
  const dispatch = useAppDispatch();

  useEffect(() => {
    let ignore = false;

    const reloadHandler = (evt: Event) => {
      evt.preventDefault();
      // refresh token
      fetch('/api/v1/refresh', {
        method: 'POST',
        credentials: 'include',
        headers: { 'X-CSRF-TOKEN': document.cookie.split('=')[1] }
      })
        .then(resp => {
          if (!ignore) {
            dispatch(setCredentials({ isRefreshing: true, isRefreshed: resp.ok }));
          }
          return resp.json();
        })
        .then(({ data }) => {
          console.log('----useRefresh---->');
          dispatch(setCredentials({ ...data, isRefreshing: false }));
        })
        .catch(err => console.error({ err }))
        .finally(() => {
          dispatch(setCredentials({ isRefreshing: false }));
        });
    };

    window.addEventListener('load', reloadHandler);

    // cleanup
    return () => {
      window.removeEventListener('load', reloadHandler);
      ignore = true;
    };
  }, [dispatch]);
}

export default useRefresh;
