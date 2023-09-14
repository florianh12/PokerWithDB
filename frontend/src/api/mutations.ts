import { useMutation } from "react-query"
import { baseUri } from "../consts"
import { Key } from "../types"


const sendRequest = (uri: string) => {
    return async () => {
        const res = await fetch(uri, { 
            method: "POST",                
        })
            .then(res => res.json())
        if (res.hasOwnProperty("success") && !res.success)
            throw Error(res.message)
        return res.message
    }
}


export const usePopulateDB = () => {
    return useMutation("populate-db", sendRequest(`${baseUri}/populate_db`))
}


export const useMigrateDB = () => {
    return useMutation("migrate-db", sendRequest(`${baseUri}/migrate_db`))
}


type markJobOfferParams = {
    companyId: Key, 
    offerId: Key, 
    developerId: Key
}

export const useMarkJobOfferAsInterested = () => {
    return useMutation("mark-joboffer-as-interested", async (args: markJobOfferParams) => {
        const uri = `${baseUri}/mark_job_offer_as_interested?companyId=${args.companyId}&offerId=${args.offerId}&developerId=${args.developerId}`
        const res = await fetch(uri, { 
            method: "PUT",
            mode: "cors",
        })
            .then(res => res.json())
        if (res.hasOwnProperty("success") && !res.success)
            throw Error(res.message)
        return res.message
    })
}