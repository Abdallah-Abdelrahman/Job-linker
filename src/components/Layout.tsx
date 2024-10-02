import { Outlet } from 'react-router-dom';
import Footer from './Footer';
import Header from './Header';

function Layout() {
  return (
    <>
      <Header />
      <main className="container mx-auto my-4">
        <Outlet />
      </main>
      <Footer />
    </>
  );
}

export default Layout;
