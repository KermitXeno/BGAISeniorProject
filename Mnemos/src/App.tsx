import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Home from './views/Home'
import About from './views/About'
import VueDemo from './views/VueDemo'
import Chat from './views/Chat'
import SignIn from './views/SignIn'
import CreateAccount from './views/CreateAccount'
import './App.css'

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="about" element={<About />} />
          <Route path="vue-demo" element={<VueDemo />} />
          <Route path="chat" element={<Chat />} />
          <Route path="signin" element={<SignIn />} />
          <Route path="create-account" element={<CreateAccount />} />

        </Route>
      </Routes>
    </div>
  )
}

export default App