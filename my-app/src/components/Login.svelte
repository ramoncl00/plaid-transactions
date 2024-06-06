<script src>
    import { PUBLIC_API_BASE_URL } from "$env/static/public";
    import Loading from "./Loading.svelte";

    let loading = false;

    let errors = {
        loginUsernameError: false,
        loginPasswordError: false,
        signUpUsernameError: false,
        signUpPasswordError: false,
        loginError: "",
        signUpError: ""
    };

    let signUpSuccess = false

    let loginCredentials = {
        username: "",
        password: "",
    };

    let signUpCredentials = {
        username: "",
        password: "",
    };

    const login = async () => {
        loading = true;
        signUpSuccess = false

        errors.loginUsernameError = false;
        errors.loginPasswordError = false;
        errors.loginError = ""

        if (loginCredentials.username === "") {
            errors.loginUsernameError = true;
            return;
        }

        if (loginCredentials.password === "") {
            errors.loginPasswordError = true;
            return;
        }

        try {
            let response = await fetch(`${PUBLIC_API_BASE_URL}/auth/login`, { 
                method: "POST", 
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username: loginCredentials.username,
                    password: loginCredentials.password
                })
            });

            var data = await response.json();

            if(response.status !== 200) {
                errors.loginError = data.detail
                loading = false
                return
            }

            localStorage.setItem("bearer", data.access);
            localStorage.setItem("refresh", data.refresh)
            loading = false;

            location.href = "/"
        } catch (ex) {
            console.error(ex);
            loading = false;
        }
    };

    const register = async () => {
        loading = true;
        signUpSuccess = false

        errors.signUpUsernameError = false;
        errors.signUpPasswordError = false;
        errors.signUpError = ""

        if (signUpCredentials.username === "") {
            errors.signUpUsernameError = true;
            loading = false
            return;
        }

        if (signUpCredentials.password === "") {
            errors.signUpPasswordError = true;
            loading = false
            return;
        }

        try {
            let response = await fetch(`${PUBLIC_API_BASE_URL}/auth/register`, { 
                method: "POST", 
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username: signUpCredentials.username,
                    password: signUpCredentials.password
                })
            });

            if(response.status !== 201) {
                errors.signUpError = "Error registering account, maybe another account with same username already exists"
                loading = false
                return
            }

            localStorage.clear()
            signUpSuccess = true
            loading = false;

            signUpCredentials.username = ""
            signUpCredentials.password = ""
        } catch (ex) {
            errors.signUpError = "Error registering account, maybe another account with same username already exists"
            console.error(ex);
            loading = false;
        }
    };
</script>

<div class="main">
    {#if loading}
        <Loading/>
    {/if}
    <input type="checkbox" id="chk" aria-hidden="true" />

    <div class="signup">
        <form>
            <label for="txt" aria-hidden="true">Sign up</label>
            {#if errors.signUpError !== ''}
                <p class="text-error">{errors.signUpError}</p>
            {/if}
            {#if signUpSuccess}
                <p class="text-success">Your account has been created successfully</p>
            {/if}
            <input
                bind:value={signUpCredentials.username}
                type="text"
                name="txt"
                placeholder="User name"
            />
            {#if errors.signUpUsernameError}
                <p class="text-error">User name cannot be empty</p>
            {/if}
            <input
                bind:value={signUpCredentials.password}
                type="password"
                name="pswd"
                placeholder="Password"
            />
            {#if errors.signUpPasswordError}
                <p class="text-error">Password cannot be empty</p>
            {/if}
            <button on:click={register}>Sign up</button>
        </form>
    </div>

    <div class="login">
        <form>
            <label for="chk" aria-hidden="true">Login</label>
            {#if errors.loginError != ''}
                <p class="text-error">{errors.loginError}</p>
            {/if}
            <input
                bind:value={loginCredentials.username}
                type="text"
                name="username"
                placeholder="User name"
            />
            {#if errors.loginUsernameError}
                <p class="text-error">User name cannot be empty</p>
            {/if}
            <input
                bind:value={loginCredentials.password}
                type="password"
                name="pswd"
                placeholder="Password"
            />
            {#if errors.loginPasswordError}
                <p class="text-error">Password cannot be empty</p>
            {/if}
            <button on:click={login}>Login</button>
            <label id="login-signup" for="chk" aria-hidden="true">Sign Up</label>
        </form>
    </div>
</div>

<style>
    .main {
        width: 350px;
        height: 500px;
        background: red;
        overflow: hidden;
        background: url("https://doc-08-2c-docs.googleusercontent.com/docs/securesc/68c90smiglihng9534mvqmq1946dmis5/fo0picsp1nhiucmc0l25s29respgpr4j/1631524275000/03522360960922298374/03522360960922298374/1Sx0jhdpEpnNIydS4rnN4kHSJtU1EyWka?e=view&authuser=0&nonce=gcrocepgbb17m&user=03522360960922298374&hash=tfhgbs86ka6divo3llbvp93mg4csvb38")
            no-repeat center/ cover;
        border-radius: 10px;
        box-shadow: 1px 3px 30px rgba(31, 24, 24, 0.46);
    }
    #chk {
        display: none;
    }
    .signup {
        position: relative;
        width: 100%;
        height: 100%;
    }
    label {
        color: #b65024;
        font-size: 2.3em;
        justify-content: center;
        display: flex;
        margin: 60px;
        font-weight: bold;
        cursor: pointer;
        transition: 0.5s ease-in-out;
    }
    input {
        width: 60%;
        height: 20px;
        background: #e0dede;
        justify-content: center;
        display: flex;
        margin: 20px auto;
        padding: 10px;
        border: none;
        outline: none;
        border-radius: 5px;
    }
    button {
        width: 60%;
        height: 40px;
        margin: 10px auto;
        justify-content: center;
        display: block;
        color: #fff;
        background: #b65024;
        font-size: 1em;
        font-weight: bold;
        margin-top: 20px;
        outline: none;
        border: none;
        border-radius: 5px;
        transition: 0.2s ease-in;
        cursor: pointer;
    }
    button:hover {
        background: #db8d6c;
    }
    .login {
        height: 460px;
        background: #eee;
        border-radius: 60% / 10%;
        transform: translateY(-180px);
        transition: 0.8s ease-in-out;
    }
    .login label {
        color: #b65024;
        transform: scale(0.6);
    }

    #chk:checked ~ .login {
        transform: translateY(-550px);
    }
    #chk:checked ~ .login label {
        transform: scale(1);
    }
    #chk:checked ~ .signup label {
        transform: scale(0.0);
    }
    .text-error {
        color: red;
        text-align: center;
    }
    .text-success {
        color: green;
        text-align: center;
    }
    #login-signup {
        scale: 0.6;
    }
</style>
