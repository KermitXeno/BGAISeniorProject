import React from 'react'
import { Routes, Route } from 'react-router-dom'
import { AuthProvider } from './contexts/AuthContext'
import Layout from './components/Layout'
import AgePlot from './components/agePlot'
import Home from './views/Home'
import About from './views/About'
import VueDemo from './views/VueDemo'
import Chat from './views/Chat'
import SignIn from './views/SignIn'
import CreateAccount from './views/CreateAccount'
import OurData from './views/OurData'

import './App.css'

function App() {
  return (
    <AuthProvider>
      <div className="App">
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<Home />} />
            <Route path="about" element={<About />} />
            <Route path="vue-demo" element={<VueDemo />} />
            <Route path="chat" element={<Chat />} />
            <Route path="signin" element={<SignIn />} />
            <Route path="create-account" element={<CreateAccount />} />
              <Route path="/data" element={<OurData />} />
              <Route path="/age-distribution" element={<AgePlot />} />


          </Route>
        </Routes>
      </div>
    </AuthProvider>
  )
}

export default App