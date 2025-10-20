# voice_agent features implementation


## Setup and Running

1. Clone the repository and navigate to the project root directory (`VOICE_AGENT`).

2. (Basic) Create and activate a Python virtual environment:

```shell 
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate

````
3. Install dependencies:

```shell
pip install django
````
4. Apply database migrations:

```shell
python manage.py migrate
````
5. Run the development server:

```shell
python manage.py runserver
````
---

## Notes ( For contribution )

- ### install FFmpeg <br />
<i>Install Chocolatey first (run as Administrator in PowerShell)</i>
```shell
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
````

<i>Then install ffmpeg (run as Administrator in PowerShell)</i>

```shell
choco install ffmpeg
````

---

Developed by neuraq devs.
