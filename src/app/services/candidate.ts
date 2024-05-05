import {api} from './auth';

export interface Candidate {
  major_id: string;
  skills: string[];
  languages: string[];
}

export interface CandidateResponse {
  candidate: Candidate;
}

export interface RecommendedJobsResponse {
  jobs: { job: Job; has_applied: boolean }[];
}

export interface Job {
  job_title: string;
  job_description: string;
  location: string;
  major_id: string;
  salary: number;
  exper_years: number;
}

export const candApi = api.injectEndpoints({
  endpoints: (builder) => ({
    createCandidate: builder.mutation<CandidateResponse, Partial<Candidate>>({
      query: (candidate) => ({
        url: 'candidates',
        method: 'POST',
        body: candidate,
      }),
      invalidatesTags: ['candidates'],
    }),
    getCurrentCandidate: builder.query<CandidateResponse, void>({
      query: () => 'candidates/@me',
    }),
    getRecommendedJobs: builder.query<RecommendedJobsResponse, void>({
      query: () => 'candidates/recommended_jobs',
    }),
    updateCurrentCandidate: builder.mutation<
      CandidateResponse,
      Partial<Candidate>
    >({
      query: (updates) => ({
        url: 'candidates/@me',
        method: 'PUT',
        body: updates,
      }),
    }),
    addSkillToCurrentCandidate: builder.mutation<
      CandidateResponse,
      { skill_id: string }
    >({
      query: ({ skill_id }) => ({
        url: 'candidates/@me/skills',
        method: 'POST',
        body: { skill_id },
      }),
    }),
    removeSkillFromCurrentCandidate: builder.mutation<
      CandidateResponse,
      { skill_id: string }
    >({
      query: ({ skill_id }) => ({
        url: `candidates/@me/skills/${skill_id}`,
        method: 'DELETE',
      }),
    }),
    addLanguageToCurrentCandidate: builder.mutation<
      CandidateResponse,
      { lang_id: string }
    >({
      query: ({ lang_id }) => ({
        url: 'candidates/@me/languages',
        method: 'POST',
        body: { lang_id },
      }),
    }),
    removeLanguageFromCurrentCandidate: builder.mutation<
      CandidateResponse,
      { lang_id: string }
    >({
      query: ({ lang_id }) => ({
        url: `candidates/@me/languages/${lang_id}`,
        method: 'DELETE',
      }),
    }),
    deleteCurrentCandidate: builder.mutation<void, void>({
      query: () => ({
        url: 'candidates/@me',
        method: 'DELETE',
      }),
    }),
  }),
});

export const {
  useCreateCandidateMutation,
  useGetCurrentCandidateQuery,
  useGetRecommendedJobsQuery,
  useUpdateCurrentCandidateMutation,
  useAddSkillToCurrentCandidateMutation,
  useRemoveSkillFromCurrentCandidateMutation,
  useAddLanguageToCurrentCandidateMutation,
  useRemoveLanguageFromCurrentCandidateMutation,
  useDeleteCurrentCandidateMutation,
} = candApi;
