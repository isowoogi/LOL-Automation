import httplib2
import os
import random
import time

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow
from tqdm import tqdm
from entities.match_data import MatchData


class UploadYoutube:
    def __init__(self, match_data: MatchData, video_file_name: str) -> None:
        self.__thumb_file = os.path.abspath(r'.\media\thumb\thumb.png')
        self.__file = video_file_name
        # self.__title = (f"{match_data['mvp']['champion']} {match_data['player_role']} vs {match_data['loser']} - {match_data['region']} {match_data['mvp']['rank']} Patch ")
        role_map = {
            'Top': '탑',
            'Jungle': '정글',
            'Mid': '미드',
            'ADC': '원딜',
            'Support': '서폿'
        }
        tier_map = {
            'Iron': '아이언',
            'Bronze': '브론즈',
            'Silver': '실버',
            'Gold': '골드',
            'Platinum': '플래티넘',
            'Emerald': '애메랄드',
            'Diamond': '다이아몬드',
            'Master': '마스터',
            'GrandMaster': '그랜드마스터',
            'Challenger': '챌린저'
        }

        translated_role = role_map.get(match_data['player_role'], 'Unknown')
        korean_tier = tier_map.get(match_data['mvp']['rank'], 'Unknown')
        self.__title=f"""롤 {korean_tier} {translated_role} {match_data['mvp']['champion']} "{match_data['mvp']['name']}" | Patch {match_data['patch']}"""
        self.__description = f"""
    {match_data['mvp']['champion']} {match_data['player_role']} played by {match_data['mvp']['name']} at #{match_data['region']}{match_data['mvp']['rank']}

    * 좋아요와 구독은 큰 힘이 됩니다! / Don't forget to subscribe! : https://bit.ly/3cVxpsK
    """
        self.__category = "20"
        self.__keywords = [f"{match_data['mvp']['champion']}", "challenger",
                           "leagueoflegends", "replay", "high kda",
                           f"{match_data['region']}"]
        httplib2.RETRIES = 1
        self.__MAX_RETRIES = 10
        self.__RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error)
        self.__RETRIABLE_STATUS_CODES = [500, 502, 503, 504]
        self.__CLIENT_SECRETS_FILE = "./credentials/client_secrets.json"
        self.__YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
        self.__YOUTUBE_API_SERVICE_NAME = "youtube"
        self.__YOUTUBE_API_VERSION = "v3"
        self.__VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")
        self.__MISSING_CLIENT_SECRETS_MESSAGE = f"""
        WARNING: Please configure OAuth 2.0

        To make this sample run you will need to populate the client_secrets.json file
        found at:

          {os.path.abspath(os.path.join(os.path.dirname(__file__),
                                          self.__CLIENT_SECRETS_FILE))}

        with information from the API Console
        https://console.developers.google.com/

        For more information about the client_secrets.json file format, please visit:
        https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
        """

    def upload_video(self):
        try:
            self.__initialize_upload()
        except HttpError as e:
            print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")

    def __upload_thumbnail(self, youtube, video_id):
        print('Uploading youtube thumnail...')
        youtube.thumbnails().set(
            videoId=video_id,
            media_body=self.__thumb_file
        ).execute()

    def __build_video_data(self):
        return {
            "file": self.__file,
            "title": self.__title,
            "description": self.__description,
            "category": self.__category,
            "keywords": self.__keywords,
            "privacyStatus": self.__VALID_PRIVACY_STATUSES[1]
        }
    def progress_bar(self,progress):
        self.pbar.update(progress - self.pbar.n)
        
    def __get_authenticated_service(self):
        flow = flow_from_clientsecrets(self.__CLIENT_SECRETS_FILE,
                                       scope=self.__YOUTUBE_UPLOAD_SCOPE,
                                       message=self.__MISSING_CLIENT_SECRETS_MESSAGE)

        storage = Storage("./credentials/storage-oauth2.json")
        credentials = storage.get()

        if credentials is None or credentials.invalid:
            credentials = run_flow(flow, storage)

        return build(self.__YOUTUBE_API_SERVICE_NAME, self.__YOUTUBE_API_VERSION,
                     http=credentials.authorize(httplib2.Http()))

    def __initialize_upload(self):
        # print('===== Video uploading section ========')
        youtube = self.__get_authenticated_service()
        options = self.__build_video_data()
        tags = None
        if options['keywords']:
            tags = options['keywords']

        body = dict(
            snippet=dict(
                title=options['title'],
                description=options['description'],
                tags=tags,
                categoryId=options['category']
            ),
            status=dict(
                privacyStatus=options['privacyStatus']
            )
        )
        # Set chunksize to 1 MB  nochunk -1 it mean upload at once
        chunksize =-1
        
        insert_request = youtube.videos().insert(
            part=",".join(body.keys()),
            body=body,
            media_body=MediaFileUpload(
                options['file'], chunksize=chunksize, resumable=True)
        )

        video_id = self.__resumable_upload(insert_request)
        self.__upload_thumbnail(youtube, video_id)

    def __resumable_upload(self, insert_request):
        response = None
        error = None
        retry = 0
        while response is None:
            print("=== Video uploding (wait until uploading finishe) ===")
            try:
                # print("Uploading file...")
                status, response = insert_request.next_chunk()
                if response is not None:
                    if 'id' in response:
                        print(
                            f"Video id {response['id']} was successfully uploaded.")
                        return response['id']
                    else:
                        exit(
                            f"The upload failed with an unexpected response: {response}")
            except HttpError as e:
                if e.resp.status in self.__RETRIABLE_STATUS_CODES:
                    error = f"A retriable HTTP error {e.resp.status} occurred:\n{e.content}"
                else:
                    raise
            except self.__RETRIABLE_EXCEPTIONS as e:
                error = f"A retriable error occurred: {e}"

            if error is not None:
                print(error)
                retry += 1
                if retry > self.__MAX_RETRIES:
                    exit("No longer attempting to retry.")

                max_sleep = 2 ** retry
                sleep_seconds = random.random() * max_sleep
                print(f"Sleeping {sleep_seconds} seconds and then retrying...")
                time.sleep(sleep_seconds)
