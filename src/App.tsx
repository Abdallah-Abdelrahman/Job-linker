import Login from "./Login";
import Register from "./Register";
import "./App.css";
import { Link, Outlet, Route, createBrowserRouter, createRoutesFromElements } from "react-router-dom";

const App = () => {
  return (
    <div className="App">
      <h1>Job Linker</h1>
    </div>
  );
};
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
  </Route>
))
export default App;
