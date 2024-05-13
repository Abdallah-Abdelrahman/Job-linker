import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import { RootState } from '../store';

export interface ServerResponse<T> {
  message: string
  status: 'success' | 'error'
  data: T
}
export interface User {
  role: string;
  name: string;
  email: string;
}

export interface UserResponse {
  user: User;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  name: string;
  password: string;
  role: 'candidate' | 'recruiter';
}

export const api = createApi({
  baseQuery: fetchBaseQuery({
    baseUrl: '/api/v1',
    prepareHeaders: (headers, { getState }) => {
      const token = (getState() as RootState).auth.jwt;
      if (token) {
        //console.log({ token });
        headers.set('Authorization', `Bearer ${token}`);
      }
      return headers;
    },
  }),
  tagTypes: ['me', 'refresh', 'candidates', 'recruiters'],
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
        params: param,
      }),
    }),
    me: builder.query<UserResponse, void>({
      query: () => ({
        url: '@me',
        //headers: {'Authorization': `Bearer ${token}`},
      }),
      providesTags: ['me', 'refresh', 'recruiters', 'candidates'],
    }),
    upload: builder.mutation<UserResponse, FormData>({
      query: (formdata) => {
        return {
          url: 'upload',
          method: 'POST',
          body: formdata,
          params: { role: formdata.get('role') },
        };
      },
      invalidatesTags: ['me']
    }),
    insights: builder.mutation<unknown, FormData>({
      query: (formdata) => ({
        url: 'insigths',
        method: 'POST',
        body: formdata
      })
    }),
    refresh: builder.mutation<UserResponse, { token: string }>({
      query: ({ token }) => ({
        url: 'refresh',
        method: 'POST',
        headers: { 'X-CSRF-TOKEN': token },
        credentials: 'include',
      }),
      invalidatesTags: ['refresh'],
    }),
    updateMe: builder.mutation<UserResponse, Partial<User>>({
      query: (updates) => ({
        url: '@me',
        method: 'PUT',
        body: updates,
      }),
      invalidatesTags: ['me'],
    }),
    deleteMe: builder.mutation<void, void>({
      query: () => ({
        url: '@me',
        method: 'DELETE',
      }),
    }),
    updatePassword: builder.mutation<
      void,
      { current_password: string; new_password: string }
    >({
      query: ({ current_password, new_password }) => ({
        url: '@me/password',
        method: 'PUT',
        body: { current_password, new_password },
      }),
    }),
    logout: builder.mutation<ServerResponse<Record<string, never>>, void>({
      query: () => ({
        url: 'logout',
        method: 'DELETE',
      }),
      invalidatesTags: ['refresh', 'candidates', 'recruiters'],
    }),
  }),
});

export const {
  useLoginMutation,
  useRegisterMutation,
  useVerfiyQuery,
  useMeQuery,
  useUploadMutation,
  useRefreshMutation,
  useLazyMeQuery,
  useUpdateMeMutation,
  useDeleteMeMutation,
  useUpdatePasswordMutation,
  useLogoutMutation,
} = api;
