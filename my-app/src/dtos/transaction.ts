export interface Transaction {
    amount: number
    iso_currency_code: string
    category: string[]
    date: string
    authorized_date: string
    name: string
    merchant_name: string
    pending: boolean
}