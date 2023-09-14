import { useState, useEffect } from "react"
import { useQuery } from "react-query"
import { searchJobOffers, fetchCompanies } from "../api/queries"
import JobOfferListItem from "../components/JobOfferListItem"
import globals from "../globals"
import { useNavigate } from 'react-router-dom';
import { CompanySelect, EUser } from "../types"
import Cookies from "js-cookie"

export default function SignUp() {
    const [registerCompany, setRegisterCompany] = useState({
        company_name: '',
        password: '',
        job_interview_difficulty: '',
        capitalism_score: '',
        degree_of_despair: '',
    })
    const [registerDeveloper, setRegisterDeveloper] = useState({
        user_name: '',
        password: '',
        first_name: '',
        last_name: '',
        uwu_score: '',
        weebiness: '',
    })
    const [registerInterviewer, setRegisterInterviewer] = useState({
      user_name: '',
      password: '',
      first_name: '',
      last_name: '',
      strictness: '',
      kindness: '',
      exp: '',
      company: '',
      token: '',
  })
  const [radioOption, setRadioOption] = useState('')
  const [companies, setCompanies] = useState<CompanySelect[]>([]);
  const navigate = useNavigate();
  const updateCompanies = async () => {
    setCompanies(await fetchCompanies())
  }

  useEffect(() => {
    updateCompanies()
  },[])

      const handleRegCompChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setRegisterCompany({ ...registerCompany, [e.target.name]: e.target.value });
      };
      const handleRadioChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setRadioOption(e.target.value)
      }
      const handleRegDevChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setRegisterDeveloper({ ...registerDeveloper, [e.target.name]: e.target.value });
      };
      const handleRegIntervChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement> ) => {
        setRegisterInterviewer({ ...registerInterviewer, [e.target.name]: e.target.value });
      };
      
      const submitCompanyRegistration = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        // Handle form 2 submission
        console.log('Form 2 submitted:', registerCompany);
        // Call backend API or perform desired action
        try {
          Cookies.set("usertype",EUser.COMPANY)
          Cookies.set("username",registerCompany.company_name)
          Cookies.set("password",registerCompany.password)
          globals.usertype=EUser.COMPANY
          globals.username=registerCompany.company_name
          globals.password=registerCompany.password
            const response = await fetch(`https://localhost:443/api/register_company?company_name=${registerCompany.company_name}` +
            `&password=${registerCompany.password}` +
            `&job_interview_difficulty=${registerCompany.job_interview_difficulty}` +
            `&capitalism_score=${registerCompany.capitalism_score}` +
            `&degree_of_despair=${registerCompany.degree_of_despair}`, {
              method: 'POST',
              // Optionally, provide headers or other configurations if required
            });
        
            if (response.ok) {
              // Handle the successful response
              const data = await response.json();
              console.log('Response:', data);
              navigate("/login")
            } else {
              // Handle the error response
              console.error('Error:', response.status);
            }
          } catch (error) {
            // Handle any exceptions or network errors
            console.error('Error:', error);
          }
        // Reset form 2 input
        setRegisterCompany({
            company_name: '',
            password: '',
            job_interview_difficulty: '',
            capitalism_score: '',
            degree_of_despair: '',
        });
      };

      const submitDeveloperRegistration = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        // Handle form 2 submission
        console.log('Form 2 submitted:', registerDeveloper);
        // Call backend API or perform desired action
        try {
          Cookies.set("usertype",EUser.DEVELOPER)
          Cookies.set("username",registerDeveloper.user_name)
          Cookies.set("password",registerDeveloper.password)
          globals.usertype=EUser.DEVELOPER
          globals.username=registerDeveloper.user_name
          globals.password=registerDeveloper.password
            const response = await fetch(`https://localhost:443/api/register_developer?user_name=${registerDeveloper.user_name}` +
            `&password=${registerDeveloper.password}&first_name=${registerDeveloper.first_name}` +
            `&last_name=${registerDeveloper.last_name}&uwu_score=${registerDeveloper.uwu_score}` +
            `&weebiness=${registerDeveloper.weebiness}`, {
              method: 'POST',
              // Optionally, provide headers or other configurations if required
            });
        
            if (response.ok) {
              // Handle the successful response
              const data = await response.json();
              console.log('Response:', data);
              navigate("/login")
            } else {
              // Handle the error response
              console.error('Error:', response.status);
            }
          } catch (error) {
            // Handle any exceptions or network errors
            console.error('Error:', error);
          }
        // Reset form 2 input
        setRegisterDeveloper({
            user_name: '',
            password: '',
            first_name: '',
            last_name: '',
            uwu_score: '',
            weebiness: '',
        });
      };

      const submitInterviewerRegistration = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        // Handle form 2 submission
        console.log('Form 2 submitted:', registerInterviewer);
        // Call backend API or perform desired action
        try {
          Cookies.set("usertype",EUser.INTERVIEWER)
          Cookies.set("username",registerInterviewer.user_name)
          Cookies.set("password",registerInterviewer.password)
          globals.usertype=EUser.INTERVIEWER
          globals.username=registerInterviewer.user_name
          globals.password=registerInterviewer.password
            const response = await fetch(`https://localhost:443/api/register_interviewer?user_name=${registerInterviewer.user_name}` +
            `&password=${registerInterviewer.password}&first_name=${registerInterviewer.first_name}` +
            `&last_name=${registerInterviewer.last_name}&strictness=${registerInterviewer.strictness}` +
            `&kindness=${registerInterviewer.kindness}&exp=${registerInterviewer.exp}&company=${registerInterviewer.company}&token=${registerInterviewer.token}`, {
              method: 'POST',
              // Optionally, provide headers or other configurations if required
            });
        
            if (response.ok) {
              // Handle the successful response
              const data = await response.json();
              console.log('Response:', data);
              navigate("/login")
            } else {
              // Handle the error response
              console.error('Error:', response.status);
            }
          } catch (error) {
            // Handle any exceptions or network errors
            console.error('Error:', error);
          }
        // Reset form 2 input
        setRegisterInterviewer({
          user_name: '',
          password: '',
          first_name: '',
          last_name: '',
          strictness: '',
          kindness: '',
          exp: '',
          company: '',
          token: '',
        });
      };
      let registerForm = <p>Please select a Usertype</p>
      if(radioOption === 'company')
            registerForm =
                <form onSubmit={submitCompanyRegistration}>
                    <label>
                        Company Name:
                        <input
                        type="text"
                        value={registerCompany.company_name}
                        onChange={handleRegCompChange}
                        name="company_name"
                        />
                    </label>
                    <br/>
                    <label>
                        Password:
                        <input
                        type="password"
                        value={registerCompany.password}
                        onChange={handleRegCompChange}
                        name="password"
                        />
                    </label>
                    <br/>
                    <label>
                        Jobinterview Difficulty:
                        <input
                        type="number"
                        value={registerCompany.job_interview_difficulty}
                        onChange={handleRegCompChange}
                        name="job_interview_difficulty"
                        />
                    </label>
                    <br/>
                    <label>
                        Capitalism Score:
                        <input
                        type="number"
                        value={registerCompany.capitalism_score}
                        onChange={handleRegCompChange}
                        name="capitalism_score"
                        />
                    </label>
                    <br/>
                    <label>
                        Degree of Despair:
                        <input
                        type="number"
                        value={registerCompany.degree_of_despair}
                        onChange={handleRegCompChange}
                        name="degree_of_despair"
                        />
                    </label>
                    <br/>
                    <button type="submit">Register Company</button>
                </form>
       else if (radioOption === 'interviewer')
            registerForm = 
                <form onSubmit={submitInterviewerRegistration}>
                    <label>
                        Username:
                        <input
                        type="text"
                        value={registerInterviewer.user_name}
                        onChange={handleRegIntervChange}
                        name="user_name"
                        />
                    </label>
                    <br/>
                    <label>
                        Password:
                        <input
                        type="password"
                        value={registerInterviewer.password}
                        onChange={handleRegIntervChange}
                        name="password"
                        />
                    </label>
                    <br/>
                    <label>
                        First Name:
                        <input
                        type="text"
                        value={registerInterviewer.first_name}
                        onChange={handleRegIntervChange}
                        name="first_name"
                        />
                    </label>
                    <br/>
                    <label>
                        Last Name:
                        <input
                        type="text"
                        value={registerInterviewer.last_name}
                        onChange={handleRegIntervChange}
                        name="last_name"
                        />
                    </label>
                    <br/>
                    <label>
                        Strictness:
                        <input
                        type="number"
                        value={registerInterviewer.strictness}
                        onChange={handleRegIntervChange}
                        name="strictness"
                        />
                    </label>
                    <br/>
                    <label>
                        Kindness:
                        <input
                        type="number"
                        value={registerInterviewer.kindness}
                        onChange={handleRegIntervChange}
                        name="kindness"
                        />
                    </label>
                    <br/>
                    <label>
                        Experience:
                        <input
                        type="number"
                        value={registerInterviewer.exp}
                        onChange={handleRegIntervChange}
                        name="exp"
                        />
                    </label>
                    <br/>
                    <label>
                        Company:
                        <select value={registerInterviewer.company} onChange={handleRegIntervChange} name="company">
                        <option value="">-</option>
                        {companies.map(company => (
                            <option key={company.id} value={company.id}>{company.name}</option>
                        ))}
                        </select>
        
                    </label>
                    <br/>
                    <label>
                        Verification Token:
                        <input
                        type="text"
                        value={registerInterviewer.token}
                        onChange={handleRegIntervChange}
                        name="token"
                        />
                    </label>
                    <br/>
                    <button type="submit">Register Interviewer</button>
                </form>
        else if (radioOption === 'developer')
            registerForm =
                <form onSubmit={submitDeveloperRegistration}>
                    <label>
                        Username:
                        <input
                        type="text"
                        value={registerDeveloper.user_name}
                        onChange={handleRegDevChange}
                        name="user_name"
                        />
                    </label>
                    <br/>
                    <label>
                        Password:
                        <input
                        type="password"
                        value={registerDeveloper.password}
                        onChange={handleRegDevChange}
                        name="password"
                        />
                    </label>
                    <br/>
                    <label>
                        First Name:
                        <input
                        type="text"
                        value={registerDeveloper.first_name}
                        onChange={handleRegDevChange}
                        name="first_name"
                        />
                    </label>
                    <br/>
                    <label>
                        Last Name:
                        <input
                        type="text"
                        value={registerDeveloper.last_name}
                        onChange={handleRegDevChange}
                        name="last_name"
                        />
                    </label>
                    <br/>
                    <label>
                        UwU-Score:
                        <input
                        type="number"
                        value={registerDeveloper.uwu_score}
                        onChange={handleRegDevChange}
                        name="uwu_score"
                        />
                    </label>
                    <br/>
                    <label>
                        Weebiness:
                        <input
                        type="number"
                        value={registerDeveloper.weebiness}
                        onChange={handleRegDevChange}
                        name="weebiness"
                        />
                    </label>
                    <br/>
                    <button type="submit">Register Developer</button>
                </form>
    return <>
        <div>
            Register new Account:
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
        { registerForm }
    </>
}