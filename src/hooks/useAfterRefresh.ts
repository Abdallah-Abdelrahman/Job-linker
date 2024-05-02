import { useAppSelector } from './store';
import { selectCurrentUser } from '../features/auth/authSlice';


/**
 * this custom is general purpose is to refetch data when argument changes
 * @param {Function} useQuery_ - any rtk query hook 
 * @returns {Object} result  - rtk query result
 */
function useAfterRefreshQuery(useQuery_) {
  const user = useAppSelector(selectCurrentUser);

  return useQuery_(user);
}

export default useAfterRefreshQuery;
