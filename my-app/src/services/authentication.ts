import { browser } from "$app/environment"
import { PUBLIC_API_BASE_URL } from "$env/static/public"

export const isAuthenticated = () => {
    if(browser) {
        let token = localStorage.getItem("bearer")
        return token != null
    }

    return false
}

export const refreshToken = async () => {
    if(browser) {
        console.log("Refreshing token")
        let token = localStorage.getItem("refresh")
        console.log("Refresh token: " + token)
        try{
            let response = await fetch(`${PUBLIC_API_BASE_URL}/auth/refresh`, {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    refresh: token
                })
            })

            if(response.status != 200) {
                console.log(`Error refreshing token: ${response.status}`)
                return
            }

            let data = await response.json()

            localStorage.setItem("bearer", data.access)
        } catch(err) {
            console.log(err)
        }
    }
}