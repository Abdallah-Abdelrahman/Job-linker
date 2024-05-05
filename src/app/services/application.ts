import { api } from "./auth";

export interface Application {
  job_id: string;
  candidate_id: string;
  job_title: string;
  application_status: string;
}

export interface ApplicationResponse {
  application: Application;
}

export const applicationApi = api.injectEndpoints({
  endpoints: (builder) => ({
    createApplication: builder.mutation<
      ApplicationResponse,
      Partial<Application>
    >({
      query: (application) => ({
        url: "applications",
        method: "POST",
        body: application,
      }),
    }),
    updateApplication: builder.mutation<
      ApplicationResponse,
      { application_id: string; updates: Partial<Application> }
    >({
      query: ({ application_id, updates }) => ({
        url: `applications/${application_id}`,
        method: "PUT",
        body: updates,
      }),
    }),
    getApplication: builder.query<
      ApplicationResponse,
      { application_id?: string }
    >({
      query: ({ application_id }) =>
        application_id ? `applications/${application_id}` : "applications",
    }),
    deleteApplication: builder.mutation<void, { application_id: string }>({
      query: ({ application_id }) => ({
        url: `applications/${application_id}`,
        method: "DELETE",
      }),
    }),
  }),
});

export const {
  useCreateApplicationMutation,
  useUpdateApplicationMutation,
  useGetApplicationQuery,
  useDeleteApplicationMutation,
} = applicationApi;
