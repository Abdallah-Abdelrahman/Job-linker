import { createSlice } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';
import type { User } from '../../app/services/auth';
import type { RootState } from '../../app/store';

type AuthState = {
  data: {
    name: string,
    role: 'recruiter' | 'candidate'
    jwt: string
  },
  message: string,
  status: string
}

const slice = createSlice({
  name: 'auth',
  initialState: {} as AuthState['data'],
  reducers: {
    setCredentials: (
      state,
      {
        payload,
      }: PayloadAction<AuthState>,
    ) => {
      const { message, status, ...rest } = payload;
      return { ...state, ...rest.data };
    },
  },
});

export const { setCredentials } = slice.actions;

export const selectCurrentUser = (state: RootState) => state.auth;

export default slice.reducer;
