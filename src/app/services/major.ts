import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { RootState } from "../store";

export interface Major {
  id: string;
  name: string;
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
  endpoints: (builder) => ({
    getMajors: builder.query<Major[], void>({
      query: () => "majors",
    }),
    createMajor: builder.mutation<Major, Partial<Major>>({
      query: (newMajor) => ({
        url: "majors",
        method: "POST",
        body: newMajor,
      }),
    }),
    updateMajor: builder.mutation<
      Major,
      { major_id: string; updates: Partial<Major> }
    >({
      query: ({ major_id, updates }) => ({
        url: `majors/${major_id}`,
        method: "PUT",
        body: updates,
      }),
    }),
    deleteMajor: builder.mutation<void, string>({
      query: (major_id) => ({
        url: `majors/${major_id}`,
        method: "DELETE",
      }),
    }),
  }),
});

export const {
  useGetMajorsQuery,
  useCreateMajorMutation,
  useUpdateMajorMutation,
  useDeleteMajorMutation,
} = api;
