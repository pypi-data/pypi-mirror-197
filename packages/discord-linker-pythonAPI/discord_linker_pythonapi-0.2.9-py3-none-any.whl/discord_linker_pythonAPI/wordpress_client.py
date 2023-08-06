from typing import Optional
import requests
import base64
import discord_linker_pythonAPI.errors as errors
import urllib3
import urllib3.exceptions


class WP_Client:
    """This client allows to connect and
    authenticate with wordpress's rest API.


    Args:
        url (str): The URL of the website.
        user (str): The user we will use to authenticate.
        password (str): The API password generated for this application.
        verify_requests (bool): Whether to verify SSL reequests or not.
    """

    def __init__(self, url:str, user:str, password:str, verify_requests:bool = True):
        self.wp_url = url.rstrip('/')

        self.wp_endpoints = {
            "DISCORD": "/discord_linker/v1/discord",
            "TOKENS": "/discord_linker/v1/tokens",
            "API": "/discord_linker/v1/api"
        }
        self.wp_header:dict = {}

        self.verify_requests = verify_requests
        if not verify_requests:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



        self.generate_header(user, password)

    

    def generate_header(self, user:str, password:str):
        """Generate the authentication header.

        Args:
            user (str): The username of the owner of this application.
            password (str): This application's password.
        """
        token = base64.b64encode((user + ':' + password).encode())
        header = {"Authorization": "Basic " + token.decode('utf-8')}
        self.wp_header = header
    


    def generate_request(self, endpoint:str, action:str, parameters:list[str]) -> str:
        """Generate the link for a rest request.

        Args:
            endpoint (str): The name of the endpoint to use. (see the keys of 'wp_endpoints' for a list of values)
            action (str): The name of the action to perform.
            parameters (list[str]): A list with the parameters that the API needs.

        Returns:
            str: A string with the URL that calls the API function.
        """

        # Translate every parameter to str
        parameters = [str(i) for i in parameters]

        return "{url}/index.php?rest_route={endpoint}/{actionAndParams}".format(
            url = self.wp_url,
            endpoint = self.wp_endpoints[endpoint],
            actionAndParams = '/'.join([action] + parameters)
        )
    

    def send_request(self, URL:str, request_type:str = "GET", data:Optional[dict] = None) -> dict:
        """Send a request of "request_type" to the "URL" with "data" as body.

        Args:
            URL (str): The URL that should receive the request.
            request_type (str, optional): The request type we should send. Defaults to "GET".
            data (Optional[dict], optional): The data we want to send. Defaults to None.

        Returns:
            dict: A dictionary created from the parsed json.
        """

        request_types = {
            "GET": requests.get,
            "POST": requests.post,
            "PUT": requests.put,
            "DELETE": requests.delete,
            "OPTIONS": requests.options,
            "HEAD": requests.head,
            "PATCH": requests.patch
        }


        return request_types[request_type](
            URL,
            headers = self.wp_header,
            json = data,
            verify = self.verify_requests
        ).json()
    

    def execute_and_check_errors(self, endpoint:str, action:str, parameters:list[str]) -> dict:
        """Send a request to the specified endpoint, calling
        the specified action with the specified parameters.

        Args:
            endpoint (str): The endpoint to use.
            action (str): The action to call.
            parameters (list[str]): The list with the parameters to pass.

        Raises:
            WP_Error: An Error thrown by the API.

        Returns:
            dict: A dictionary with the API's response.
        """
        status = self.send_request(self.generate_request(endpoint, action, parameters))
        if status['code'] != "SUCCESS":
            raise errors.get_exception(status)
        return status



    def discord_link(self, discord_id:str, link_token:str):
        """Link a discord account to a wordpress account using a link token.

        Args:
            discord_id (str): The ID of the discord account.
            link_token (str): The link token used to link the accounts.
        """
        self.execute_and_check_errors("DISCORD", "link", [discord_id, link_token])


    def discord_unlink(self, discord_id:str):
        """Unlink a discord account from the wordpress account it's linked with.

        Args:
            discord_id (str): The ID of the discord account we want to unlink.
        """
        self.execute_and_check_errors("DISCORD", "unlink", [discord_id])

    
    def token_delete(self, link_token:str):
        """Delete a link token.

        Args:
            link_token (str): The link token we want to delete.
        """
        self.execute_and_check_errors("TOKENS", "delete", [link_token])
    
    def token_list(self) -> list[str]:
        """Get a list with all active tokens for the logged in user.

        Returns:
            list[str]: A list containing all active tokens.
        """
        status = self.execute_and_check_errors("TOKENS", "get", [])
        return status["link_tokens"]
    
    def token_create(self) -> str:
        """Create a link token for the account we are connected as.

        Returns:
            str: The generated link token.
        """
        status = self.execute_and_check_errors("TOKENS", "create", [])
        return status['link_token']
    

    def get_account_details(self, discord_id:str) -> dict:
        """Get details about the connected account.

        Args:
            discord_id (str): The ID of the discord account.

        Returns:
            dict: The details of the linked user.
        """
        details = self.execute_and_check_errors("DISCORD", "get_account_details", [discord_id])

        return details['details']
    
    def check_credentials(self) -> bool:
        """Checks if the credentials are correct.

        Returns:
            bool: True if login was successful, False if login was not successful.
        """
        try:
            self.execute_and_check_errors("API", "credential_check", [])
        except errors.WP_Error:
            return False
        return True