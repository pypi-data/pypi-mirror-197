#!/usr/bin/env python3
from altvmasterlist import shared
from dataclasses import dataclass
from re import compile
import logging
import sys

logging.basicConfig(level=logging.INFO)
logging.getLogger().setLevel(logging.INFO)
# Masterlist API Docs: https://docs.altv.mp/articles/master_list_api.html
logging.debug(f'starting with base link: {shared.AltstatsUrls.base_link}')


# This is the server object
@dataclass
class Server:
    Id: int
    FoundAt: str = ""
    LastActivity: bool = False
    Visible: bool = False
    ServerId: str = ""
    Players: int = 0
    Name: str = ""
    Locked: bool = False
    Ip: str = ""
    Port: int = 0
    MaxPlayers: int = 0
    Ping: int = 0
    Website: str = ""
    Language: str = ""
    Description: str = ""
    LastUpdate: int = 0
    IsOfficial: bool = False
    PlayerRecord: int = 0
    PlayerRecordDate: str = ""
    LastFetchOnline: bool = False
    LanguageShort: str = ""
    GameMode: str = ""
    Branch: str = ""
    Build: int = 0
    CdnUrl: str = ""
    EarlyAuthUrl: str = ""
    Verified: bool = False
    UseCdn: bool = False
    UseEarlyAuth: bool = False
    BannerUrl: str = ""
    Promoted: bool = False
    Tags: list[str] = None
    UseVoiceChat: bool = False
    Level: int = 0
    Version: float = 0.0

    # initialize the object with all values that are available in the alt:V masterlist API
    def __init__(self, server_id, no_fetch=False):
        self.Id = server_id

        if not no_fetch:
            temp_data = shared.request(shared.AltstatsUrls.server_link.format(self.Id))
            if temp_data is None or temp_data == {} or not temp_data["LastUpdate"]:
                # the api returned no data or the server is offline
                self.LastActivity = False
                self.Players = 0
            else:
                self.FoundAt = temp_data["FoundAt"]
                self.LastActivity = temp_data["LastActivity"]
                self.Visible = temp_data["Visible"]
                self.ServerId = temp_data["ServerId"]
                self.Players = temp_data["Players"]
                self.Name = temp_data["Name"]
                self.Locked = temp_data["Locked"]
                self.Ip = temp_data["Ip"]
                self.Port = temp_data["Port"]
                self.MaxPlayers = temp_data["MaxPlayers"]
                self.Ping = temp_data["Ping"]
                self.Website = temp_data["Website"]
                self.Language = temp_data["Language"]
                self.Description = temp_data["Description"]
                self.LastUpdate = temp_data["LastUpdate"]
                self.IsOfficial = temp_data["IsOfficial"]
                self.PlayerRecord = temp_data["PlayerRecord"]
                self.PlayerRecordDate = temp_data["PlayerRecordDate"]
                self.LastFetchOnline = temp_data["LastFetchOnline"]
                self.LanguageShort = temp_data["LanguageShort"]
                self.GameMode = temp_data["GameMode"]
                self.Branch = temp_data["Branch"]
                self.Build = temp_data["Build"]
                self.CdnUrl = temp_data["CdnUrl"]
                self.EarlyAuthUrl = temp_data["EarlyAuthUrl"]
                self.Verified = temp_data["Verified"]
                self.UseCdn = temp_data["UseCdn"]
                self.UseEarlyAuth = temp_data["UseEarlyAuth"]
                self.BannerUrl = temp_data["BannerUrl"]
                self.Promoted = temp_data["Promoted"]
                self.Tags = temp_data["Tags"]
                self.UseVoiceChat = temp_data["UseVoiceChat"]
                self.Level = temp_data["Level"]
                self.Version = temp_data["Version"]

    # fetch the server data and replace it
    def update(self):
        self.__init__(self.Id)

    @property
    def connect_json(self):
        return shared.fetch_connect_json(self.UseCdn, self.Locked, self.LastFetchOnline, self.Ip, self.Port, self.CdnUrl)

    @property
    def permissions(self):
        return shared.get_permissions(self.connect_json)

    def get_dtc_url(self, password=None):
        return shared.get_dtc_url(self.UseCdn, self.CdnUrl, self.Ip, self.Port, self.Locked, password)

    def get_resource_size(self, resource, decimal=2):
        return shared.get_resource_size(self.UseCdn, self.CdnUrl, resource, self.Ip, self.Port, decimal)


# Fetch the stats of all servers that are currently online
# e.g. [
#   {
#     "ServerCount": 72,
#     "PlayerCount": 958,
#     "TimeStamp": "2021-01-01T12:15:00.464Z"
#   },
#   {
#     "ServerCount": 73,
#     "PlayerCount": 945,
#     "TimeStamp": "2021-01-01T12:10:00.465Z"
#   },
#   {
#     "others": "..."
#   }
# ]
def get_server_stats():
    data = shared.request(shared.AltstatsUrls.all_server_stats_link)
    if data is None:
        return None
    else:
        return data


# Get all Servers that are online as Server object
def get_servers():
    return_servers = []
    servers = shared.request(shared.AltstatsUrls.all_servers_link)
    if servers is None or servers == "{}":
        return None
    else:
        for server in servers:
            # Now change every JSON response to a server object that we can e.g. update it when we want
            tmp_server = Server(server["id"], True)
            tmp_server.Name = server["name"]
            tmp_server.Locked = bool(server["locked"])
            tmp_server.Players = server["playerCount"]
            tmp_server.MaxPlayers = server["slots"]
            tmp_server.gameMode = server["gameMode"]
            tmp_server.language = server["language"]
            tmp_server.IsOfficial = bool(server["official"])
            tmp_server.Verified = bool(server["verified"])
            tmp_server.Promoted = bool(server["promoted"])
            tmp_server.Tags = server["tags"]
            return_servers.append(tmp_server)

        return return_servers


# validate a given alt:V server id
def validate_id(server_id):
    server_id = str(server_id)
    regex = compile(r"^\d+$")
    result = regex.match(server_id)
    if result is not None:
        return True
    else:
        return False


if __name__ == "__main__":
    print("This is a Module!")
    sys.exit()
