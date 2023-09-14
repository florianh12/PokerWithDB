import { useQuery } from "react-query"
import { baseUri } from "../consts"
import { JobOffer, Company, CompanySelect, EUser, ReportHejze, Key } from "../types"
import { useNavigate } from 'react-router-dom';
import globals from "../globals";
import Cookies from "js-cookie";


export const searchJobOffers = async (searchQuery: string, developerId: Key) => {
    const encodedSearchQuery = encodeURIComponent(searchQuery)
    return await fetch(`${baseUri}/search_job_offers?searchQuery=${encodedSearchQuery}&developerId=${developerId}`, { mode: "cors"})
        .then(res => res.json())
}

export const setGlobals = () => {
    const cookieValue = Cookies.get("usertype")
    console.log(cookieValue)
    switch (cookieValue) {
        case EUser.COMPANY.toString():
            globals.usertype = EUser.COMPANY
            break 
        case EUser.DEVELOPER.toString():
            globals.usertype = EUser.DEVELOPER
            break
        case EUser.INTERVIEWER.toString():
            globals.usertype = EUser.INTERVIEWER
            break
        default:
            globals.usertype = EUser.NONE
    }
    const u = Cookies.get("username")
    globals.username = u? u : ''
    const p = Cookies.get("password")
    globals.password = p? p : ''
    const ci = Cookies.get("companyId")
    globals.companyId = ci ? ci : ''
    const di = Cookies.get("developerId")
    globals.developerId = di? di : ''
}

export const useLoggedInRedirect = async () => {
    setGlobals()
    const navigate = useNavigate();

    setGlobals()
  
    if (globals.usertype === EUser.NONE) {
      navigate('/login');
      return;
    }
  
    const data = await requestLogIn(
      globals.usertype.toString(),
      globals.username,
      globals.password
    );
  
    if (!data.successLogin) {
      navigate('/login');
    }
  };


export const requestLogIn = async (type: string, name: string, pwd: string): Promise<{ successLogin: Boolean, id: Key}> => {
    return await fetch(`${baseUri}/login?type=${type}&name=${name}&pwd=${pwd}`, { mode: "cors"})
        .then(res => res.json())
}

export const fetchCompanies = async (): Promise<Array<CompanySelect>> => {
    return await fetch(`${baseUri}/get_companies`, { mode: "cors"})
        .then(res => res.json())
}

export const generateToken = async (tokenFor: Key) => {
    return await fetch(`${baseUri}/set_token?company_id=${tokenFor}`, { mode: "cors"})
        .then(res => res.json())
}

export const getReportHejze = async (reportFor: string): Promise<Array<ReportHejze>> => {
    return await fetch(`${baseUri}/report_hejze?company_id=${reportFor}`, { mode: "cors"})
        .then(res => res.json())
}

export const useGetMarkedJobOffers = (developerId: Key) => {
    return useQuery("get-marked-job-offers", async (): Promise<Array<JobOffer>> => {
        const res = await fetch(`${baseUri}/get_marked_job_offers?developerId=${developerId}`, { mode: "cors"})
            .then(res => res.json())
        if (!res.success) {
            console.log(res)
            throw Error(res.message)
        }
        return res.data
    })
}


export const useReportWild = (searchQuery: string = "") => {
    return useQuery("report-wild", async (): Promise<Array<Company>> => {
        const encodedSearchQuery = encodeURIComponent(searchQuery)
        const data = await fetch(`${baseUri}/report_wild?searchQuery=${encodedSearchQuery}`)
            .then(res => res.json())
        return data
    })
}
