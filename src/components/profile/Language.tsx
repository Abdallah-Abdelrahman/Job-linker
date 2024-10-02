import { useState } from 'react';
import { useCreateLanguageMutation } from '../../app/services/language';
import {
  useAddLanguageToCurrentCandidateMutation,
  useRemoveLanguageFromCurrentCandidateMutation,
} from '../../app/services/candidate';
import { Input, ListItem, Text } from '@chakra-ui/react';
import UpdateOrCancel from './UpdateOrCancel';
import MyIcon from '../Icon';
import * as T from './types';

type LangaugeProps = {
  language: T.Language;
  isEditable: boolean;
};
function Language({ language, isEditable }: LangaugeProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [value, setValue] = useState(language.name);
  const [add, { isLoading: isLoading1 }] = useCreateLanguageMutation();
  const [removeCandidLang, { isLoading: isLoading2 }] =
    useRemoveLanguageFromCurrentCandidateMutation();
  const [addLangToCandid, { isLoading: isLoading3 }] =
    useAddLanguageToCurrentCandidateMutation();

  const handleUpdate = () => {
    Promise.allSettled([
      removeCandidLang({ lang_id: language.id }).unwrap(),
      add({ name: value })
        .unwrap()
        .then(({ data }) => addLangToCandid({ lang_id: data.id })),
    ])
      .then((_) => setIsEditing(false))
      .catch((err) => console.log({ err }))
      .finally(() => {
        setIsEditing(false);
      });
  };

  return (
    <ListItem className="relative p-2 bg-orange-50 text-orange-500 rounded-tl-lg rounded-br-lg">
      {isEditing ? (
        /* render input field to edit value */
        <>
          <Input
            className="!w-max"
            value={value}
            onChange={(e) => setValue(e.target.value)}
          />
          <UpdateOrCancel
            size="sm"
            rounded="full"
            isLoading={isLoading1 || isLoading2 || isLoading3}
            update={handleUpdate}
            cancel={() => {
              setIsEditing(false);
              setValue(language.name);
            }}
          />
        </>
      ) : (
        /* render normal text component */
        <>
          {isEditable && (
            <MyIcon
              href="/sprite.svg#edit"
              className="absolute top-0 right-0 w-3 h-3 cursor-pointer"
              onClick={() => setIsEditing(true)}
            />
          )}
          <Text>{value}</Text>
        </>
      )}
    </ListItem>
  );
}
export default Language;
