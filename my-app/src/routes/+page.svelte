<script>
	import Login from "../components/Login.svelte";
	import { isAuthenticated, refreshToken } from "../services/authentication";
    import { PUBLIC_API_BASE_URL } from "$env/static/public";
	import { onMount } from "svelte";
	import Loading from "../components/Loading.svelte";

	let loadError = ""
	let linkToken = ""
	let loading = false

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
						// pass
					},
					// @ts-ignore
					onEvent: (eventName, metadata) => {
						// pass
					},
					// @ts-ignore
					onExit: (error, metadata) => {
						location.href = "/about"
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

	onMount(() => {
		refreshToken();
		if(isAuthenticated())
			openPlaid();
	})

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
</style>
