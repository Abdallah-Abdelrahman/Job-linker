import { api } from './auth';

export interface Recruiter {
  company_name: string;
  company_info: string;
}

export interface RecruiterResponse {
  recruiter: Recruiter;
}

export const recruiterApi = api.injectEndpoints({
  endpoints: (builder) => ({
    createRecruiter: builder.mutation<RecruiterResponse, void>({
      query: () => ({
        url: 'recruiters',
        method: 'POST',
      }),
      invalidatesTags: ['recruiters'],
    }),
    getCurrentRecruiter: builder.query<RecruiterResponse, void>({
      query: () => 'recruiters/@me',
    }),
    updateCurrentRecruiter: builder.mutation<
      RecruiterResponse,
      Partial<Recruiter>
    >({
      query: (updates) => ({
        url: 'recruiters/@me',
        method: 'PUT',
        body: updates,
      }),
    }),
  }),
});

export const {
  useCreateRecruiterMutation,
  useGetCurrentRecruiterQuery,
  useUpdateCurrentRecruiterMutation,
} = recruiterApi;
