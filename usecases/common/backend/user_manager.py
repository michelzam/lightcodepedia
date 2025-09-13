import json
from dataclasses import dataclass

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import bcrypt
import streamlit as st
from usecases.common.backend.user_state import connected_users

from usecases.common.backend.env_manager import EnvManager
from dotenv import load_dotenv


def login(user_name: str, password: str) -> bool:
    user_manager = UserManager()
    result = user_manager.check_user(user_name, password)
    if result:
        st.session_state.user_info = user_manager.get_user_info(user_name, password)
        # print(f"{st.session_state.user_info = }")
        if user_name not in connected_users:
            connected_users.append(user_name)
    return result

def users_logged_in() -> list[str]:
    return connected_users

def update_user(user_name: str, password: str, new_password: str,
                repo: str, token: str) -> bool:
    user_manager = UserManager()
    if not user_manager.check_user(user_name, password):
        return False
    return user_manager.update_user(user_name=user_name,
        password=new_password, repo=repo, token=token)

def get_user_info(user_name: str, password: str) -> tuple[str, str]:
    user_manager = UserManager()
    return user_manager.get_user_info(user_name, password)

def get_status() -> str:
    if "status" not in st.session_state:
        st.session_state.status = "unverified"
    return  st.session_state.status

def get_user_repo() -> str:
    if "user_repo" in st.session_state:
        user_repo = st.session_state.user_repo
    else:
        user_repo = ''
    return user_repo

def get_user_name() -> str:
    if "user_name" not in st.session_state:
        return ''
    return st.session_state.user_name

@dataclass
class UserManager:
    client: gspread.Client = None
    json_str: str = None
    user_repos: list = None
    sheet_url: str = None

    def __post_init__(self):
        load_dotenv()
        @dataclass
        class UserRepo:
            url: str
            json_file: str

        self.json_str =  EnvManager.get_secret("GSHEET_JSON")
        self.user_repos = EnvManager.load_instances(UserRepo, "PLUGIN_USERS")
        self.sheet_url = self.user_repos[0].url

        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        json_data = json.loads(self.json_str)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(json_data, scope)
        self.client = gspread.authorize(creds)

    def _get_gsheet(self, json_file: str, url: str, sheet_name: str = 'Sheet1') -> pd.DataFrame:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(json_file, scope)
        client = gspread.authorize(creds)

        # sheet = client.open_by_url(url).sheet1
        sheet = client.open_by_url(url).worksheet(sheet_name)
        data = sheet.get_all_records()

        df = pd.DataFrame(data)

    def _get_gsheet_from_json(self, json_str: str, url: str, sheet_name: str = 'Sheet1') -> pd.DataFrame:
        sheet = self.client.open_by_url(url).worksheet(sheet_name)
        data = sheet.get_all_records()
        df = pd.DataFrame(data)
        return df

    def get_users(self) -> pd.DataFrame:

        if self.user_repos:
            df = self._get_gsheet_from_json(self.json_str, self.sheet_url)
            return df

    def get_assets(self) -> pd.DataFrame:

        if self.user_repos:
            df = self._get_gsheet_from_json(self.json_str, self.sheet_url,  sheet_name='Assets')
            return df


    def user_exists(self, user_name: str) -> bool:
        df = self.get_users()
        return user_name in df["user_name"].values

    def hash_password(self, plain_password: str) -> bytes:
        # Generate a salt and hash the password
        salt = bcrypt.gensalt()  # The salt is generated and included in the final hash
        hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
        return hashed_password

    def verify_password(self, plain_password: str, hashed_password: bytes) -> bool:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)


    def check_user(self, user_name: str, password: str) -> bool:
        sheet = self.client.open_by_url(self.sheet_url).sheet1
        records = sheet.get_all_records()

        for i, record in enumerate(records, start=2):  # Start from row 2 because row 1 is the header
            if record['user_name'] == user_name:
                hashed_password = record['password'].encode('utf-8')  # Convert the stored password back to bytes
                if self.verify_password(password, hashed_password):
                    st.session_state.user_repo = record['repo']
                    return True
                else:
                    st.session_state.user_repo = ''
                    print(f"Password for user {user_name} is incorrect.")
                    return False

        return False

    def get_user_info(self, user_name: str, password: str) -> tuple[str, str]:
        sheet = self.client.open_by_url(self.sheet_url).sheet1
        records = sheet.get_all_records()

        for i, record in enumerate(records, start=2):  # Start from row 2 because row 1 is the header
            if record['user_name'] == user_name:
                hashed_password = record['password'].encode('utf-8')  # Convert the stored password back to bytes
                if self.verify_password(password, hashed_password):
                    return record['repo'], record['token']
                else:
                    print(f"Password for user {user_name} is incorrect.")
                    return False

        return False

    def register_user(self, user_name: str, plain_password: str) -> bool:
        if self.user_exists(user_name):
            return False
        hashed_pw = self.hash_password(plain_password)
        sheet = self.client.open_by_url(self.sheet_url).sheet1

        sheet.append_row([user_name, hashed_pw.decode('utf-8')])
        return True


    def unregister_user(self, user_name: str, password: str) -> bool:
        sheet = self.client.open_by_url(self.sheet_url).sheet1

        # Get all data from the sheet
        records = sheet.get_all_records()

        # Check if the username exists
        for i, record in enumerate(records, start=2):  # Start from row 2 because row 1 is the header
            if record['user_name'] == user_name:
                # Verify the password by comparing with the stored hashed password
                hashed_password = record['password'].encode('utf-8')  # Convert the stored password back to bytes
                if self.verify_password(password, hashed_password):
                    # If the password is correct, remove the row
                    sheet.delete_rows(i)
                    return True
                else:
                    print(f"Password for user {user_name} is incorrect.")
                    return False

        return False

    def update_user(self, user_name:str, password: str, repo: str, token: str) -> bool:
        if not self.user_exists(user_name):
            return False
        hashed_pw = self.hash_password(password).decode('utf-8')  # hash the plain password
        sheet = self.client.open_by_url(self.sheet_url).sheet1

        user_data = sheet.get_all_records()
        for idx, row in enumerate(user_data, start=2):  # start=2 to skip header row
            if row['user_name'] == user_name:
                # Update the password and token in the user's row
                if len(password) > 0:  # Only update password if a new password is provided
                    sheet.update(f'B{idx}', [[hashed_pw]])  # Assuming password is in column B
                sheet.update(f'C{idx}', [[repo]])  # Assuming repo is in column C
                sheet.update(f'D{idx}', [[token]])  # Assuming token is in column D
                return True

        return False
