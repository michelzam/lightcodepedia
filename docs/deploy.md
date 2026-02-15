# Deploy your **LightCode** app to Streamlit Community Cloud (via GitHub)

> Follow this guide to create a GitHub account, fork this repo, sign in to Streamlit with GitHub, create & deploy the app, and (if needed) fix a build error by switching Python to **3.10**.

## Prerequisites
- A web browser and internet connection.
- A GitHub account (we will create one if you don't have it).

---

## Step 1 — Create (or sign into) your **GitHub** account

1. Click **Sign up** (or **Sign in** if you already have an account).
   
   ![GitHub header: Sign up](assets/github_header_signup.png)

2. Fill the sign-up form (email, password, username, country), then **Create account**.
   
   ![GitHub sign-up form](assets/github_signup_form.png)

3. Go to the repository [lightcodepedia](https://github.com/MichelZam/lightcodepedia) and open the **Fork** menu.
   
   ![Fork dropdown](assets/github_fork_dropdown.png)

4. Choose **Create a new fork**.
   
   ![Create a new fork menu](assets/github_create_new_fork_menu.png)

5. On the **Create a new fork** page, keep the default name (or customize), ensure **Copy the `main` branch only** is checked, then click **Create fork**.
   
   ![Create a new fork page](assets/github_create_new_fork_page.png)

6. ✅ If you land on your new repo page (forked from `michelzam/lightcodepedia`), your fork is ready.
   
   ![Fork success repository page](assets/github_fork_success_repo.png)

---

## Step 2 — Deploy on **Streamlit Community Cloud**

1. Go to Streamlit Community Cloud https://streamlit.io/cloud and click **Continue to sign-in**.
   
   ![Streamlit: Continue to sign-in](assets/streamlit_continue_to_signin.png)

2. Click **Create app** (or **Create your first app now**).
   
   ![Create app button](assets/streamlit_create_app_button.png)

3. When prompted, click **Connect to GitHub**.
   
   ![Connect to GitHub modal](assets/streamlit_connect_to_github_modal.png)

4. On GitHub, click **Authorize streamlit** to allow access.
   
   ![Authorize Streamlit on GitHub](assets/streamlit_github_authorize.png)

5. Back in Streamlit, fill the deploy form then **Deploy**:
   - **Repository**: select your **fork** of `lightcodepedia`
   - **Branch**: `main`
   - **Main file path**: `main.py`
   
   ![Streamlit deploy form (main.py)](assets/streamlit_deploy_form_main_py.png)

---

## Troubleshooting — If an error appears during deployment

If the build fails with a Python version error:

1. Open your app in Streamlit Cloud → **Manage app**.  
2. Go to **Settings** → **General** (or **Advanced/Runtime**).  
3. Set **Python version** to **3.10** and click **Save changes**.  
   
   ![Change Python to 3.10 in app settings](assets/streamlit_runtime_python_310.png)


Lightcode.
(c) KarmicSoft 2026
