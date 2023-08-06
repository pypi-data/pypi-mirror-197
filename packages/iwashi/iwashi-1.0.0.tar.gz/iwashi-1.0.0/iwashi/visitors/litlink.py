import json
import re
from typing import List, Union

import bs4
import requests
from typing_extensions import TypedDict

from ..helper import HTTP_REGEX
from ..visitor import Context, SiteVisitor


class LitLink(SiteVisitor):
    NAME = 'LitLink'
    URL_REGEX: re.Pattern = re.compile(HTTP_REGEX + r'lit\.link/(?P<id>\w+)', re.IGNORECASE)

    def normalize(self, url: str) -> str:
        match = self.URL_REGEX.match(url)
        if match is None:
            return url
        return f'https://lit.link/{match.group("id")}'

    def visit(self, url, context: Context, id: str):
        res = requests.get(f'https://lit.link/{id}')
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        data_element = soup.find(attrs={'id': '__NEXT_DATA__'})
        if data_element is None:
            print(f'[LitLink] Could not find data element for {url}')
            return
        data: Root = json.loads(data_element.get_text())
        profile: ProfileData = json.loads(data['props']['pageProps']['profileString'])

        context.create_result('LitLink', url=url, name=profile['name'], score=1.0, description=profile['profileText'], profile_picture=profile['pictureUrl'])

        for link in profile['snsIconLink']['details']:
            if 'url' not in link:
                continue
            context.visit(link['url'])


class Birthday(TypedDict):
    seconds: int
    nanoseconds: int


class SnsIconLink(TypedDict):
    details: Union[List, List['DetailsItem0']]


class ButtonLink(TypedDict):
    iconUrl: str
    title: str
    description: str
    url: str
    urlType: str


class DetailsItem0(TypedDict):
    linkType: str
    url: str


class CreatorDetailLayout(TypedDict):
    fontFamily: str
    fontColor: str
    fontSize: str
    textAlign: str
    backgroundImageUrl: str
    backgroundColor: str
    backgroundGradation: str
    backgroundOverlayColor: str
    linkShapeType: str
    linkShapeColor: str
    template: str


class CategorySettingsItem0(TypedDict):
    id: str
    name: str
    english: str


class GenreSettingsItem0(TypedDict):
    id: str
    name: str
    english: str
    category_settings: List[CategorySettingsItem0]
    categorySettings: List[CategorySettingsItem0]


class SnsActivitySetting(TypedDict):
    genreSettings: List[GenreSettingsItem0]


class ProfileData(TypedDict):
    uid: str
    name: str
    sex: str
    birthday: Birthday
    genre: str
    profileText: str
    url: str
    pictureUrl: str
    pictureType: str
    snsIconLink: SnsIconLink
    profileLink: SnsIconLink
    creatorDetailLayout: CreatorDetailLayout
    snsActivitySetting: SnsActivitySetting


class Account(TypedDict):
    email: str
    url: str
    emailUpdateResponse: None
    isLoading: bool
    emailConnected: bool
    urlUpdateResponse: None


class FontColor(TypedDict):
    r: int
    g: int
    b: int
    a: int


class CreatorDetailEdit(TypedDict):
    isEdit: bool
    editingProfile: None
    editingSnsIconLinkDetails: List
    editingProfileLinkDetails: List
    editingCreatorDetailLayout: None
    selectedBackgroundCategory: str
    fontColor: FontColor
    backgroundColor: FontColor
    backgroundGradationStartColor: FontColor
    backgroundGradationEndColor: FontColor
    backgroundGradationColorPaletteIndex: int
    isActiveUrlPastingOnText: bool
    linkShapeColor: FontColor
    profileLinkWidth: int
    isLoading: bool
    snsActivityGenres: List
    imageUpLoading: bool
    showSavedToast: bool
    toastText: str
    profileLinkUrlType: None
    profileLinkErrors: List
    modalSnsType: None
    snsModalDefaultUrl: str
    multipleImageLinkIndex: int
    fourImageLinkIndex: int
    selectedIndexOnImageOrSnsModal: int
    isCheckedOpenCategory: bool
    currentOpenedGenreIndex: int
    showIconQrCode: bool
    hasSavedProfile: bool
    backgroundImageUrlForOverlay: str


class GenreCategory(TypedDict):
    isLoading: bool
    selectedMoreThanOne: bool
    genreCategoryList: List
    openedGenreCategoryIds: List


class Profile(TypedDict):
    isLoggedIn: bool
    showCopiedMessage: bool
    showIconQrCode: bool
    profile: None


class LineLogin(TypedDict):
    lineLoginResponse: None
    isLoading: bool


class Login(TypedDict):
    loginResponse: None
    isLoading: bool
    loginErrorMessageId: None


