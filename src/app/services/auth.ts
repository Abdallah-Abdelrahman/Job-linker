
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import { RootState } from '../store'

export interface User {
  role: string
  name: string
  email: string
}

export interface UserResponse {
  user: User
}

export interface LoginRequest {
  email: string
  password: string
}

export interface RegisterRequest {
  email: string
  name: string
  password: string
  role: 'candidate' | 'recruiter'
}

export const api = createApi({
  baseQuery: fetchBaseQuery({
    baseUrl: '/api',
    prepareHeaders: (headers, { getState }) => {
      // By default, if we have a token in the store, let's use that for authenticated requests
      const token = (getState() as RootState).auth.jwt;
      if (token) {
        console.log({ token });
        headers.set('Authorization', `Bearer ${token}`);
      }
      return headers;
    },
  }),
  tagTypes: ['refresh'],
  endpoints: (builder) => ({
    login: builder.mutation<UserResponse, LoginRequest>({
      query: (credentials) => ({
        url: 'login',
        method: 'POST',
        body: credentials,
      }),
    }),
    register: builder.mutation<UserResponse, RegisterRequest>({
      query: (credentials) => ({
        url: 'register',
        method: 'POST',
        body: credentials,
      }),
    }),
    verfiy: builder.query<UserResponse, { token: string }>({
      query: (param) => ({
        url: 'verify',
        params: param
      }),
    }),
    me: builder.query<UserResponse, void>({
      query: () => ({
        url: '@me',
        //headers: {'Authorization': `Bearer ${token}`},
      }),
      providesTags: ['refresh'],
    }),
    upload: builder.mutation<UserResponse, File>({
      query: (file) => ({
        url: 'upload',
        method: 'POST',
        body: file
      }),
    }),
    refresh: builder.mutation<UserResponse, { token: string }>({
      query: ({ token }) => ({
        url: 'refresh',
        method: 'POST',
        headers: { 'X-CSRF-TOKEN': token },
        credentials: 'include',
      }),
      invalidatesTags: ['refresh'],
    })
  }),
});

export const {
  useLoginMutation,
  useRegisterMutation,
  useVerfiyQuery,
  useMeQuery,
  useUploadMutation,
  useRefreshMutation,
  useLazyMeQuery
} = api;
