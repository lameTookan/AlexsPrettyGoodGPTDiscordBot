import sys
import MyStuff as ms 

sys.path.append("./APGCM")
import APGCM
from config_maker import make_config
make_config()
from bot.bot import main as bot_main

if __name__ == "__main__":
    ms.mh.main_helper()
    bot_main()