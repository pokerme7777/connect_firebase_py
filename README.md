# connect_firebase_py
## About connecting firebase using Python

- A Python Env
- Connecting with Firebase Admin
- Retrieve data to local folder

A key point, Firebase Stroage is actually Google Cloud Storage!


### Connecting with Firebase Admin
- 1. Go to `Project Overview` $\Rightarrow$ `Project Setting` $\Rightarrow$ `Service accounts`
- 2. Press button `Generate new private key` and then, Download the JSON credentials file. 
- 3. Rename the downloaded file as `serviceAccountKey.json`
- 4. Move to the file you want.


### Python Env 
- 1. Python
- 2. ```pip install firebase_admin```

## Retrieve data to local folder
- 1. Prepare your local folder
- 2. Check `001_admin_SDK_setup.ipynb`