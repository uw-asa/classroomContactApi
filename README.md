# classroomContactApi

A Python / Flask implementation of an API that communicates with edwpub and local sqlite databases to provide lists of classroom contacts / instructors to app users. This project has no direct front-end, but should handle any appropriately configured client that can handle JSON data behind an SSO login (shibboleth/netid).

## Development Status

This project is a re-implementation of the original classroom contacts api, which was written in PHP. New features will be implemented in this project, but the overall project is still highly under construction. Specific needs for the project are things like tests, error handling, API documentation, and project documentation.

## Setup Environments

### Development

Set up env and run the local server (assumes you have a virtualenv set up already, with flask, pyodbc, etc installed)

```powershell
(venv) > $env:FLASK_APP = "classroomContactApi"
(venv) > $env:FLASK_ENV = "development"
(venv) > flask run
```

#### Local Database Setup

```powershell
(venv) > $env:FLASK_APP = "classroomContactApi"
(venv) > $env:FLASK_ENV = "development"
(venv) > flask init-db
```

Alternately, just run using vscode configuration (see launch.json)

### Production

#### IIS Webserver

1. Download + install Python to `C:\Python[vvv]`
2. Create a project directory in `C:\inetpub\wwwroot\classroomContactApi` if it doesn't exist already, or `git clone` this project within `\wwwroot\` to create and copy files to the correct location
3. Set up a virtual environment (within `C:\inetpub\wwwroot\classroomContactApi`):

```powershell
PS C:\inetpub\wwwroot\classroomContactApi> python venv .\venv
```

4. Activate the virtual environment:

```powershell
> .\venv\Scripts\Activate.ps1
```

5. Copy project files / check out git repository to location
6. Install wfastcgi

```powershell
(venv) > pip install wfastcgi
```

7. Set up FastCGI handler in IIS Manager

#### Everything Else

Just read the Flask deployment documentation.
