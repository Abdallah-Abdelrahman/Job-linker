import { FormControl, Select } from "@chakra-ui/react";
import { college_majors } from "../../constants";
import Upload from "../Upload";
import { useCreateJobMutation } from "../../app/services/job";
import { useCreateMajorMutation } from "../../app/services/major";
import { useReducer } from "react";
import { useUploadMutation } from "../../app/services/auth";
import { useAppSelector } from "../../hooks/store";
import { selectCurrentUser } from "../../features/auth";

function AddJob() {

  const user = useAppSelector(selectCurrentUser);
  const [add_job] = useCreateJobMutation();
  const [uploadJOB] = useUploadMutation();
  const [add_major] = useCreateMajorMutation();
  const [formError, dispatch] = useReducer((oldState, newState) => {
    return { ...oldState, ...newState };
  }, { major: false, file: false });

  const handleSubmit: React.FormEventHandler<HTMLFormElement> = (evt) => {
    evt.preventDefault();
    const formdata = new FormData(evt.currentTarget);
    const { major, file } = Object.fromEntries(formdata) as { major: string, file: File };
    let canSubmit = false;

    dispatch({ major: !(major), file: !(file.name) });
    canSubmit = Boolean(major && file.name);

    if (canSubmit) {
      formdata.append('role', user.role);

      add_major({ name: major })
        .unwrap()
        .then(data => {
            formdata.append('major_id', data.data.id);
            uploadJOB(formdata)
            .unwrap()
            .then(d => console.log({d}))
            .catch(e => console.log('--------upload error------->', e));
            })
        .catch();
    }
  };

  return (
    <form id='job' onSubmit={handleSubmit} className='space-y-4'>
      <FormControl>
        <Select
          isInvalid={formError.major}
          name='major'
          placeholder='select your major'
          color='gray.600'
        >
          {college_majors.map((major) => (
            <option key={major} value={major}>
              {major}
            </option>
          ))}
        </Select>
      </FormControl>
      <Upload isError={formError.file} />
    </form>

  );
}

export default AddJob;
