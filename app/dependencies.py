from fastapi.templating import Jinja2Templates
import tomllib

templates = Jinja2Templates(directory="app/templates")

try:
	with open("app/conf/config.toml", "rb") as f:
		config = tomllib.load(f)
except FileNotFoundError:
	print("No custom config found!\nUsing template config!\nPlease configure your config in app/conf/config.toml")
	with open("app/conf/config_template.toml", "rb") as f:
		config = tomllib.load(f)

server_config = config["server_config"]
