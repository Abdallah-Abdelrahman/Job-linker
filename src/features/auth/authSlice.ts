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
      console.log('------payload---->',{payload, state});
      return {
        ...state,
        ...rest,
      };
    },
    unsetCredentials: (state) => {
      state.jwt = null;
      state.role = null;
      state.isRefreshed = false;
      state.isRefreshing = false;

    }
  },
});

export const { setCredentials, unsetCredentials } = slice.actions;

export const selectCurrentUser = (state: RootState) => state.auth;

export default slice.reducer;
