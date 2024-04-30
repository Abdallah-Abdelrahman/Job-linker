import Login from "./Login";
import Register from "./Register";
import "./App.css";
import { Link, Outlet, Route, createBrowserRouter, createRoutesFromElements, useNavigate } from "react-router-dom";
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
      .then(data => {
        console.log({ data });
        navigate('/me');
      })
      .catch(err => console.error({ err }));
  }, [token, navigate]);

  return (<h1>verify</h1>);
}

function Me() {

  useEffect(() => {

    let ignore = false;

    if (!ignore)
      fetch('/api/refresh', {
        method: 'POST',
        credentials: 'include',
        headers: { 'X-CSRF-TOKEN': document.cookie.split('=')[1] }
      })
        .then(resp => resp.json())
        .then(data => console.log({ data }))
        .catch(err => console.error({ err }));

    // cleanup
    return () => {
      ignore = true;
    }
  }, [])

  return (<h1>me</h1>)
}

function Layout() {
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
    <div style={{ width: '100%', height: '100%', padding: '1rem', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <header style={{ width: '100%' }}>
        <ul style={{ display: 'flex', justifyContent: 'flex-end', gap: '1.5rem' }}>
          <li><Link to='/'> home </Link></li>
          <li><Link to='login'>login</Link></li>
          <li><Link to='signup'>signup</Link></li>
        </ul>
      </header>
      <main style={{ margin: 'auto' }}>
        <form onSubmit={handleSubmit}>
          <input type="file" name='file' /><br />
          <button type='submit'>upload</button>
        </form>
        <Outlet />
      </main>
      <footer style={{ marginTop: 'auto' }}>ATS &copy; mohanad & abdallah</footer>

    </div>

  )
}
export const router = createBrowserRouter(createRoutesFromElements(
  <Route path='/' element={<Layout />}>
    <Route index element={<App />} />
    <Route path='login' element={<Login />} />
    <Route path='signup' element={<Register />} />
    <Route path='verify' element={<Verify />} />
    <Route path='me' element={<Me />} />
  </Route>
));
export default App;
