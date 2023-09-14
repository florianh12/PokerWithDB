// https://www.w3schools.com/react/react_router.asp
import { Outlet, Link, useNavigate } from "react-router-dom"
import globals from "./globals"
import { EUser } from "./types"
import Cookies from 'js-cookie'
import { setGlobals } from "./api/queries"


const Routing = () => {
  const navigate = useNavigate()
  setGlobals()

  const logout = () => {
    Cookies.remove("usertype")
    globals.usertype = EUser.NONE
    navigate("/login")
  }

  return (
    <>
      <nav>
        <ul style={{listStyle: 'none'}}>
          <li>
            {
              globals.usertype != EUser.NONE ?
              <Link to="/home" reloadDocument style={{ width: '50px', marginRight: '25px' }}>Home</Link>
              : null
            } 
            {
              globals.usertype == EUser.DEVELOPER ?
              <>
                <Link to="/search" reloadDocument style={{ width: '50px', marginRight: '25px' }}>Search</Link>
                <Link to="/marked" reloadDocument style={{ width: '50px', marginRight: '25px' }}>Marked</Link>
              </>
              : null
            }
            {
            globals.usertype == EUser.NONE ?
            <>
              <Link to="/signup" style={{ width: '50px', marginRight: '25px' }}>Sign Up</Link>
              <Link to="/login" style={{ width: '50px', marginRight: '25px' }}>LogIn</Link>
            </>
            : <a onClick={logout}>LogOut</a>
            }
          </li>
        </ul>
      </nav>

      <Outlet />
    </>
  )
}

export default Routing