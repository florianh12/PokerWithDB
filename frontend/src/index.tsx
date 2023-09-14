import React from 'react'
import {QueryClient, QueryClientProvider} from "react-query"
import ReactDOM from 'react-dom/client'
import {BrowserRouter, Routes, Route} from "react-router-dom"

import './styles/index.css'
import './styles/App.css';

import Home from "./pages/Home"
import NoPage from "./pages/NoPage"
import { JobSearch } from './pages/JobSearch'
import { MarkedJobOffers } from './pages/MarkedJobOffers'
import Routing from "./Routing"
import SignUp from './pages/SignUp'
import LogIn from './pages/Login'



export default function App() {
  const queryClient = new QueryClient()

  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Routing />}>
            <Route index element={<LogIn />} />
            <Route path="search" element={<JobSearch />} />
            <Route path="signup" element={<SignUp />} />
            <Route path="login" element={<LogIn />} />
            <Route path="home" element={<Home />} />
            <Route path="marked" element={<MarkedJobOffers />} />
            <Route path="*" element={<NoPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}


const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
)
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
