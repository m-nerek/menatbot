import requests
import os
from bs4 import BeautifulSoup

# Remember to update these if you change your creds (unlikely)
mc_username = os.getenv("mc_username")
mc_pass = os.getenv("mc_pass")
login_url = "https://mc.ggservers.com/site/login"
server_url = "https://mc.ggservers.com/server/53524"

class MinecraftManager:
    def __init__(self):
        """
        Class to manage handling the ggservers website.
        """
        self.session = requests.session()

    def login(self):
        """
        Login request. pretty straightforward
        :return:
        """
        r = self.session.get(login_url)
        soup = BeautifulSoup(r.text, "html.parser")
        # a = soup.find_all(name="YII_CSRF_TOKEN")
        login_data = {"LoginForm[name]": mc_username,
                      "LoginForm[password]": mc_pass,
                      "LoginForm[rememberMe]": "0",
                      "LoginForm[ignorehelp]": "0",
                      "YII_CSRF_TOKEN": soup.find("input", dict(name="YII_CSRF_TOKEN")).attrs['value'],
                      "yt0": "login"}
        return self.session.post(login_url,data=login_data)

    def start_server(self):
        """
        Starts the minecraft server, visits the server status page to get the CSRF token, then sends the start request.
        If sessions get confused, maybe consider rerunning init to clean it up.
        :return:
        """
        login_response = self.login()
        if login_response.status_code != "200":
            menato_response = "Something went wrong with the login. Ask Aster to investigate"
            return [menato_response]
        r = self.session.get(server_url)
        soup = BeautifulSoup(r.text, "html.parser")
        server_start = {
            "ajax": "start",
            "YII_CSRF_TOKEN": soup.find("input", dict(name="YII_CSRF_TOKEN")).attrs['value']
        }
        response = self.session.post(server_url, data=server_start)
        if response.status_code != "200":
            menato_response = "Something went wrong with the server start request. Ask Aster to investigate"
            return [menato_response]
        menato_response = "Server start requested, please wait 5s before trying to connect"
        return [menato_response]

    def server_status(self):
        """
        Thankfully, this nice little banner provides both IP and status, all in one, poggies!
        :return:
        """
        menato_response = "https://mc.ggservers.com/status/53524.png"
        return [menato_response]

    def stop_server(self):
        """
        Hook function for now, I'm not sure I wanna let these dolts dick around with turning it off
        :return:
        """
        r3 = self.session.get(server_url)
        soup = BeautifulSoup(r3.text, "html.parser")
        server_stop = {
            "ajax": "stop",
            "YII_CSRF_TOKEN": soup.find("input", dict(name="YII_CSRF_TOKEN")).attrs['value']
        }
        r4 = self.session.post(server_url, data=server_stop)

