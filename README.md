# classroomContactApi

A Python / Flask implementation of an API that communicates with edwpub and local sqlite databases to provide lists of classroom contacts / instructors to app users. This project has no direct front-end, but should handle any appropriately configured client that can handle JSON data behind an SSO login (shibboleth/netid).

## Development Status

This project is a re-implementation of the original classroom contacts api, which was written in PHP. New features will be implemented in this project, but the overall project is still highly under construction. Specific needs for the project are things like tests, error handling, API documentation, and project documentation.

Requests use local filesystem cache files to accelerate requests that return a lot of the same data / data that rarely changes, and to reduce the number of round trips to the database. This can take requests down from approximately 300ms to 10ms.

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

#### Windows / IIS Webserver

Setting up on a Windows/IIS webserver is the expected deployment option, but is messy and takes a lot of faffing, debugging, etc. The following steps _should_ get everything working. YMMV.

1. Download + install Python to `C:\Python[vvv]`
2. Create a project directory in `C:\inetpub\wwwroot\classroomContactApi` if it doesn't exist already, or `git clone` this project within `\wwwroot\` to create and copy files to the correct location
3. Set up a virtual environment (within `C:\inetpub\wwwroot\classroomContactApi`):

```powershell
PS C:\inetpub\wwwroot\classroomContactApi> python -m venv .\venv
```

4. Activate the virtual environment:

```powershell
> .\venv\Scripts\activate
```

5. Copy project files / check out git repository to location
6. Install wfastcgi

```powershell
(venv) > python -m pip install classroomContactApi, wfastcgi
```

7. Enable wfastcgi as a script processor in IIS

```powershell
(venv) > wfastcgi-enable
```

8. Go to IIS Settings, FastCGI settings, configure fast CGI setting for the added application:
    - Set Environment Variables (collection) to contain the following: (Be careful of slash ( `\` `/` ) directions)
      - `WSGI_HANDLER` : `classroomContactApi.app`
      - `PYTHONPATH` : `C:\inetpub\wwwroot\classroomContactApi`
      - `SCRIPT_NAME` : `/classroomContactApi`
        - ⚠ Note: this must match the subdirectory under which th Flask WSGI Application will be served by IIS. Omit if this is running on your server's root
        - This is not documented under wfastcgi, found setting suggestion on stackoverflow somewhere
      - (for debugging ONLY) `WSGI_LOG` : `C:\inetpub\logs\wsgi\classroomContactApi.log`
        - ⚠ Note: You must create and grant the IIS_IUSRS full write permission on whatever log file you create, otherwise the WSGI process will fail to launch (can't start to write to the log, will fail with access denied to directory / file) leading to mysterious 500 server errors from IIS (there won't be helpful logs about the crash from IIS)
9. Add a handler mapping to the site - Handler Mappings (classroomContactApi) -> Add Module Mapping
    - Request path: `*`
    - Module: FastCGIModule
    - Executable: `C:\inetpub\wwwroot\classroomContactApi\venv\Scripts\python.exe|C:\inetpub\wwwroot\classroomContactApi\venv\Lib\site-packages\wfastcgi.py`
10. Set Handler Mapping -> Request Restrictions
    - UN-check "Invoke handler only if request is mapped to"
    - Verbs tab -> "All"
    - Access tab -> "Script"
11. When closing, if it asks to create a FastCGI application for this mapping, select No
12. Switch the Handler Mappings view in IIS Manager to the ordered list, and put the Python handler at the very top of the list, above all others, so that something else, like PHP doesn't try to serve anything from this application.
13. Set up the site folder as an application (right-click, convert to application)
14. Create an application pool, setting the identity of the application pool to use an account that has access to the SQL Server database. This will be the context within which Python/pyodbc will pass the connection identity to the database for authentication using the "TrustedConnection=True" connection parameter (Windows integrated authentication)
15. Set (if not already) the same account as a member of the local "IIS_IUSRS" group on the webserver (via lusrmgr.msc)
16. Set the application to use the created application pool as set up in the previous steps (via Right-click application in IIS Manager > Manage Application > Advanced Settings...)

17. Add site path to the list of shibboleth sites (if applicable) in the shibboleth configuration (located in `C:\opt\shibboleth-sp\etc\shibboleth\shibboleth2.xml`)

```xml
  <Path name="classroomcontactapi" authType="shibboleth" requireSession="true">
      <AccessControl>
          <Rule require="gws_groups">[control / access group]</Rule>
      </AccessControl>              
  </Path> 
```

18. Restart the shibboleth daemon / service

#### Every other kind of web server (apache, nginx, etc)

Just read the Flask deployment documentation. Note, however, that running this particular application in a Non-Windows environment will require changes to how the SQL Server database is accessed. Make necessary changes to `db.py`.
