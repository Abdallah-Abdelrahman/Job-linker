import { Button, FormControl, Input, Select } from '@chakra-ui/react';
import { useReducer } from 'react';
import Upload from '../Upload';
import { college_majors } from '../../constants';

type TFormdata = {
  file: File,
} & Record<'major' | 'company_email' | 'company_name' | 'company_address', string>;
const initialErrorState = {
  candidate: { file: false, major: false },
  recruiter: { company_name: false, company_email: false, company_address: false }
};
/**
 * manages the error state
 * @param {object} state - error state
 * @param {object} action - object of which the state depends on to update
 *
 * @returns the new state
 */
const reducer = (state, action) => {
  switch (action.type) {
    case 'candidate':
      return {
        ...state, candidate: { ...state.candidate, ...action.payload }
      };
    case 'recruiter':
      return {
        ...state, recruiter: { ...state.recruiter, ...action.payload }
      };
    default:
      return (state);
  }
};

function MyForm({ onSubmit, role, isLoading }) {
  const [formError, dispatch] = useReducer(reducer, initialErrorState);

  const recruiterJSX = (
    <>
      <FormControl isInvalid={formError.recruiter.company_name}>
        <Input
          placeholder='insert company name'
          type='text'
          name='company_name'
        />
      </FormControl>
      <FormControl isInvalid={formError.recruiter.company_email}>
        <Input
          placeholder='insert company email'
          type='text'
          name='company_email'
        />
      </FormControl>
      <FormControl isInvalid={formError.recruiter.company_address}>
        <Input
          placeholder='company address'
          type='text'
          name='company_address'
        />
      </FormControl>
    </>
  );
  const candidateJSX = (
    <>
      <FormControl>
        <Select
          isInvalid={formError.candidate.major}
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
      <Upload
        label={role == 'recruiter' ? 'Upload your job description file' : 'Upload your cv'}
        isError={formError.candidate.file}
      />
    </>
  );

  const handleSubmit = (evt) => {
    const formdata = new FormData(evt.currentTarget);
    const { file, major, company_email, company_name, company_address }
      = Object.fromEntries(formdata) as TFormdata;
    let canSubmit = false;
    evt.preventDefault();
    formdata.append('role', role);

    if (role == 'candidate') {
      dispatch({
        type: 'candidate',
        payload: { file: !(file.name), major: !(major) }
      });
      canSubmit = Boolean(file.name && major);
    }

    if (role == 'recruiter') {
      dispatch({
        type: 'recruiter',
        payload: {
          company_name: !(company_name),
          company_email: !(company_email),
          company_address: !(company_address),
        }
      });
      canSubmit = Boolean(company_name && company_address && company_email);
    }

    if (canSubmit) {
      onSubmit(formdata);
    }
  };


  return (
    <form
      autoComplete='off'
      onSubmit={handleSubmit}
      className='flex flex-col w-full p-6 space-y-4 bg-white rounded-lg shadow-md'
    >
      {role == 'candidate' ? candidateJSX : recruiterJSX}
      <Button
        className='ml-auto !bg-sky-500 !text-white'
        type='submit' isLoading={isLoading}>Create Profile</Button>
    </form>
  );
}

export default MyForm;
