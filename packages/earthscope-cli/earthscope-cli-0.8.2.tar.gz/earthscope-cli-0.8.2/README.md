# EarthScope CLI

A Typer CLI for authenticating with the EarthScope API
* [Getting Started](#Getting_Started)
  * [Requirements](#Requirements) 
  * [Installation](#Installation)
  * [Use the CLI with your user profile](#Use the CLI with your user profile) 
  * [Use the CLI with machine-to-machine client credentials](#Use the CLI with machine-to-machine client credentials) 
* [Example - Retrieve a file from the UNAVCO Data File Server](#Example)
  * [cURL](#curl)
  * [Wget](#wget)
* [FAQ/troubleshooting](#faq)

## Getting Started<a name="Getting_Started"></a>
### Requirements<a name="Requirements"></a>
   To use the CLI you must have:
   * Registered an account with Earthscope ([sign up now](https://data-idm.unavco.org/user/profile/login)!). See [here](https://www.unavco.org/data/gps-gnss/file-server/user-profile.html) for more information
   * Python >= 3.7
   * A bash-like shell (see [bash for windows](https://learn.microsoft.com/en-us/windows/wsl/install))
### Installation<a name="Installation"></a>

1. (Optional) Suggest setting up and activating a python virtual environment so as to not clutter your system python

   ```shell
   python3 -m venv venv
   . venv/bin/activate
   ```
   
2. Install the CLI:

   ```shell
   pip install earthscope-cli
   ```

3. Use the CLI. The package has a `console_scripts` section which makes a shortcut called `es` available in your python environment.

   ```shell
   es --help
   ```

### Use the CLI with your user profile<a name="Use the CLI with your user profile"></a>

#### **Login to EarthScope with Device Authorization Flow:**

```shell
es sso login
```
This will prompt your browser to open a device confirmation page with the same code displayed in the url shown on your command line.
If you are on a device that does not have a web browser, you can copy the displayed url in a browser on another device (personal computer, mobile device, etc...)
and complete the confirmation there.

The **login** command will save your token locally. If this token is deleted, you will need to re-authenticate (login) to retrieve your token again.
Run the following command to see where your token is stored:
```shell
es sso state --path
```

#### **get/refresh your access token**
```shell
es sso access --token
```
The **access** command will display your access token. If your access token is close to expiration or expired, 
the default behavior is to automatically refresh your token.

If you want to manually refresh your token:
```shell
es sso refresh
```

Never share your tokens. If you think your token has been compromised, please revoke your refresh token and re-authenticate (login):
```shell
es sso refresh --revoke
es sso login
```

#### **Get your user profile from the `user-management-api` running behind https://data-idm.unavco.org/user/profile/**
```shell
es user get
```

#### **Explore the CLI**
Use `--help` on any command to see more information on available commands and options.
```shell
es --help
es sso --help
es access --help
.
.
```

### Example: Retrieve a file from the UNAVCO Data File Server with cURL or Wget<a name="Example"></a>
* Step 1: login. This step is only required once (the first time you run the cli on your device) unless your access token is deleted from your device.
* Step 2: Retrieve your token using `es sso access --token`. Add this access token as an Authorization header with your cURL or Wget command.

<a name="curl"></a>
Example using cURL:
```shell
curl -L -O -f --url https://data-idm.unavco.org/archive/gnss/rinex/obs/1992/001/algo0010.92d.Z --header "authorization: Bearer $(es sso access --token)"
```
where

-L : follow redirects\
-O : uses server filename\
-f : (HTTP) Fail on error without server output. Error code 22 -- good for scripting

Make sure to include the -f or it will be difficult to tell if an error occured.


<a name="weget"></a>
Example using Wget:
```shell
wget https://data-idm.unavco.org/archive/gnss/rinex/obs/2022/060/p1230600.22d.Z --header "authorization: Bearer $(es sso access --token)"
```

See more [file server access examples](https://www.unavco.org/data/gps-gnss/file-server/file-server-access-examples.html)

If you would like to access files using python - please check out the [earthscope-sdk](https://gitlab.com/earthscope/public/earthscope-sdk/)

### FAQ/troubleshooting<a name="faq"></a>
* **How long does my access token last?**
  * Your access token lasts 8 hours. Once it is expired, your refresh token will need to be used to refresh your access token.
* **How long does my refresh token last?**
  * Your refresh token will never expire - unless you are inactive (do not use it) for one year. 
    If it does expire, you will need to re-authenticate to get a new access and refresh token.
* **What is a refresh token and how does the CLI use it?**
  * A refresh token is a special token that is used to renew your access token without you needing to log in again. 
    The refresh token is obtained from your access token, and using the `es sso access` command will automatically 
    renew your access token if it is close to expiration. You can 'manually' refresh your access token by using the command `es sso refresh`.
    If your access token is compromised, you can revoke your refresh token using `es sso refresh --revoke`. Once your access token expires, 
    it can no longer be renewed and you will need to re-login.
* **Should I hard-code my access token into my script?**
  * No. We recommend you use the cli commands to retrieve your access tokens in your scripts. 
  This way your access token will not be compromised by anyone viewing your script. 
  The access token only lasts 8 hours and cannot be used afterwards unless refreshed.

Please contact [data-help@earthscope.org](data-help@earthscope.org) with questions or issues.