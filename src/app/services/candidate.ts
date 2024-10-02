import { api } from './auth';

export interface Education {
  candidate_id: string;
  created_at: string;
  degree: string;
  description: string;
  end_date: string;
  field_of_study: string;
  id: string;
  institute: string;
  start_date: string;
  updated_at: string;
}

export interface Language {
  created_at: string;
  id: string;
  name: string;
  updated_at: string;
}

export interface Major {
  created_at: string;
  id: string;
  name: string;
  updated_at: string;
}

export interface Skill {
  created_at: string;
  id: string;
  name: string;
  updated_at: string;
}

export interface WorkExperience {
  candidate_id: string;
  company: string;
  created_at: string;
  description: string;
  end_date: string;
  id: string;
  location: string;
  start_date: string;
  title: string;
  updated_at: string;
}

export interface Candidate {
  id: string;
  educations: Education[];
  languages: Language[];
  major: Major;
  skills: Skill[];
  work_experiences: WorkExperience[];
}

export interface CandidateResponse {
  data: Candidate;
  message: string;
  status: string;
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
      invalidatesTags: ['me'],
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
    addWorkExperienceToCurrentCandidate: builder.mutation<
      CandidateResponse,
      Partial<WorkExperience>
    >({
      query: (workExperience) => ({
        url: 'candidates/@me/work_experiences',
        method: 'POST',
        body: workExperience,
      }),
    }),
    updateWorkExperienceForCurrentCandidate: builder.mutation<
      CandidateResponse,
      { workExperienceId: string; updates: Partial<WorkExperience> }
    >({
      query: ({ workExperienceId, updates }) => ({
        url: `candidates/@me/work_experiences/${workExperienceId}`,
        method: 'PUT',
        body: updates,
      }),
    }),
    deleteWorkExperienceForCurrentCandidate: builder.mutation<
      void,
      { workExperienceId: string }
    >({
      query: ({ workExperienceId }) => ({
        url: `candidates/@me/work_experiences/${workExperienceId}`,
        method: 'DELETE',
      }),
    }),
    addEducationToCurrentCandidate: builder.mutation<
      CandidateResponse,
      Partial<Education>
    >({
      query: (education) => ({
        url: 'candidates/@me/educations',
        method: 'POST',
        body: education,
      }),
    }),
    updateEducationForCurrentCandidate: builder.mutation<
      CandidateResponse,
      { education_id: string; education: Partial<Education> }
    >({
      query: ({ education_id, education }) => ({
        url: `candidates/@me/educations/${education_id}`,
        method: 'PUT',
        body: education,
      }),
      invalidatesTags: ['me'],
    }),
    deleteEducationForCurrentCandidate: builder.mutation<
      void,
      { educationId: string }
    >({
      query: ({ educationId }) => ({
        url: `candidates/@me/educations/${educationId}`,
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
  useAddWorkExperienceToCurrentCandidateMutation,
  useUpdateWorkExperienceForCurrentCandidateMutation,
  useDeleteWorkExperienceForCurrentCandidateMutation,
  useAddEducationToCurrentCandidateMutation,
  useUpdateEducationForCurrentCandidateMutation,
  useDeleteEducationForCurrentCandidateMutation,
  useDeleteCurrentCandidateMutation,
} = candApi;
