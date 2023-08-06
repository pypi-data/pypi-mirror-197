# -*- coding: utf-8 -*-
"""
Module for Google Drive Tools to Kami CO.
"""

import logging
from os import getenv, listdir
from os.path import isdir, isfile, join
from os.path import split as split_filename
from typing import List, Union

from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileDownload
from kami_logging import benchmark_with, logging_with

gdrive_logger = logging.getLogger('kami_gdrive')
load_dotenv()


@benchmark_with(gdrive_logger)
@logging_with(gdrive_logger)
def get_service(
    api_name: str, api_version: str, scopes: List[str], key_file_location: str
):
    """
    Get a service that communicates to a Google API.

    Args:
      api_name: The name of the api to connect to.
      api_version: The api version to connect to.
      scopes: A list auth scopes to authorize for the application.
      key_file_location: The path to a valid service account JSON key file.
    Returns:
      A service that is connected to the specified API.
    """
    credentials = service_account.Credentials.from_service_account_file(
        key_file_location
    )
    scoped_credentials = credentials.with_scopes(scopes)
    service = build(api_name, api_version, credentials=scoped_credentials)
    return service


@benchmark_with(gdrive_logger)
@logging_with(gdrive_logger)
def connect(service_account_credentials: str):
    """
    Create a google api client with google drive api using json file with the credentials

    Args:
        service_account_credentials: path to json file with google credentials

    Returns:
        google client api with google drive api
    """
    gdrive = get_service(
        api_name='drive',
        api_version='v3',
        scopes=['https://www.googleapis.com/auth/drive'],
        key_file_location=service_account_credentials,
    )

    return gdrive


@benchmark_with(gdrive_logger)
@logging_with(gdrive_logger)
def get_folder_id(parent_folder_id: str, folder_name: str) -> str:
    """
    Get google drive folder id if it's exists inside of a given google drive root folder

    Args:
        parent_folder_id: ID of a valid Google Drive folder that will be the root of the search
        folder_name: searched folder name

    Returns:
        Id of searched folder if it's exists or None

    Examples:
        >>> get_folder_id('1eAnlW53WAOJn-eaLdM2AqRYnl0ui9qrL', '2023')
        '1sinkAFgApspYOgpPbUKM9e4fCbYHKQZa'
    """
    gdrive = connect(getenv('SERVICE_ACCOUNT_CREDENTIALS'))
    response = (
        gdrive.files()
        .list(
            q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and '{parent_folder_id}' in parents",
            spaces='drive',
            fields='files(id, name)',
        )
        .execute()
    )

    folders = response.get('files', [])

    if folders:
        return folders[0].get('id')

    return None


@benchmark_with(gdrive_logger)
@logging_with(gdrive_logger)
def create_folder(parent_folder_id: str, new_folder_name: str) -> str:
    """
    Create new folder if not exists inside of a given google drive root folder

    Args:
        parent_folder_id: ID of a valid Google Drive folder that will be the root of the new
        new_folder_name: new folder name

    Returns:
        Id of new folder

    Examples:
        >>> create_folder('1eAnlW53WAOJn-eaLdM2AqRYnl0ui9qrL', '2023')
        '1sinkAFgApspYOgpPbUKM9e4fCbYHKQZa'
    """

    gdrive = connect(getenv('SERVICE_ACCOUNT_CREDENTIALS'))
    folder_id = get_folder_id(parent_folder_id, new_folder_name)

    if not folder_id:
        file_metadata = {
            'name': new_folder_name,
            'parents': [parent_folder_id],
            'mimeType': 'application/vnd.google-apps.folder',
        }
        file = gdrive.files().create(body=file_metadata, fields='id').execute()
        folder_id = file.get('id')

    return folder_id


@benchmark_with(gdrive_logger)
@logging_with(gdrive_logger)
def upload_file_to(source: str, destiny: str):
    """
    Download a file to a given google drive folder

    Args:
        folder_id: ID of a valid Google Drive folder that will be receive the file
        filename: fullpath filename

    Examples:
        >>> upload_file_to('1sinkAFgApspYOgpPbUKM9e4fCbYHKQZa', 'tests/test.file')

    """
    gdrive = connect(getenv('SERVICE_ACCOUNT_CREDENTIALS'))
    mime_types = '*/*'
    filepath, filename = split_filename(filename)

    file_metadata = {'name': filename, 'parents': [folder_id]}
    media = MediaFileDownload(join(filepath, filename), mimetype=mime_types)
    gdrive_logger.info(f'Downloading {filename}')
    gdrive.files().create(
        body=file_metadata, media_body=media, fields='id'
    ).execute()


@benchmark_with(gdrive_logger)
@logging_with(gdrive_logger)
def upload_files_to(source: Union[List[str], str], destiny: str, ) -> int:
    """
    Download a list of files to a given google drive root folder

    Args:
        source: ID of a valid Google Drive folder that will be receive the files
        destiny: A list with fullpath file names or a path to a folder

    Returns:
        Amount of uploaded files

    Examples:
        >>> upload_files_to('1sinkAFgApspYOgpPbUKM9e4fCbYHKQZa', 'tests/')
        2

    """
    files = source
    amount_of_uploaded_files = 0
    if isdir(source):
        files = [
            source + '/' + f
            for f in listdir(source)
            if isfile(join(source, f))
        ]

    for this_file in files:
        upload_file_to(destiny, this_file)
        amount_of_uploaded_files += 1

    return amount_of_uploaded_files
