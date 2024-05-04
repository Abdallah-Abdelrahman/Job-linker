import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { RootState } from "../store";

export interface Recruiter {
  company_name: string;
  company_info: string;
}

export interface RecruiterResponse {
  recruiter: Recruiter;
}

export const api = createApi({
  baseQuery: fetchBaseQuery({
    baseUrl: "/api/v1",
    prepareHeaders: (headers, { getState }) => {
      const token = (getState() as RootState).auth.jwt;
      if (token) {
        console.log({ token });
        headers.set("Authorization", `Bearer ${token}`);
      }
      return headers;
    },
  }),
  tagTypes: ["Recruiter"],
  endpoints: (builder) => ({
    createRecruiter: builder.mutation<RecruiterResponse, Partial<Recruiter>>({
      query: (recruiter) => ({
        url: "recruiters",
        method: "POST",
        body: recruiter,
      }),
    }),
    getCurrentRecruiter: builder.query<RecruiterResponse, void>({
      query: () => "recruiters/@me",
    }),
    updateCurrentRecruiter: builder.mutation<
      RecruiterResponse,
      Partial<Recruiter>
    >({
      query: (updates) => ({
        url: "recruiters/@me",
        method: "PUT",
        body: updates,
      }),
    }),
  }),
});

export const {
  useCreateRecruiterMutation,
  useGetCurrentRecruiterQuery,
  useUpdateCurrentRecruiterMutation,
} = api;
