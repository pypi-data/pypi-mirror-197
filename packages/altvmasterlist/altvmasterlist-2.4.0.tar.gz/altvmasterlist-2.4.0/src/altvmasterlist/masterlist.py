#!/usr/bin/env python3
from altvmasterlist import shared
from dataclasses import dataclass
from re import compile
import logging
import sys

logging.basicConfig(level=logging.INFO)
logging.getLogger().setLevel(logging.INFO)
# Masterlist API Docs: https://docs.altv.mp/articles/master_list_api.html
logging.debug(f'starting with base link: {shared.MasterlistUrls.base_link}')


# This is the server object
@dataclass
class Server:
    id: int
    active: bool = False
    maxPlayers: int = 0
    players: int = 0
    name: str = ""
    locked: bool = False
    host: str = ""
    port: int = 0
    gameMode: str = ""
    website: str = ""
    language: str = ""
    description: str = ""
    verified: bool = False
    promoted: bool = False
    useEarlyAuth: bool = False
    earlyAuthUrl: str = ""
    useCdn: bool = False
    cdnUrl: str = ""
    useVoiceChat: bool = False
    tags: list[str] = None
    bannerUrl: str = ""
    branch: str = ""
    build: str = ""
    version: float = 0.0
    lastUpdate: int = 0

    # initialize the object with all values that are available in the alt:V masterlist API
    def __init__(self, server_id, no_fetch=False):
        self.id = server_id

        if not no_fetch:
            temp_data = shared.request(shared.MasterlistUrls.server_link.format(self.id))
            if temp_data is None or temp_data == {} or not temp_data["active"]:
                # the api returned no data or the server is offline
                self.active = False
                self.players = 0
            else:
                self.active = temp_data["active"]
                self.maxPlayers = temp_data["info"]["maxPlayers"]
                self.players = temp_data["info"]["players"]
                self.name = temp_data["info"]["name"]
                self.locked = temp_data["info"]["locked"]
                self.host = temp_data["info"]["host"]
                self.port = temp_data["info"]["port"]
                self.gameMode = temp_data["info"]["gameMode"]
                self.website = temp_data["info"]["website"]
                self.language = temp_data["info"]["language"]
                self.description = temp_data["info"]["description"]
                self.verified = temp_data["info"]["verified"]
                self.promoted = temp_data["info"]["promoted"]
                self.useEarlyAuth = temp_data["info"]["useEarlyAuth"]
                self.earlyAuthUrl = temp_data["info"]["earlyAuthUrl"]
                self.useCdn = temp_data["info"]["useCdn"]
                self.cdnUrl = temp_data["info"]["cdnUrl"]
                self.useVoiceChat = temp_data["info"]["useVoiceChat"]
                self.tags = temp_data["info"]["tags"]
                self.bannerUrl = temp_data["info"]["bannerUrl"]
                self.branch = temp_data["info"]["branch"]
                self.build = temp_data["info"]["build"]
                self.version = temp_data["info"]["version"]
                self.lastUpdate = temp_data["info"]["lastUpdate"]

    # fetch the server data and replace it
    def update(self):
        self.__init__(self.id)

    # get the maximum player count with a specified time range
    # returns a JSON object e.g. [{"t":1652096100,"c":50},{"t":1652096400,"c":52},{"t":1652096700,"c":57}]
    # time: 1d, 7d, 31d
    def get_max(self, time: str = "1d"):
        return shared.request(shared.MasterlistUrls.server_max_link.format(self.id, time))

    # get the average player count with a specified time range
    # returns a JSON object e.g. [{"t":1652096100,"c":50},{"t":1652096400,"c":52},{"t":1652096700,"c":57}]
    # time: 1d, 7d, 31d
    # return result will return the average of all values e.g. 126
    def get_avg(self, time: str = "1d", return_result: bool = False):
        average_data = shared.request(shared.MasterlistUrls.server_average_link.format(self.id, time))
        if not average_data:
            return None

        if return_result:
            players_all = 0
            for entry in average_data:
                players_all = players_all + entry["c"]
            result = players_all / len(average_data)
            return round(result)
        else:
            return average_data

    @property
    def connect_json(self):
        return shared.fetch_connect_json(self.useCdn, self.locked, self.active, self.host, self.port, self.cdnUrl)

    @property
    def permissions(self):
        return shared.get_permissions(self.connect_json)

    def get_dtc_url(self, password=None):
        return shared.get_dtc_url(self.useCdn, self.cdnUrl, self.host, self.port, self.locked, password)

    def get_resource_size(self, resource, decimal=2):
        return shared.get_resource_size(self.useCdn, self.cdnUrl, resource, self.host, self.port, decimal)


# Fetch the stats of all servers that are currently online
# e.g. {"serversCount":121,"playersCount":1595}
def get_server_stats():
    data = shared.request(shared.MasterlistUrls.all_server_stats_link)
    if data is None:
        return None
    else:
        return data


# Get all Servers that are online as Server object
def get_servers():
    return_servers = []
    servers = shared.request(shared.MasterlistUrls.all_servers_link)
    if servers is None or servers == "{}":
        return None
    else:
        for server in servers:
            # Now change every JSON response to a server object that we can e.g. update it when we want
            tmp_server = Server(server["id"], no_fetch=True)
            tmp_server.active = True
            tmp_server.maxPlayers = server["maxPlayers"]
            tmp_server.players = server["players"]
            tmp_server.name = server["name"]
            tmp_server.locked = server["locked"]
            tmp_server.host = server["host"]
            tmp_server.port = server["port"]
            tmp_server.gameMode = server["gameMode"]
            tmp_server.website = server["website"]
            tmp_server.language = server["language"]
            tmp_server.description = server["description"]
            tmp_server.verified = server["verified"]
            tmp_server.promoted = server["promoted"]
            tmp_server.useEarlyAuth = server["useEarlyAuth"]
            tmp_server.earlyAuthUrl = server["earlyAuthUrl"]
            tmp_server.useCdn = server["useCdn"]
            tmp_server.cdnUrl = server["cdnUrl"]
            tmp_server.useVoiceChat = server["useVoiceChat"]
            tmp_server.tags = server["tags"]
            tmp_server.bannerUrl = server["bannerUrl"]
            tmp_server.branch = server["branch"]
            tmp_server.build = server["build"]
            tmp_server.version = server["version"]
            tmp_server.lastUpdate = server["lastUpdate"]
            return_servers.append(tmp_server)

        return return_servers


# validate a given alt:V server id
def validate_id(server_id):
    regex = compile(r"^[\da-zA-Z]{32}$")
    result = regex.match(server_id)
    if result is not None:
        return True
    else:
        return False


if __name__ == "__main__":
    print("This is a Module!")
    sys.exit()
