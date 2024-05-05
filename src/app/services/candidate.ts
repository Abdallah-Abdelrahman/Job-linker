import { api } from "./auth";

const candidApi = api.injectEndpoints({
  endpoints: (build) => ({
    createCand: build.mutation({
      query: () => 'test',
    }),
  }),
});

export const {} = candidApi;

