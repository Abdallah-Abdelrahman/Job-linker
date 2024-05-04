import { api } from './auth';

const majorApi = api.injectEndpoints({
  endpoints: (build) => ({
    createMajor: build.mutation({
      query: (body) => ({
        url: 'majors',
        method: 'POST',
        body
      }),
    }),
    deleteMajor: build.mutation({
      query: (body) => ({
        url: 'majors',
        method: 'DELETE',
        body
      }),
    }),
  }),
});

export const { useCreateMajorMutation, useDeleteMajorMutation } = majorApi;
