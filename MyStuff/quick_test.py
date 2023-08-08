import sys 
sys.path.append("./APGCM")

import APGCM 

cw = APGCM.chat_utilities.quick_make_chat_wrapper()
APGCM.chat_utilities.quick_and_dirty_chatloop(cw)