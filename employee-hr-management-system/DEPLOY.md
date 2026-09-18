# Deployment

## Streamlit Community Cloud

1. Push this folder to a GitHub repository.
2. In Streamlit Community Cloud, choose **Create app**.
3. Select the repository, branch, and `app.py` entrypoint.
4. Deploy.
5. For a real shared deployment, use a remote MySQL database. Do not rely on the bundled SQLite file for persistent production data.
6. In the app's **Advanced settings → Secrets**, add:

```toml
MYSQL_HOST = "your-mysql-host"
MYSQL_PORT = "3306"
MYSQL_USER = "your-user"
MYSQL_PASSWORD = "your-password"
MYSQL_DATABASE = "hr_management"
```

The application already reads these values through environment variables.

### Important persistence note

The local SQLite database is useful for demos and offline development, but cloud app files should not be treated as a durable database. For a deployed version where CRUD changes must survive restarts, connect the app to MySQL.

## Local

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m streamlit run app.py
```

Then open the local URL printed by Streamlit.

## Git

```powershell
git add .
git commit -m "Upgrade HR dashboard UI and workflows"
git push
```
