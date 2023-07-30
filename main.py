import sys

sys.path.append("./APGCM")
from APGCM import (
    DEFAULT_LOGGING_LEVEL,
    BaseLogger,
    ChatFactory,
    ChatWrapper,
    JsonSaveHandler,
    exceptions,
    
)
from APGCM.settings import DEFAULT_TEMPLATE_NAME, OPENAI_API_KEY

from bot.bot import main as bot_main

if __name__ == "__main__":
    bot_main()