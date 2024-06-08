<script lang="ts">
import DatePicker from "$lib/images/NicePng_free-estimate-png_948285.png";
import type {Transaction} from "../dtos/transaction";
import {PUBLIC_API_BASE_URL} from "$env/static/public";
import Loading from "./Loading.svelte";
import NoResults from "$lib/images/icons8-nothing-found-100.png"


let startDate = new Date()
let endDate = new Date()
let loading = false
let loadingError = ""

let transactions: Transaction[] = []
let dateRegex = /^\d{4}-\d{2}-\d{2}$/

let last_transactions = sessionStorage.getItem("last_transactions")
if(last_transactions != null) {
    transactions = JSON.parse(last_transactions)
}

const searchTransactions = () => {
    loadingError = ""

    if(!dateRegex.test(endDate.toString()) || !dateRegex.test(startDate.toString())){
        loadingError = "Dates are in a bad format, please enter a valid date"
        return
    }

    loading = true

    let public_key = localStorage.getItem("plaid_key")
    let token = localStorage.getItem("bearer")

    fetch(`${PUBLIC_API_BASE_URL}/transactions`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
            public_key: public_key,
            start_date: startDate,
            end_date: endDate,
        })
    })
        .then(response => response.json())
        .then((data: Transaction[]) => {
            transactions = data.map(x => x)
            sessionStorage.setItem("last_transactions", JSON.stringify(transactions))
        })
        .catch(error => {
            loadingError = "There was an error getting data from Plaid";
        })
        .finally(() => {
            loading = false
        })
}

</script>


<div class="container">
    {#if loading} <Loading/> {/if}
    {#if loadingError !== ""} <p class="text-error">{loadingError}</p> {/if}
    <div class="date-inputs">
        <div>
            <p>Start date</p>
            <input bind:value={startDate} style="background: url({DatePicker}) no-repeat center;" type="date" id="start-date" placeholder="Start Date">
        </div>
        <div>
            <p>End date</p>
            <input bind:value={endDate} style="background: url({DatePicker}) no-repeat center;" type="date" id="end-date" placeholder="End Date">
        </div>
    </div>
    <div class="transactions" id="transactions">
        {#if transactions.length !== 0}
            {#each transactions as transaction}
                <div class="card">
                    <div class="transaction-amount">${transaction.amount}</div>
                    <div class="transaction-category">Category: {#each transaction.category as category} {category} {/each}</div>
                    <div class="transaction-date">Date: {transaction.date}</div>
                    <div class="transaction-name">Transaction Name: {transaction.name}</div>
                    <div class="transaction-merchant">Merchant: {transaction.merchant_name}</div>
                    {#if transaction.pending}
                        <div class="transaction-pending">Status: Pending</div>
                    {/if}
                    {#if !transaction.pending}
                        <div class="transaction-completed">Status: Completed</div>
                    {/if}
                </div>
            {/each}
        {/if}
        {#if transactions.length === 0}
            <div class="no-results">
                <img alt="No results found" src="{NoResults}">
                <p>No results found</p>
            </div>
        {/if}
    </div>
    <input on:click={searchTransactions} type="button" class="btn" value="List transactions">
</div>

<style>
    .btn {
        border: solid 3px black;
        background: none;
        padding: 10px;
        border-radius: 5px;
        transition: background-color 0.1s ease, color 0.1s ease;
        cursor: pointer;
        width: 100%;
        font-family: var(--font-body),serif;
    }

    .btn:hover {
        color: orange;
        border-color: orange;
    }

    input[type="date"] {
        appearance: none;
        -webkit-appearance: none;
        -moz-appearance: none;
        background-color: #fff;
        border: 1px solid #ccc;
        border-radius: 4px;
        padding: 10px;
        font-size: 16px;
        color: #000000;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
        outline: none;
    }

    input[type="date"]::-webkit-calendar-picker-indicator {
        cursor: pointer;
    }

    input[type="date"]:hover, input[type="date"]:focus {
        border-color: #007bff;
        box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
    }

    input[type="date"]:focus {
        border-color: #0056b3;
        box-shadow: 0 0 5px rgba(0, 86, 179, 0.5);
    }

    .container {
        background-color: #fff;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        width: 400px;
    }

    .transactions {
        border: 1px solid #ccc;
        border-radius: 4px;
        padding: 10px;
        min-height: 100px;
        max-height: 400px;
        overflow-y: auto;
        margin-bottom: 20px;
        background-color: #f9f9f9;
    }

    .date-inputs {
        display: flex;
    }

    .date-inputs div {
        flex-grow: 1;
        text-align: center;
        margin: 5px;
    }

    .date-inputs div p {
        font-family: var(--font-body),serif;
    }

    .card {
        border: 1px solid #ccc;
        border-radius: 5px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .transaction-amount {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .transaction-category {
        margin-bottom: 5px;
    }
    .transaction-date {
        color: #888;
    }
    .transaction-name {
        font-weight: bold;
    }
    .transaction-merchant {
        color: #555;
    }
    .transaction-pending {
        color: red;
        font-weight: bold;
    }

    .transaction-completed {
        color: green;
        font-weight: bold;
    }

    .text-error {
        text-align: center;
        color: red;
        font-family: Arial, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    }

    .no-results {
        text-align: center;
    }
</style>