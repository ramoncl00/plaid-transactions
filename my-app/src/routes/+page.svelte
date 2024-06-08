<script>
	import Login from "../components/Login.svelte";
	import {isAuthenticated, isAuthenticatedInPlaid, refreshToken} from "../services/authentication";
    import { PUBLIC_API_BASE_URL } from "$env/static/public";
	import Loading from "../components/Loading.svelte";
	import Transactions from "../components/Transactions.svelte";

	refreshToken();

	let loadError = ""
	let linkToken = ""
	let loading = false

	const checkPlaidToken = () => {
		let keyCreationTime = sessionStorage.getItem("key_creation_time")
		if(keyCreationTime != null){
			let last_time = Number.parseInt(keyCreationTime, 10)
			let difference = Date.now() - last_time
			let minutes = difference / (1000 * 60);

			if(minutes >= 30) {
				localStorage.removeItem("plaid_key")
				sessionStorage.removeItem("key_creation_time")
				location.reload()
			}
		}
	}

	const openPlaid = () => {
		loading = true

		let token = localStorage.getItem("bearer")

		fetch(`${PUBLIC_API_BASE_URL}/link-token?lang=en`, {
			headers: { Authorization: `Bearer ${token}` },
		})
			.then(async (response) => {
				if (response.status !== 200) {
					loadError = "There was an error getting data from Plaid";
					return
				}

				return response.json();
			})
			.then(data => {
				linkToken = data.link_token;

				// @ts-ignore
				const handler = Plaid.create({
					token: linkToken,
					// @ts-ignore
					onSuccess: async (publicToken, metadata) => {
						localStorage.setItem("plaid_key", publicToken)
						sessionStorage.setItem("key_creation_time", Date.now().toString())
						location.reload()
					},
					// @ts-ignore
					onEvent: (eventName, metadata) => {
						// pass
					},
					// @ts-ignore
					onExit: (error, metadata) => {
						// pass
					},
				});

				handler.open()
			})
			.catch((error) => {
				loadError = "There was an error getting data from Plaid";
			})
			.finally(() => {
				loading = false;
			});	
	}

</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

<section>
	{#if loading}
		<Loading/>
	{/if}

	{#if loadError !== ""}
		<h1 class="text-error">{loadError}</h1>
	{/if}

	{#if !isAuthenticated()}
		<Login/>
	{/if}

	{#if isAuthenticated()}
		{#if !isAuthenticatedInPlaid()}
			<input on:click={openPlaid} class="btn" type="button" value="Authenticate in plaid">
		{/if}
		{#if isAuthenticatedInPlaid()}
			<Transactions/>
		{/if}
	{/if}

</section>

<style>
	section {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		flex: 0.6;
	}

	.text-error {
		font-size: 18px;
		color: red;
		font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
	}

	.btn {
		border: solid 3px black;
		background: none;
		padding: 10px;
		border-radius: 5px;
		transition: background-color 0.1s ease, color 0.1s ease;
		cursor: pointer;
		font-family: var(--font-body),serif;
	}

	.btn:hover {
		color: orange;
		border-color: orange;
	}
</style>
