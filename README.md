# neuraqdevs-voice_agent


## Setup and Running

1. Clone the repository and navigate to the project root directory (`neuraqdevs-voice_agent`).

2. (Optional) Create and activate a Python virtual environment:

```shell 
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate

````
3. Install dependencies:

```shell
pip install -r requirements.txt
# Else install seprate : pip install django
````
4. Apply database migrations:

```shell
python manage.py migrate
````
5. Run the development server:

```shell
python manage.py runserver
````
## Notes

- Adjust `voiceai/settings.py` as necessary for database or allowed hosts configuration.
- Templates are located in the `templates/` directory.
- Application URL configurations are in `voiceapp/urls.py` and `voiceai/urls.py`.

---

Developed by neuraqdevs.
