import { useEffect } from 'react';
import { setCredentials } from '../features/auth/authSlice';
import { useAppDispatch } from './store';
import { env } from '../app/services/auth';

function useRefresh() {
  const dispatch = useAppDispatch();

  useEffect(() => {
    let ignore = false;

    const reloadHandler = () => {
      // refresh token
      fetch(`${env["production"]}/api/v1/refresh`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'X-CSRF-TOKEN': document.cookie.split('=')[1] },
      })
        .then((resp) => {
          if (!ignore) {
            dispatch(
              setCredentials({ isRefreshing: true, isRefreshed: resp.ok }),
            );
          }
          return resp.json();
        })
        .then(({ data }) => {
          // console.log('----useRefresh---->');
          dispatch(setCredentials({ ...data, isRefreshing: false }));
        })
        .catch((err) => console.error({ err }))
        .finally(() => {
          dispatch(setCredentials({ isRefreshing: false }));
        });
    };

    /**
     * For more info on why handling browser reloading this way,
     * see https://rb.gy/dbwngc
     */
    if (document.readyState === 'loading') {
      // Loading hasn't finished yet
      document.addEventListener('DOMContentLoaded', reloadHandler);
    } else {
      // `DOMContentLoaded` has already fired
      reloadHandler();
    }

    // cleanup
    return () => {
      document.removeEventListener('DOMContentLoaded', reloadHandler);
      ignore = true;
    };
  }, [dispatch]);
}

export default useRefresh;
