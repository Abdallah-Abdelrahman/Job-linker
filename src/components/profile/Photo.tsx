import { Box, Button, SkeletonCircle } from '@chakra-ui/react';
import MyIcon from '../Icon';
import { useRef } from 'react';

type Props = {
  imageUrl: string,
  setFile: React.Dispatch<React.SetStateAction<File | null>>,
  isLoading: boolean
  disabled: boolean
}

function Photo({ imageUrl, setFile, isLoading, disabled }: Props) {
  const ref = useRef();
  const fileName = imageUrl.split('/').pop();
  const filePath = 'http://localhost:5000/api/v1/download/images/' + fileName;

  console.log({ disabled })
  return (
    <Box className='w-32 min-h-32 h-32 rounded-full overflow-hidden relative'>
      <SkeletonCircle w='100%' h='100%' isLoaded={!isLoading}>
        <img
          src={filePath || 'https://placehold.co/600x400'}
          className='w-full h-full object-cover'
        />
      </SkeletonCircle>
      <Button
        disabled={disabled}
        className={`!absolute !bg-transparent !inset-0 !w-full !h-full
        flex items-center justify-center opacity-0
        hover:${disabled ? '!cursor-auto' : 'opacity-80 !cursor-pointer'} transition duration-500 bg-white bg-opacity-30`}
        onClick={() => !disabled && ref.current.click()}
      >
        <MyIcon href='/sprite.svg#profile-placeholder' className='w-10 h-10' />
      </Button>
      <input
        id='file-upload'
        ref={ref}
        type='file'
        onChange={(e) => setFile(e.target.files?.[0])}
        className='hidden'
      />

    </Box>
  );
}

export default Photo;
