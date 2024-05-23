import { api } from './auth';

export interface Skill {
  skill_id: string;
  name: string;
}

export interface SkillResponse {
  skill: Skill;
}

export const skillApi = api.injectEndpoints({
  endpoints: (builder) => ({
    getSkills: builder.query<Skill[], void>({
      query: () => 'skills',
    }),
    createSkill: builder.mutation<SkillResponse, Partial<Skill>>({
      query: (skill) => ({
        url: 'skills',
        method: 'POST',
        body: skill,
      }),
    }),
    updateSkill: builder.mutation<
      SkillResponse,
      { skill_id: string; skill: Partial<Skill> }
    >({
      query: ({ skill_id, skill }) => {
        return ({
          url: `skills/${skill_id}`,
          method: 'PUT',
          body: skill,
        });
      },
    }),
    deleteSkill: builder.mutation<void, { skill_id: string }>({
      query: ({ skill_id }) => ({
        url: `skills/${skill_id}`,
        method: 'DELETE',
      }),
    }),
  }),
});

export const {
  useGetSkillsQuery,
  useCreateSkillMutation,
  useUpdateSkillMutation,
  useDeleteSkillMutation,
} = skillApi;
