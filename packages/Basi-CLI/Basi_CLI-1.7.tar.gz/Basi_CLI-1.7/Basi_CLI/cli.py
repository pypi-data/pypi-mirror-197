import click
import requests
import typer
import getpass

app = typer.Typer()

user_bucket_name = 'damg-test'
subscription_tiers = ['free', 'gold', 'platinum']
BASE_URL = 'http://34.74.233.133:8090'


@app.command("create_user")
def create_user():

    # Prompt the user for username
    username = typer.prompt("Enter username")

    # Make a request to the endpoint to check if the username already exists
    username_response = (requests.post(BASE_URL + f'/check-user-exists?username={username}')).json()
    status = username_response["user"]

    if status == False:
        typer.echo("Username already exists.")
        raise typer.Abort()

    # Prompt the user for password
    password = getpass.getpass(prompt='Enter password: ')
    
    # Prompt the user to re-enter password for verification
    password2 = getpass.getpass(prompt='Re-enter password: ')
    
    # Verify that the passwords match
    if password != password2:
        typer.echo("Passwords don't match.")
        raise typer.Abort()
    
    # Prompt the user for email
    email = typer.prompt("Enter email")

    # Prompt the user for full name
    full_name = typer.prompt('Enter full name: ')
    
    # Prompt the user to select a subscription tier
    plan = typer.prompt("Select subscription tier", type=click.Choice(subscription_tiers))

    response = requests.post(BASE_URL + f'/add-user?username={username}&password={password}&email={email}&full_name={full_name}&plan={plan}').json()
    output = response["user"]
    
    # Code to create user goes here
    typer.echo(output)


@app.command("download")
def download(filename: str):

    """
    Downloads a file with the specified filename and returns the URL of the file moved to your S3 location.
    """

    username = typer.prompt("Username: ")
    password = getpass.getpass(prompt='Password: ')

    url = "http://34.74.233.133:8090/token"
    json_data = {"username": username, "password": password}

    response = requests.post(url, data=json_data, auth=("client_id", "client_secret"))       
    if response.status_code == 200:
        typer.echo(f"Logged in as {username}")
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
    else:
        typer.echo("Invalid username or password")
        return



    # Make a request to the endpoint to check if call limit has exceeded
    username_response = (requests.post(BASE_URL + f'/check-users-api-record?username={username}')).json()
    status = username_response["user"]

    if (status):

        file_url_response = requests.post(BASE_URL + f'/download?filename={filename}', headers=headers).json()
        file_url = file_url_response["url"]       

        typer.echo(file_url) 

        requests.post(BASE_URL + f'/check-users-api-record?url="/download"&response={file_url}&username={username}')

    else:
        typer.echo("User limit reached! Please try later.")


@app.command("fetch_goes")
def fetch_goes(year: str, day: str, hour: str):
    """
    Lists all files in the specified bucket that match the file prefix and time parameters.
    """

    username = typer.prompt("Username: ")
    password = getpass.getpass(prompt='Password: ')

    url = "http://34.74.233.133:8090/token"
    json_data = {"username": username, "password": password}

    response = requests.post(url, data=json_data, auth=("client_id", "client_secret"))       
    if response.status_code == 200:
        typer.echo(f"Logged in as {username}")
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
    else:
        typer.echo("Invalid username or password")
        return

    # Make a request to the endpoint to check if call limit has exceeded
    username_response = (requests.post(BASE_URL + f'/check-users-api-record?username={username}')).json()
    status = username_response["user"]

    if (status):

        # Make a request to the endpoint to retrieve the list of files for the selected file prefix, year, day and hour
        file_list_response = (requests.post(BASE_URL + f'/list-files-goes?year={year}&day={day}&hour={hour}', headers=headers)).json()
        file_list = file_list_response["file_list"]

        typer.echo(f"Files in bucket GOES18 matching prefix ABI-L1b-RadC and time {year}-{day}T{hour}:00:00:")

        for file in file_list:
            typer.echo(file)

        requests.post(BASE_URL + f'/check-users-api-record?url="/fetch-goes"&response={file_list}&username={username}')

    else:
        typer.echo("User limit reached! Please try later.")


@app.command("fetch_nexrad")
def fetch_nexrad(year: str, month: str, day: str, station: str):
    """
    Lists all files in the specified bucket that match the file prefix and time parameters.
    """

    username = typer.prompt("Username: ")
    password = getpass.getpass(prompt='Password: ')

    url = "http://34.74.233.133:8090/token"
    json_data = {"username": username, "password": password}

    response = requests.post(url, data=json_data, auth=("client_id", "client_secret"))       
    if response.status_code == 200:
        typer.echo(f"Logged in as {username}")
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
    else:
        typer.echo("Invalid username or password")
        return

    # Make a request to the endpoint to check if call limit has exceeded
    username_response = (requests.post(BASE_URL + f'/check-users-api-record?username={username}')).json()
    status = username_response["user"]

    if (status):

        # Make a request to the endpoint to retrieve the list of files for the selected year, day and hour
        file_list_response = (requests.post(BASE_URL + f'/fetch-nexrad?year={year}&month={month}&day={day}&station={station}', headers=headers)).json()
        file_list = file_list_response["file_list"]

        typer.echo(f"Files in noaa-nexrad-level2 bucket matching the station {station} and date {day}-{month}-{year}")

        for file in file_list:
            typer.echo(file)

        requests.post(BASE_URL + f'/check-users-api-record?url="/fetch-nexrad"&response={file_list}&username={username}')

    else:
        typer.echo("User limit reached! Please try later.")


if __name__ == "__main__":
    app() 