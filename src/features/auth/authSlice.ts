import { createSlice } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';
import type { RootState } from '../../app/store';

type AuthState = {
  data: {
    name: string | null,
    role: 'recruiter' | 'candidate' | null
    jwt: string | null
    isRefreshing: boolean,
    isRefreshed: boolean
  },
  message: string,
  status: string,
}

const slice = createSlice({
  name: 'auth',
  initialState: { isRefreshed: false, isRefreshing: true } as AuthState['data'],
  reducers: {
    setCredentials: (
      state,
      {
        payload,
      }: PayloadAction<AuthState>,
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
