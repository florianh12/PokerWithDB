import globals from "../globals"
import { useGetMarkedJobOffers, setGlobals } from "../api/queries"
import JobOfferListItem from "../components/JobOfferListItem"


export const MarkedJobOffers = () => {
    const { data, error, isLoading } = useGetMarkedJobOffers(globals.developerId)

    setGlobals()

    if (error)
        return <p>An error occurred, while fetching the data</p>

    if (isLoading)
        return <p>Loading job offers...</p>

    if (data)
        return <ul>
            { data?.map(jobOffer => <JobOfferListItem key={`${jobOffer.company}+${jobOffer._id}`} jobOffer={jobOffer}/>) }
        </ul>

    return <p>No job offers marked as &quot;interested in&quot;</p>
}