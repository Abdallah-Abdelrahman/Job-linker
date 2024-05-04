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
  }),
});

export const { useCreateMajorMutation } = majorApi;