class ConfirmationModalOptions(TypedDict):
    modalText: str
    positiveText: str
    negativeText: str


class SelectBackgroundImageModalOptions(TypedDict):
    isButtonLinkDesignImage: bool


class SelectImageModalOptions(TypedDict):
    isMultipleImageLink: bool
    isButtonLink: bool


class Modal(TypedDict):
    modalOpened: bool
    modalComponentName: str
    masterModalId: str
    confirmationModalOptions: ConfirmationModalOptions
    selectBackgroundImageModalOptions: SelectBackgroundImageModalOptions
    selectImageModalOptions: SelectImageModalOptions


class LineMessaging(TypedDict):
    lineMessaging: None
    isLoading: bool


class PasswordReminder(TypedDict):
    passwordReminderResponse: None
    isLoading: bool
    isCompletedSendEmail: bool
    hasErrorResponse: bool


class PasswordChange(TypedDict):
    passwordChangeResponse: None
    isLoading: bool


class SignUp(TypedDict):
    singUpAuthResponse: None
    signUpByLineResponse: None
    isLoading: bool
    registeredAlready: bool
    hasAccountByEmailAuth: bool
    defaultEmail: str
    hasErrorSignupResponse: bool


class FirebaseAuth(TypedDict):
    firebaseUser: None
    isAuthLoading: bool
    isResendEmailVerificationSucceeded: None


class SignupDetail(TypedDict):
    isInstagramConnected: bool
    isTwitterConnected: bool
    isLoading: bool
    isVerifiedUrl: None


class LineSignup(TypedDict):
    lineSignUpResponse: None
    isLoading: bool


class DatasetsItem0(TypedDict):
    label: str
    backgroundColor: str
    borderColor: str
    data: List


class UserGraphAccessLog(TypedDict):
    labels: List
    datasets: List[DatasetsItem0]


class Analytics(TypedDict):
    displayPeriod: str
    urlSortType: str
    topSortType: str
    isUrlSortAscendant: bool
    isTopSortAscendant: bool
    isReferralSortAscendant: bool
    isDeviceSortAscendant: bool
    pvCounts: int
    clickCounts: int
    accessTopTableSortType: str
    userTodayAccessLog: None
    userOneWeekAccessLog: None
    userOneMonthAccessLog: None
    userThreeMonthsAccessLog: None
    userSixMonthsAccessLog: None
    userOneYearAccessLog: None
    userAllAccessLog: None
    userGraphAccessLog: UserGraphAccessLog
    userUrlAccessLogs: List
    userTopAccessLogs: List
    userReferralAccessLogs: List
    userDeviceAccessLogs: List
    isAnalyticsStateLoading: bool
    urlAddedAreaHeight: int
    topAddedAreaHeight: int
    referralAddedAreaHeight: int
    isShowingMoreOnUrl: bool
    isShowingMoreOnTop: bool
    isShowingMoreOnReferral: bool
    isAnalyticsApiError: bool
    isShowingToast: bool
    apiError: None


class Notification(TypedDict):
    isLoading: bool
    selectedNotification: None


class CreatorDetailEditTutorial(TypedDict):
    editingCreatorPreferance: None
    tutorialCount: int
    isTutorialButtonEditDone: bool
    isTutorialLinkDraggerDone: bool
    isTutorialLinkEditDone: bool


class AccountDelete(TypedDict):
    isLoading: bool
    isSucceededDelete: None


class ProfileImageNftModal(TypedDict):
    pass


class SignupGenre(TypedDict):
    isSucceeded: None
    isLoading: bool


class InitialState(TypedDict):
    account: Account
    creatorDetailEdit: CreatorDetailEdit
    genreCategory: GenreCategory
    profile: Profile
    lineLogin: LineLogin
    login: Login
    modal: Modal
    lineMessaging: LineMessaging
    passwordReminder: PasswordReminder
    passwordChange: PasswordChange
    signUp: SignUp
    firebaseAuth: FirebaseAuth
    signupDetail: SignupDetail
    lineSignup: LineSignup
    analytics: Analytics
    notification: Notification
    creatorDetailEditTutorial: CreatorDetailEditTutorial
    accountDelete: AccountDelete
    profileImageNFTModal: ProfileImageNftModal
    signupGenre: SignupGenre


class PageProps(TypedDict):
    initialState: InitialState
    profileString: str
    ogpImageUrl: str


class Props(TypedDict):
    pageProps: PageProps
    __N_SSP: bool


class Query(TypedDict):
    creatorUrl: str


class Root(TypedDict):
    props: Props
    page: str
    query: Query
    buildId: str
    isFallback: bool
    gssp: bool
    locale: str
    locales: List[str]
    defaultLocale: str
    scriptLoader: List
