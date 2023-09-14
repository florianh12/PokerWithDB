import { useState } from "react"
import { JobOffer } from "../types"
import globals from "../globals"
import { useMarkJobOfferAsInterested } from "../api/mutations"


const JobOfferListItem = ({ jobOffer }: { jobOffer: JobOffer}) => {

    const [isInterested, setIsInterested] = useState(jobOffer.developer_interested)
    const [isLoading, setIsLoading] = useState(false)

    const markJobOfferAsInterested = useMarkJobOfferAsInterested()
    const markAsInterested = async () => {
        setIsLoading(true)
        await markJobOfferAsInterested.mutateAsync({
            companyId: jobOffer.company,
            offerId: jobOffer._id,
            developerId: globals.developerId
        })
        setIsInterested(true)
        setIsLoading(false)
    }

    let interestedButton = <button>Marking...</button>
    if (!isLoading) {
        interestedButton = isInterested ? <button>Interested</button> :  <button onClick={markAsInterested}>Mark as interested</button> 
    }

    return <li>
        <div>
            <h1>{jobOffer.title}</h1>
            { interestedButton }
            <div>
                <div>Pay: {jobOffer.pay}</div>
                <div>Begin: {jobOffer.begin_date ? jobOffer.begin_date.toString() : "not given"} </div>
                <div>End: {jobOffer.end_date ? jobOffer.end_date.toString() : "not given"} </div>
            </div>
            <p>{jobOffer.description}</p>
        </div>
    </li>
}

export default JobOfferListItem