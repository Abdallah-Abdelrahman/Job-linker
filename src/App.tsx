import { Register } from "./features/auth";
import { Login } from "./features/auth";
import "./App.css";
import { Link, NavLink, Outlet, Route, createBrowserRouter, createRoutesFromElements, useNavigate } from "react-router-dom";
import { useEffect } from "react";

const App = () => {
  return (
    <div className="App">
      <h1>Job Linker</h1>
    </div>
  );
};

function Verify() {
  // extarct the query from url
  const parmas = new URLSearchParams(window.location.search);
  const navigate = useNavigate();
  const token = parmas.get('token');

  useEffect(() => {
    fetch(`/api/verify?token=${token}`)
      .then(resp => resp.json())
      .then(_ => {
        navigate('/me');
      })
      .catch(err => console.error({ err }));
  }, [token, navigate]);

  return (<h1>verify</h1>);
}

function Me() {
  // refresh token request
  useEffect(() => {
    let ignore = false;

    if (!ignore) {
      fetch('/api/@me', {
        headers: { 'Authorization': '' }
      })
        .then(resp => resp.json())
        .then(data => console.log({ data }))
        .catch(err => console.error({ err }));
    }

    // cleanup
    return () => {
      ignore = true;
    }
  }, [])

  return (<h1>me</h1>)
}

function Upload() {
  const handleSubmit = (evt) => {
    evt.preventDefault()
    const formData = new FormData(evt.currentTarget)
    console.log({ formData })
    fetch('/api/upload', {
      method: 'POST',
      body: formData
    })
      .then(resp => resp.json())
      .then(data => console.log({ data }))
      .catch(err => console.error({ err }))
  }

  return (
    <form onSubmit={handleSubmit}>
      <input type="file" name='file' /><br />
      <button type='submit'>upload</button>
    </form>

  )
}

function Layout() {
  // TODO: request refresh only when token expires
  useEffect(() => {
    // refresh token on reload
    const reloadHandler = (evt) => {
      console.log({ evt });
      evt.preventDefault();
      fetch('/api/refresh', {
        method: 'POST',
        credentials: 'include',
        headers: { 'X-CSRF-TOKEN': document.cookie.split('=')[1] }
      })
        .then(resp => resp.json())
        .then(data => console.log({ data }, '--------->'))
        .catch(err => console.error({ err }));
    };

    //window.addEventListener('beforeunload', reloadHandler);

    // cleanup
    return () => {
      //window.removeEventListener('beforeunload', reloadHandler);
    }
  }, []);

  return (
    <div className='w-full h-full p-4 flex flex-col items-center'>
      <header className='w-full shadow-md rounded-md' >
        <ul className='flex justify-center p-4 gap-10'>
          <li><NavLink to='/'> home </NavLink></li>
          <li><NavLink to='login'>login</NavLink></li>
          <li><NavLink to='signup'>signup</NavLink></li>
        </ul>
      </header>
      <main className='w-full m-auto flex justify-center'>
        <Outlet />
      </main>
      <footer className='mt-auto'>ATS &copy; mohanad & abdallah</footer>

    </div>
  )
}

export const router = createBrowserRouter(createRoutesFromElements(
  <Route path='/' element={<Layout />}>
    <Route index element={<App />} />
    <Route path='signup' element={<Register />} />
    <Route path='login' element={<Login />} />
    <Route path='verify' element={<Verify />} />
    <Route path='me' element={<Me />} />
  </Route>
));

export default App;
