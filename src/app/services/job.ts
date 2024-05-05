import { api } from "./auth";

export interface Job {
  major_id: string;
  job_title: string;
  location: string;
  job_description: string;
  exper_years: string;
  salary: number;
}

export interface JobResponse {
  job: Job;
}

export interface Candidate {
  id: string;
  name: string;
  email: string;
}

export interface RecommendedCandidateResponse {
  candidates: Candidate[];
}

export const jobApi = api.injectEndpoints({
  endpoints: (builder) => ({
    createJob: builder.mutation<JobResponse, Partial<Job>>({
      query: (job) => ({
        url: "jobs",
        method: "POST",
        body: job,
      }),
    }),
    getJob: builder.query<JobResponse, { job_id: string }>({
      query: ({ job_id }) => `jobs/${job_id}`,
    }),
    updateJob: builder.mutation<
      JobResponse,
      { job_id: string; updates: Partial<Job> }
    >({
      query: ({ job_id, updates }) => ({
        url: `jobs/${job_id}`,
        method: "PUT",
        body: updates,
      }),
    }),
    deleteJob: builder.mutation<void, { job_id: string }>({
      query: ({ job_id }) => ({
        url: `jobs/${job_id}`,
        method: "DELETE",
      }),
    }),
    addSkillToJob: builder.mutation<
      JobResponse,
      { job_id: string; skill_id: string }
    >({
      query: ({ job_id, skill_id }) => ({
        url: `jobs/${job_id}/skills`,
        method: "POST",
        body: { skill_id },
      }),
    }),
    removeSkillFromJob: builder.mutation<
      JobResponse,
      { job_id: string; skill_id: string }
    >({
      query: ({ job_id, skill_id }) => ({
        url: `jobs/${job_id}/skills/${skill_id}`,
        method: "DELETE",
      }),
    }),
    getJobs: builder.query<Job[], void>({
      query: () => "jobs",
    }),
    getRecommendedCandidates: builder.query<
      RecommendedCandidateResponse,
      { job_id: string }
    >({
      query: ({ job_id }) => `jobs/${job_id}/recommended_candidates`,
    }),
  }),
});

export const {
  useCreateJobMutation,
  useGetJobQuery,
  useUpdateJobMutation,
  useDeleteJobMutation,
  useAddSkillToJobMutation,
  useRemoveSkillFromJobMutation,
  useGetJobsQuery,
  useGetRecommendedCandidatesQuery,
} = jobApi;
