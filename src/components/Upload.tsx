import { useEffect, useRef, useState } from 'react';
import { Text, FormControl, Input, FormLabel, Box } from '@chakra-ui/react';
import { MyIcon } from '.';

function Upload(props) {
  const inputRef = useRef<HTMLInputElement | null>(null);
  const boxRef = useRef<HTMLDivElement | null>(null);
  const [file, setFile] = useState<string>();

  // focus box when no file uploaded
  // TODO: make the upload clickable by enter key
  useEffect(() => {
    if (props.isError) {
      boxRef.current?.focus();
    }
  });

  return (
    <FormControl className='px-4 flex flex-col items-center gap-2'>
      <FormLabel className='self-start text-gray-600 !text-base'>Upload your cv </FormLabel>
      <Box
        ref={boxRef}
        tabIndex={0}
        className={`
        cursor-pointer focus:outline-none focus:ring-2  ring-offset-2
        ${props.isError ? 'focus:ring-red-400' : 'focus:ring-sky-400'}
        grid place-items-center gap-2 p-4 border-2 border-dashed rounded-md`}
        onClick={() => {
          inputRef.current?.click();
        }}
      >
        <MyIcon
          href='/sprite.svg#upload-0x01'
          className='w-10 h-10'
        />
        <Input
          ref={inputRef}
          type='file'
          name='file'
          hidden
          onChange={(evt) => setFile(evt.currentTarget.files?.[0].name)}
        />
        <Text className='text-sm text-gray-500'>
          {!file
            ? <span>click to upload your file<br /> max size: 2MB<br /> media type: pdf</span>
            : file}
        </Text>
      </Box>
    </FormControl>
  );
}


export default Upload;
