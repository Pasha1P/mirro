import { BrowserRouter, Navigate, Route, Routes } from 'react-router'
import './App.css'
import './main.js'
import React, { useEffect, useState } from 'react'
import Login from './pages/Login'
import Registration from './pages/Registration'

export type ContextType = {
  XCSRFToken: string,
  token: string,
  setToken: (token: string) => void
}
export const Context = React.createContext<ContextType>({
  XCSRFToken: '',
  token: '',
  setToken: () => { }
})

function App() {
  const [XCSRFToken, setXCSRFToken] = useState('')
  const [token, setToken] = useState('')

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/get_xcsrf/', { method: 'GET', credentials: 'include' })
      .then(res => { return res.json() })
      .then((data) => {
        console.log(data)
        console.log(data['X-CSRFToken'])
        setXCSRFToken(data['X-CSRFToken']);
      })
      .catch(() => { setXCSRFToken('') })
  }, [])

  return (
    <>
      <Context.Provider value={{ XCSRFToken, token, setToken }}>
        <BrowserRouter>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/registration" element={<Registration />} />
            <Route path="/boards" element={<Registration />} />
            <Route path='*' element={<Navigate to="/login" replace />} />
          </Routes>
        </BrowserRouter>
      </Context.Provider>
    </>
  )
}

export default App
