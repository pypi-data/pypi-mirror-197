import re

import requests

from ..visitor import Context, SiteVisitor
from ..helper import HTTP_REGEX


class Twitch(SiteVisitor):
    NAME = 'Twitch'
    URL_REGEX: re.Pattern = re.compile(HTTP_REGEX + r'twitch.tv/(?P<id>\w+)', re.IGNORECASE)

    def normalize(self, url: str) -> str:
        match = self.URL_REGEX.match(url)
        if match is None:
            return url
        return f'https://www.twitch.tv/{match.group("id")}'

    def visit(self, url, context: Context, id: str):
        url = f'https://www.twitch.tv/{id}'

        res = requests.get(url)
        match = re.search(r'clientId ?= ?"(?P<token>kimne78kx3ncx6brgo4mv6wki5h1ko)"', res.text)
        if match is None:
            print(f'[Twitch] Could not find token for {url}')
            return
        token = match.group('token')

        res = requests.post('https://gql.twitch.tv/gql', json=[
            {
                "operationName": "ChannelRoot_AboutPanel",
                "variables": {
                    "channelLogin": id,
                    "skipSchedule": True
                },
                "extensions": {
                    "persistedQuery": {
                        "version": 1,
                        "sha256Hash": "6089531acef6c09ece01b440c41978f4c8dc60cb4fa0124c9a9d3f896709b6c6"
                    }
                }
            }
        ], headers={
            'Client-Id': token,
        })

        info: Root = res.json()
        info

        info: Root = res.json()
        user = info[0]["data"]["user"]
        context.create_result('Twitch', url=url, name=user["displayName"], score=1.0, description=user["description"], profile_picture=user['profileImageURL'])

        for link in user['channel']["socialMedias"]:
            context.visit(link["url"])

from typing import List

from typing_extensions import TypedDict


class Followers(TypedDict):
    totalCount: int
    __typename: str


class SocialMediasItem0(TypedDict):
    id: str
    name: str
    title: str
    url: str
    __typename: str


class Channel(TypedDict):
    id: str
    socialMedias: List[SocialMediasItem0]
    __typename: str


class LastBroadcast(TypedDict):
    id: str
    game: None
    __typename: str


class Videos(TypedDict):
    edges: List
    __typename: str


class User(TypedDict):
    id: str
    description: str
    displayName: str
    isPartner: bool
    primaryColorHex: str
    profileImageURL: str
    followers: Followers
    channel: Channel
    lastBroadcast: LastBroadcast
    primaryTeam: None
    videos: Videos
    __typename: str


class Data(TypedDict):
    currentUser: None
    user: User


class Extensions(TypedDict):
    durationMilliseconds: int
    operationName: str
    requestID: str


class RootItem0(TypedDict):
    data: Data
    extensions: Extensions


Root = List[RootItem0]