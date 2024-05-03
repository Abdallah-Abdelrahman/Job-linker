import { useRef, useState } from 'react';
import { useUploadMutation } from '../app/services/auth';
import { Text, FormControl, Input } from '@chakra-ui/react';
import MyIcon from './Icon';
import { useAppSelector } from '../hooks/store';
import { selectCurrentUser } from '../features/auth/authSlice';

function Upload() {
  const user = useAppSelector(selectCurrentUser);
  const [upload, { isSuccess, isLoading, isError }] = useUploadMutation();
  const inputRef = useRef(null);
  const [isUploaded, setIsUploaded] = useState(false);
  const [file, setFile] = useState<string | null>(null);

  const handleSubmit = (evt) => {
    const formData = new FormData(evt.currentTarget);
    evt.preventDefault();
    console.log({user})
    upload({file: formData, role: user.role})
      .unwrap()
      .then(data => {
        console.log({ data })
      })
      .catch(err => console.error({ err }))
  };

  return (
    <form onSubmit={handleSubmit}>
      <FormControl className='flex flex-col items-center gap-2'>
        <MyIcon
          href='/sprite.svg#upload-file'
          className=''
          onClick={() => {
            inputRef.current?.click();
            setIsUploaded(true);
          }}
        />
        <Input
          ref={inputRef}
          type='file'
          name='file'
          hidden
          onChange={(evt) => setFile(evt.currentTarget.files[0].name)}
        />
        <Text className='text-gray-500'>
          {!file
            ? <span>click to upload your file<br /> max size: 2MB<br /> media type: pdf</span>
            : file}
        </Text>
      </FormControl>
      {isUploaded && <button className='block bg-blue-100 text-blue-600 py-2 w-1/2 mt-3 mx-auto' type='submit'>
        {isLoading ? 'loading..' : isSuccess ? 'saved' : isError ? 'smth wrong' : 'save'}
      </button>
      }

    </form>

  );
}

export default Upload;
