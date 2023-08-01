import sys
import MyStuff as ms 

sys.path.append("./APGCM")
import APGCM
from config import make_config
from bot.bot import main as bot_main
make_config()
if __name__ == "__main__":
    ms.mh.main_helper()
    bot_main()