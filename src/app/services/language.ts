import { api } from "./auth";

export interface Language {
  language_id: string;
  name: string;
}

export interface LanguageResponse {
  language: Language;
}

export const languageApi = api.injectEndpoints({
  endpoints: (builder) => ({
    getLanguages: builder.query<Language[], void>({
      query: () => "languages",
    }),
    createLanguage: builder.mutation<LanguageResponse, Partial<Language>>({
      query: (language) => ({
        url: "languages",
        method: "POST",
        body: language,
      }),
    }),
    updateLanguage: builder.mutation<
      LanguageResponse,
      { language_id: string; updates: Partial<Language> }
    >({
      query: ({ language_id, updates }) => ({
        url: `languages/${language_id}`,
        method: "PUT",
        body: updates,
      }),
    }),
    deleteLanguage: builder.mutation<void, { language_id: string }>({
      query: ({ language_id }) => ({
        url: `languages/${language_id}`,
        method: "DELETE",
      }),
    }),
  }),
});

export const {
  useGetLanguagesQuery,
  useCreateLanguageMutation,
  useUpdateLanguageMutation,
  useDeleteLanguageMutation,
} = languageApi;
