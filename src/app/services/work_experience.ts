import { api } from './auth';

export interface WorkExperience {
  id: string;
  title: string;
  description: string;
  company: string;
  location: string;
  startDate: Date;
  endDate: Date;
}

export interface WorkExperienceResponse {
  work_experience: WorkExperience;
}

export const workExperienceApi = api.injectEndpoints({
  endpoints: (builder) => ({
    createWorkExperience: builder.mutation<
      WorkExperienceResponse,
      Partial<WorkExperience>
    >({
      query: (work_experience) => ({
        url: 'work_experiences',
        method: 'POST',
        body: work_experience,
      }),
    }),
    getWorkExperience: builder.query<
      WorkExperienceResponse,
      { work_experience_id: string }
    >({
      query: ({ work_experience_id }) =>
        `work_experiences/${work_experience_id}`,
    }),
    updateWorkExperience: builder.mutation<
      WorkExperienceResponse,
      { work_experience_id: string; xp: Partial<WorkExperience> }
    >({
      query: ({ work_experience_id, xp }) => ({
        url: `work_experiences/${work_experience_id}`,
        method: 'PUT',
        body: xp,
      }),
      invalidatesTags: ['me'],
    }),
    deleteWorkExperience: builder.mutation<
      void,
      { work_experience_id: string }
    >({
      query: ({ work_experience_id }) => ({
        url: `work_experiences/${work_experience_id}`,
        method: 'DELETE',
      }),
    }),
    getWorkExperiences: builder.query<WorkExperience[], { major_id?: string }>({
      query: ({ major_id }) =>
        major_id ? `work_experiences/${major_id}` : 'work_experiences',
    }),
  }),
});

export const {
  useCreateWorkExperienceMutation,
  useGetWorkExperienceQuery,
  useUpdateWorkExperienceMutation,
  useDeleteWorkExperienceMutation,
  useGetWorkExperiencesQuery,
} = workExperienceApi;
