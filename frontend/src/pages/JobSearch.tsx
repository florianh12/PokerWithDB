import { JobOffer } from "../types"
import { useEffect, useState } from "react"
import { useQuery } from "react-query"
import { searchJobOffers, setGlobals } from "../api/queries"
import JobOfferListItem from "../components/JobOfferListItem"
import globals from "../globals"


export const JobSearch = () => {
    const [ searchQuery, setSearchQuery ] = useState("")
    const { data, error, isLoading } = useQuery(["search-job-offers", searchQuery], async (): Promise<Array<JobOffer>> => {
        return await searchJobOffers(searchQuery, globals.developerId)
    })

    setGlobals()

    let queryResult = <p>No job offers found for the search query</p>

    if (error)
        queryResult = <p>An error occurred, while fetching the data</p>
    else if (isLoading)
        queryResult = <p>Loading job offers...</p>
    else if (data && data?.length > 0)
        queryResult = <ul>
            { data?.map(jobOffer => <JobOfferListItem key={`${jobOffer.company}+${jobOffer._id}`} jobOffer={jobOffer}/>) }
        </ul>

    return <>
    <h1>Search</h1>
        <div>
            <input 
                type="text" 
                placeholder="Search..." 
                value={searchQuery} 
                onChange={e => setSearchQuery(e.target.value)}/>
        </div>
        { queryResult }
    </>
}