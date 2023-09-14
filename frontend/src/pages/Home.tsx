import { useState, useEffect } from 'react'
import { useMigrateDB } from '../api/mutations'
import { fetchCompanies, generateToken, getReportHejze, setGlobals } from "../api/queries"
import { CompanySelect, EUser, ReportHejze } from '../types'
import { useQuery } from 'react-query'
import { baseUri } from '../consts'
import globals from '../globals'
import { useNavigate } from 'react-router-dom'
import Cookies from 'js-cookie';


const Home = () => {
    const [searchQuery, setSearchQuery] = useState("")
    const [companies, setCompanies] = useState<CompanySelect[]>([])
    const [tokenFor, setTokenFor] = useState("")
    const [reportFor, setReportFor] = useState(companies.length > 0 ? String(companies[0].id) : "1")
    const [tokenValue, setTokenValue] = useState("None generated yet, one-time-use only!")
    const [isMigrating, setIsMigrating] = useState(false)
    const navigate = useNavigate()

    useEffect(() => {
        fetchCompanies().then(data => setCompanies(data))
    }, []);

    const { data, error, isLoading } = useQuery(["report-hejze", reportFor], async (): Promise<Array<ReportHejze>> => {
      return await getReportHejze(reportFor)
    })

    setGlobals()

    let reportDataHTML = <p>No data found!</p>


    if (error)
      reportDataHTML = <p>An error occurred, while fetching the data</p>
    else if (isLoading)
      reportDataHTML = <p>Loading report Hejze...</p>
    else if (data && data?.length > 0) {
      reportDataHTML = (
        <table>
          <thead>
            <tr>
              <th>First Name</th>
              <th>Last Name</th>
              <th>Strictness</th>
              <th>Kindness</th>
              <th>Experience</th>
              <th>Developers Blocked</th>
            </tr>
          </thead>
          <tbody>
            {data.map((interviewer, index) => (
              <tr key={index}>
                <td>{interviewer.first_name}</td>
                <td>{interviewer.last_name}</td>
                <td>{interviewer.strictness}</td>
                <td>{interviewer.kindness}</td>
                <td>{interviewer.exp}</td>
                <td>{interviewer.blocked_devs}</td>
              </tr>
            ))}
          </tbody>
        </table>
      );
    }
    
    const requestToken = async () => {
      if(globals.usertype === EUser.COMPANY) {
        console.log("ID:",globals.companyId)
        setTokenValue(await generateToken(globals.companyId))
      }
    }
    let tokenHTML = null
    if(globals.usertype === EUser.COMPANY)
      tokenHTML =  <p>Generate Company token:<br/><button type='button' onClick={requestToken}>Generate Token</button><br/> {tokenValue}</p>
    
    
    const migrateDataBase = useMigrateDB()
    const migrate = async () => {
      setIsMigrating(true)
      migrateDataBase.mutateAsync()
      Cookies.remove("usertype")
      globals.usertype = EUser.NONE
      navigate("/login")
    }

    const reportWild = () => {
      const encodedSearchQuery = encodeURIComponent(searchQuery)
      window.location.href = `${baseUri}/report_wild?searchQuery=${encodedSearchQuery}`
    }

    return <>
        <h1>Home</h1>
        <br/>
          <button onClick={migrate}>{ isMigrating ? "Migrating..." : "Migrate Database" }</button>
        <br/>
        Request Report Wild:
          <label>job type: <input value={searchQuery} onChange={e => setSearchQuery(e.target.value)}/></label>
          <button onClick={reportWild}>Report Wild</button>
        <br/>
        Request Report Hejze:
            <label>
                Company:
                <select value={reportFor} onChange={e => setReportFor(e.target.value)} name="report">
                  {companies.map(company => (
                    <option key={company.id} value={company.id}>{company.name}</option>
                  ))}
                </select>
            </label>
            <br/>
        { reportDataHTML }
        <br/>
          {tokenHTML}
    </>
}

export default Home