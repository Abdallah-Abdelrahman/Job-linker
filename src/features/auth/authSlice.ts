import { createSlice } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';
import type { RootState } from '../../app/store';

type AuthState = {
  role: 'recruiter' | 'candidate' | null,
  jwt: string | null,
  isRefreshing: boolean,
  isRefreshed: boolean
  message: string,
  status: string,
}
const initialState: AuthState = {
  role: null,
  jwt: null,
  message: '',
  status: '',
  isRefreshing: true,
  isRefreshed: false
};

const slice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    setCredentials: (
      state,
      {
        payload,
      }: PayloadAction<Partial<AuthState>>,
    ) => {
      const { message, status, ...rest } = payload;
      return {
        ...state,
        ...rest,
      };
    },
  },
});

export const { setCredentials } = slice.actions;

export const selectCurrentUser = (state: RootState) => state.auth;

export default slice.reducer;
