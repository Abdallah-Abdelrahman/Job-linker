import { Link } from 'react-router-dom';
import _404 from '../assets/404.gif';
import { Heading, Text } from '@chakra-ui/react';

function ErrorPage() {
  return (
    <main className="w-full max-w-xl p-4 mx-auto h-full flex flex-col items-center justify-center">
      <Heading as="h1">Oops..</Heading>
      <img src={_404} alt="lost walking person" />
      <Text>
        {' '}
        looks like you got lost! go to
        <Link to="/" className="mx-2 text-sky-500">
          home
        </Link>
      </Text>
    </main>
  );
}

export default ErrorPage;
