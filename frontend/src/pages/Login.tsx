import { useState } from "react"
import { requestLogIn } from "../api/queries"
import globals from "../globals"
import { EUser } from "../types"
import { useNavigate } from 'react-router-dom';
import Cookies from 'js-cookie';

export default function LogIn() {
    const navigate = useNavigate();
    const [radioOption, setRadioOption] = useState('')
    const [logInInfo, setLogInInfo] = useState({
        name: '',
        pwd: '',
    })

   const tryLogIn = async (type: string, name: string, pwd: string) => {
        const data = await requestLogIn(type,name,pwd)
        if (data.successLogin) {
            switch (type) {
                case "i":
                    globals.usertype = EUser.INTERVIEWER
                    Cookies.set("usertype",EUser.INTERVIEWER)
                    break
                case "d":
                    Cookies.set("usertype",EUser.DEVELOPER)
                    Cookies.set("developerId",data.id.toString())
                    globals.usertype = EUser.DEVELOPER
                    globals.developerId = data.id
                    break
                case "c":
                    Cookies.set("usertype",EUser.COMPANY)
                    Cookies.set("companyId",data.id.toString())
                    globals.usertype = EUser.COMPANY
                    globals.companyId = data.id
            }
            globals.username = name
            globals.password = pwd
            navigate("/home")
        }
        return data.successLogin
    }

    const populate = async () => {
        try {
          const response = await fetch(`https://localhost:443/api/populate_db`, {
            method: 'POST',
            // Optionally, provide headers or other configurations if required
          });
      
          if (response.ok) {
            // Handle the successful response
            const data = await response.json();
            console.log('Response:', data);

            Cookies.remove("usertype")
            globals.usertype = EUser.NONE

            navigate("/login")
          } else {
            // Handle the error response
            console.error('Error:', response.status);
          }
        } catch (error) {
          // Handle any exceptions or network errors
          console.error('Error:', error);
        }
      }

    const handleRadioChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setRadioOption(e.target.value)
      }

    const handleLogInInfoChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setLogInInfo({ ...logInInfo, [e.target.name]: e.target.value })
    }

    const submitCompany = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()
        await tryLogIn('c',logInInfo.name,logInInfo.pwd)
        setLogInInfo({
            name: '',
            pwd: '',
        })
    }

    const submitDeveloper = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()
        await tryLogIn('d',logInInfo.name,logInInfo.pwd)
        setLogInInfo({
            name: '',
            pwd: '',
        })
    }

    const submitInterviewer = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()
        await tryLogIn('i',logInInfo.name,logInInfo.pwd)
        setLogInInfo({
            name: '',
            pwd: '',
        })
    }

      let loginForm = <p>Please select a Usertype</p>

      if(radioOption === 'company')
        loginForm = 
            <form onSubmit={submitCompany}>
                <label>
                Company Name:
                    <input
                    type="text"
                    value={logInInfo.name}
                    onChange={handleLogInInfoChange}
                    name="name"
                    />
                </label>
                <br/>
                <label>
                    Password:
                    <input
                    type="password"
                    value={logInInfo.pwd}
                    onChange={handleLogInInfoChange}
                    name="pwd"
                    />
                </label>
                <br/>
                <button type="submit">LogIn</button>
            </form>
      else if (radioOption === 'interviewer')
        loginForm = 
            <form onSubmit={submitInterviewer}>
                <label>
                Username:
                    <input
                    type="text"
                    value={logInInfo.name}
                    onChange={handleLogInInfoChange}
                    name="name"
                    />
                </label>
                <br/>
                <label>
                    Password:
                    <input
                    type="password"
                    value={logInInfo.pwd}
                    onChange={handleLogInInfoChange}
                    name="pwd"
                    />
                </label>
                <br/>
                <button type="submit">LogIn</button>
            </form>
      else if (radioOption === 'developer')
        loginForm = 
            <form onSubmit={submitDeveloper}>
                <label>
                Username:
                    <input
                    type="text"
                    value={logInInfo.name}
                    onChange={handleLogInInfoChange}
                    name="name"
                    />
                </label>
                <br/>
                <label>
                    Password:
                    <input
                    type="password"
                    value={logInInfo.pwd}
                    onChange={handleLogInInfoChange}
                    name="pwd"
                    />
                </label>
                <br/>
                <button type="submit">LogIn</button>
            </form>
    return <>
        <div>
            Login as:
        <label>
            <input
            type="radio"
            value="company"
            checked={radioOption === 'company'}
            onChange={handleRadioChange}
            />
            Company
        </label>

        <label>
            <input
            type="radio"
            value="interviewer"
            checked={radioOption === 'interviewer'}
            onChange={handleRadioChange}
            />
            Interviewer
        </label>

        <label>
            <input
            type="radio"
            value="developer"
            checked={radioOption === 'developer'}
            onChange={handleRadioChange}
            />
            Developer
        </label>
        </div>
        { loginForm }
        <br/>
        <button onClick={populate}>Populate</button>
    </>
}