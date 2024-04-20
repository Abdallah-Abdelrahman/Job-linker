import { useEffect, useState } from 'react'
import reactLogo from './assets/react.svg'
import './App.css'

function App() {
  const [msg, setMsg] = useState('')

  useEffect(()=>{
      fetch('/hello')
      .then(resp => resp.json())
      .then(data => setMsg(data))
      .catch(err => console.log({err}))
      }, [])

  return (
    <>
      <div>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Flask + React</h1>
      <div className="card">
        <h1>This {msg} is from flask</h1>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
}

export default App
