import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import { RootState } from '../store';
import { setCredentials } from '../../features/auth';
import type {
  BaseQueryFn,
  FetchArgs,
  FetchBaseQueryError,
} from '@reduxjs/toolkit/query';
import { unsetCredentials } from '../../features/auth/authSlice';

export interface ServerResponse<T> {
  message: string;
  status: 'success' | 'error';
  data: T;
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

const baseQuery = fetchBaseQuery({
  baseUrl: '/api/v1',
  prepareHeaders: async (headers, { getState }) => {
    const token = (getState() as RootState).auth.jwt;
    if (token) {
      headers.set('Authorization', `Bearer ${token}`);
    }
    return headers;
  },
});

/**
 * custom wrapper around baseQuery to refresh token on 401 status error
 *
 */
const baseQueryWithReauth: BaseQueryFn<
  string | FetchArgs,
  unknown,
  FetchBaseQueryError
> = async (args, api, extraOptions) => {
  let result = await baseQuery(args, api, extraOptions);

  if (result.error && result.error.status === 401) {
    console.log('-------token expires------->');
    api.dispatch(setCredentials({ isRefreshing: true }));

    // try to get a new token
    const refreshResult = await baseQuery(
      {
        url: '/refresh',
        method: 'POST',
        headers: { 'X-CSRF-TOKEN': document.cookie.split('=')[1] },
        credentials: 'include',
      },
      api,
      extraOptions,
    );

    if (refreshResult.data) {
      // store the new token
      api.dispatch(
        setCredentials({
          ...refreshResult.data.data,
          isRefreshed: true,
          isRefreshing: false,
        }),
      );

      // retry the initial query
      result = await baseQuery(args, api, extraOptions);
    } else {
      // no refresh token; logout
      api.dispatch(setCredentials({ isRefreshing: false }));
    }
  }
  return result;
};

export const api = createApi({
  baseQuery: baseQueryWithReauth,
  tagTypes: ['me', 'refresh', 'candidates', 'recruiters', 'job'],
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
      providesTags: ['me', 'refresh', 'recruiters', 'candidates', 'job'],
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
      invalidatesTags: ['me'],
    }),
    insights: builder.mutation<unknown, FormData>({
      query: (formdata) => ({
        url: 'upload/insights',
        method: 'POST',
        body: formdata,
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
    uploadProfileImage: builder.mutation<UserResponse, FormData>({
      query: (formdata) => {
        return {
          url: 'upload_profile_image',
          method: 'POST',
          body: formdata,
        };
      },
      invalidatesTags: ['me'],
    }),
    getUploadedFile: builder.query<
      string,
      { file_type: string; filename: string }
    >({
      query: ({ file_type, filename }) => ({
        url: `uploads/${file_type}/${filename}`,
      }),
      responseHandler: (response) => response.data.url,
    }),
  }),
});

export const {
  useLoginMutation,
  useRegisterMutation,
  useVerfiyQuery,
  useLazyVerfiyQuery,
  useMeQuery,
  useUploadMutation,
  useRefreshMutation,
  useLazyMeQuery,
  useUpdateMeMutation,
  useDeleteMeMutation,
  useUpdatePasswordMutation,
  useLogoutMutation,
  useInsightsMutation,
  useUploadProfileImageMutation,
  useGetUploadedFileQuery,
} = api;
