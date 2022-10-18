from dotenv import load_dotenv, dotenv_values

load_dotenv(verbose=True)
values = dotenv_values(verbose=True)

DATABASE_URI = values['DATABASE_URI']
