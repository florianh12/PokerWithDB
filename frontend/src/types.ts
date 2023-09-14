import { type } from "os"

export type Key = string | number

export type JobOffer = {
    company: Key,
    _id: Key,
    title: string,
    description: string,
    pay: number,
    begin_date: Date,
    end_date: Date,
    interviewer: Key,
    developer_interested: boolean,

    company_name: string,
    interviewer_name: string
}

export type Company = {
    id: Key,
    name: string,
    count_interested_developers: number
}

export type CompanySelect = {
    id: Key,
    name: string,
}

export enum EUser {
    NONE = 'NONE',
    DEVELOPER = 'd',
    COMPANY = 'c',
    INTERVIEWER = 'i'
  };
export type ReportHejze = {
    first_name: string,
    last_name: string,
    strictness: number,
    kindness: number,
    exp: number,
    blocked_devs: number
}