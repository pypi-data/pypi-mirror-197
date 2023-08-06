<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="static/logo/icon.jpg" alt="Project logo"></a>
</p>

<h3 align="center">Kami Google Drive</h3>

<div align="center">


[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![GitHub release](https://img.shields.io/github/release/devkami/kami-logging?include_prereleases=&sort=semver&color=blue)](https://github.com/devkami/kami-logging/releases/)
[![issues - kami-logging](https://img.shields.io/github/issues/devkami/kami-logging)](https://github.com/devkami/kami-logging/issues)
[![pulls - kami-logging](https://img.shields.io/github/pulls/devkami/kami-logging)](https://github.com/devkami/kami-logging/pulls)
[![License](https://img.shields.io/badge/License-GNU-blue)](#license)


</div>

---

<p align="center"> Simple functions to create folder and upload files using google drive api
    <br> 
</p>

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Deployment](#deployment)
- [Usage](#usage)
- [Built Using](#built_using)
- [TODO](../TODO.md)
- [Contributing](../CONTRIBUTING.md)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)

## 🧐 About <a name = "about"></a>

This package arose from the need to simplify the google drive management tasks of applications created by the Kami CO software development team.

Currently the package has 6 functions: get_service, connect, get_folder_id, create_folder, upload_file, upload_files

## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the package and a daily use example.

### Prerequisites

- python >= 3.9
- kami-logging >= 0.2.0
- google-api-core >= 2.11.0
- google-api-python-client >= 2.50.0
- google-auth-httplib2 >= 0.1.0
- google-auth-oauthlib >= 0.5.2
- google-auth >= 2.7.0
- googleapis-common-protos >= 1.56.2

### Installing

```terminal
$pip install kami-gdrive
```

## 🎈 Usage <a name="usage"></a>

To get work with this package first you need to create an project and an agent and get json file with correspondent credentials jus the way of google drive api documentation find [here](https://developers.google.com/drive/api/quickstart/python?hl=pt-br)

The 6 functions available are:

- _**get_service():**_

Get a service that communicates to a Google API.

Args:

- _api_name_ : The name of the api to connect to.
- _api_version_ : The api version to connect to.
- _scopes_ : A list auth scopes to authorize for the application.
- _key_file_location_ : The path to a valid service account JSON key file.

Returns: A service that is connected to the specified API.

- _**connect(service_account_credentials):**_

Connect with google drive api service.

Args:

- service_account_credentials : The path to a valid service account JSON key file.

Returns: A google drive api service.

- _**get_folder_id(parent_folder_id, folder_name):**_

Get id of a folder in driver if its exists.

Args:

- _parent_folder_id_ : Id to root or parent folder when search will begin.
- _folder_name_ : Searched folder name

Returns: Id to folder or None

- _**create_folder(parent_folder_id, folder_name):**_

- Create New Folder in especified parent folder.

Args:

- _parent_folder_id_ : Id to root or parent folder when new folder will be created.
- _folder_name_ : Name for the new folder

Returns: Id to new folder or None

- _**upload_file(folder_id, this_file):**_

- Upload an local file to especified folder on google drive.

Args:

- _folder_id_ : Id to the folder when this file will be uploaded.
- _this_file_ : Absolute or Relative full path to the local file.

Returns: Show an log with the result of process

- _**upload_files(folder_id, files_list):**_

- Upload an list of local file to especified folder on google drive.

Args:

- _folder_id_ : Id to the folder when this file will be uploaded.
- _files_list_ : List of Absolute or Relative full path to the each local file.

Returns: Show an log with the result of process

example:

```python
from kami_gdrive import create_folder, get_folder_id, upload_file
root_folder_id = '1eAnlW53WAOJn-eaLdM2AqRYnl0ui9qrL'
my_new_folder_id = create_folder(root_folder_id, 'my_new_folder')
local_file = 'Path/To/My/file.ext'
upload_file(my_new_folder_id, local_file)

```

Result:
<p align="center">
  <a href="" rel="noopener">
 <img src="static/example1.png" alt="Project logo"></a>
</p>

## ⛏️ Built Using <a name = "built_using"></a>

- [Python](https://www.python.org/) - Database
- [Logging](https://docs.python.org/3/library/logging.html) - Server Framework


## ✍️ Authors <a name = "authors"></a>

- [@maicondmenezes](https://github.com/maicondmenezes) - Idea & Initial work

See also the list of [contributors](https://github.com/devkami/kami-logging/contributors) who participated in this project.

## 🎉 Acknowledgements <a name = "acknowledgement"></a>

- References:
  - Arjancodes: [Github](https://github.com/ArjanCodes/), [Youtube](https://www.youtube.com/@ArjanCodes), [Twitter](https://twitter.com/arjancodes)
  - Eduardo Mendes: [Github](https://github.com/dunossauro), [Youtube](https://www.youtube.com/@Dunossauro), [Twitter](https://twitter.com/dunossauro)
