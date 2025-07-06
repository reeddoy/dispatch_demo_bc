import dotenv
from pathlib import Path

env_path = Path(__file__).parent / ".env"
dotenv.load_dotenv(dotenv_path=env_path)

from .shared.services.servers import server
app = server