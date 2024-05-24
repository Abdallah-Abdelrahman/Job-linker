import { api } from './auth';

export interface Major {
  id: string;
  name: string;
}

export const majorApi = api.injectEndpoints({
  endpoints: (builder) => ({
    getMajors: builder.query<Major[], void>({
      query: () => 'majors',
    }),
    createMajor: builder.mutation<{ data: Major }, Partial<Major>>({
      query: (body) => ({
        url: 'majors',
        method: 'POST',
        body,
      }),
      invalidatesTags: ['me'],
    }),
    updateMajor: builder.mutation<
      Major,
      { major_id: string; major: Partial<Major> }
    >({
      query: ({ major_id, major }) => ({
        url: `majors/${major_id}`,
        method: 'PUT',
        body: major,
      }),
    }),
    deleteMajor: builder.mutation<void, string>({
      query: (major_id) => ({
        url: `majors/${major_id}`,
        method: 'DELETE',
      }),
    }),
  }),
});

export const {
  useGetMajorsQuery,
  useCreateMajorMutation,
  useUpdateMajorMutation,
  useDeleteMajorMutation,
} = majorApi;
