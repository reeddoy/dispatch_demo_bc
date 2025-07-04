import dotenv

dotenv.load_dotenv(override=True)

from .shared.services.servers import server
app = server