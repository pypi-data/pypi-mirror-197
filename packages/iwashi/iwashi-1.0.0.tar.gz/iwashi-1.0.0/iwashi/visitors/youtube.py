from typing import List, Union
import re
from typing import List

import requests
from typing_extensions import TypedDict
from yt_dlp import YoutubeDL
from urllib import parse

from ..visitor import Context, SiteVisitor
from ..helper import HTTP_REGEX

ytdlp = YoutubeDL({
    "quiet": True
})


class Youtube(SiteVisitor):
    NAME = 'Youtube'
    URL_REGEX: re.Pattern = re.compile(HTTP_REGEX + r'(m\.)?(youtube\.com|youtu\.be)', re.IGNORECASE)

    def normalize(self, url: str) -> str:
        info = ytdlp.extract_info(url, download=False, process=False)
        if info is None:
            return url
        if info['extractor'] == 'youtube:tab':
            return info.get('uploader_url') or self.normalize(info['url'])
        return info.get('uploader_url') or info.get('channel_url') # type: ignore

    def visit(self, url, context: Context):
        info = ytdlp.extract_info(url, download=False, process=False)
        assert info
        if 'channel_url' not in info:
            print(f'[Youtube] could not find channel_url for {url}')
            return
        if info['channel_url'] != url:
            info = ytdlp.extract_info(info['channel_url'], download=False, process=False)
            assert info

        context.mark_visited(info['channel_url'])

        profile_picture = None
        if 'thumbnails' in info and len(info['thumbnails']) > 0:
            for thumbnail in info['thumbnails']:
                if 'id' in thumbnail and thumbnail['id'] == 'avatar_uncropped':
                    profile_picture = thumbnail['url']
                    break
            else:
                profile_picture = info['thumbnails'][0]['url']

        context.create_result('Youtube', url=info['channel_url'], score=1.0, name=info['uploader'], description=info['description'], profile_picture=profile_picture)

        res = requests.get(f'{info["channel_url"]}/about')
        match = re.search(r'\"innertubeApiKey\": ?\"(?P<key>\w+)\"', res.text)
        if match is None:
            return

        key = match.group('key')
        about_res = requests.post(f'https://www.youtube.com/youtubei/v1/browse?key={key}&prettyPrint=False', json={
            "context": {
                "client": {
                    "clientName": "WEB",
                    "clientVersion": "2.20201021.01.00",
                    "device": {
                        "deviceCategory": "WEB",
                    },
                    "originalUrl": "https://www.youtube.com/@krr/about"
                }
            },
            'browseId': info['uploader_id']
        })
        about = about_res.json()
        header: Root = about['header']
        if 'headerLinks' not in header['c4TabbedHeaderRenderer']:
            return
        header_links = header['c4TabbedHeaderRenderer']['headerLinks']['channelHeaderLinksRenderer']
        for link in header_links.get('primaryLinks', []) + header_links.get('secondaryLinks', []):
            url = link['navigationEndpoint']['urlEndpoint']['url']
            if url.startswith('https://www.youtube.com/redirect'):
                context.visit(parse.unquote('&q='.join(url.split('&q=')[1:])))
            else:
                context.visit(url)


class WebCommandMetadata(TypedDict):
    url: str
    webPageType: str
    rootVe: int
    apiUrl: str


class CommandMetadata(TypedDict):
    webCommandMetadata: Union[WebCommandMetadata, 'WebCommandMetadata1']


class BrowseEndpoint(TypedDict):
    browseId: str
    canonicalBaseUrl: str


class NavigationEndpoint(TypedDict):
    clickTrackingParams: str
    commandMetadata: CommandMetadata
    browseEndpoint: Union[BrowseEndpoint, 'BrowseEndpoint1']


class ThumbnailsItem0(TypedDict):
    url: str
    width: int
    height: int


class Avatar(TypedDict):
    thumbnails: Union[List['ThumbnailsItem01'], List[ThumbnailsItem0]]


class WebCommandMetadata1(TypedDict):
    url: str
    webPageType: str
    rootVe: int


class UrlEndpoint(TypedDict):
    url: str
    target: str
    nofollow: bool


class NavigationEndpoint1(TypedDict):
    clickTrackingParams: str
    commandMetadata: CommandMetadata
    urlEndpoint: UrlEndpoint


class ThumbnailsItem01(TypedDict):
    url: str


class Title(TypedDict):
    simpleText: str


class PrimaryLinksItem0(TypedDict):
    navigationEndpoint: NavigationEndpoint1
    icon: Avatar
    title: Title


class ChannelHeaderLinksRenderer(TypedDict):
    primaryLinks: List[PrimaryLinksItem0]
    secondaryLinks: List[PrimaryLinksItem0]


class HeaderLinks(TypedDict):
    channelHeaderLinksRenderer: ChannelHeaderLinksRenderer


class AccessibilityData(TypedDict):
    label: str


class Accessibility(TypedDict):
    accessibilityData: AccessibilityData


class SubscriberCountText(TypedDict):
    accessibility: Accessibility
    simpleText: str


class RunsItem0(TypedDict):
    text: str


class ChannelHandleText(TypedDict):
    runs: List[RunsItem0]


class BrowseEndpoint1(TypedDict):
    browseId: str
    params: str
    canonicalBaseUrl: str


class MoreIcon(TypedDict):
    iconType: str


class ChannelTaglineRenderer(TypedDict):
    content: str
    maxLines: int
    moreLabel: str
    moreEndpoint: NavigationEndpoint
    moreIcon: MoreIcon


class Tagline(TypedDict):
    channelTaglineRenderer: ChannelTaglineRenderer


class C4TabbedHeaderRenderer(TypedDict):
    channelId: str
    title: str
    navigationEndpoint: NavigationEndpoint
    avatar: Avatar
    banner: Avatar
    headerLinks: HeaderLinks
    subscriberCountText: SubscriberCountText
    tvBanner: Avatar
    mobileBanner: Avatar
    trackingParams: str
    channelHandleText: ChannelHandleText
    style: str
    videosCountText: ChannelHandleText
    tagline: Tagline


class Root(TypedDict):
    c4TabbedHeaderRenderer: C4TabbedHeaderRenderer
