from MyStuff import ms as ms 
import time 
import pyfiglet

# ================================================================================================

def title_card():
    divider_2 = "="*(len(ms.auto_double_cyan) -6)
    divider_2_len = len(divider_2)
   
    divider_len = len(ms.auto_double_cyan)
    larry = pyfiglet.Figlet(font="isometric3", justify="center")
    digital = pyfiglet.Figlet(font='digital', justify="center")
    key_board = pyfiglet.Figlet(font='smkeyboard')
    col = pyfiglet.Figlet( font = "rev" )
    
    title = col.renderText("A P G D B")
    
    name = ms.cyan("|----------------->Alex's Pretty Good GPT Discord Bot<-----------------|").center(divider_len, " ")
    apgcm =   larry.renderText("APGCM" )
   
   
    print(ms.auto_double_cyan)
    print("\n\n")
    print(ms.cyan("|_______________________...Welcome To..._______________________|").center(divider_len, " "))
    print("\n")
    print(title.center(divider_len, " "))
    
    print(name.center(divider_len, " "))
    print()
    print()

    print(ms.auto_center_stars)
    print()
    time.sleep(2)
    print() 
    
    
    print("........................Powered By........................".center(divider_2_len, " "))
    print(ms.magenta(apgcm.center(divider_len, " ")))
    print("\n")
    print(ms.magenta("|--------------> Alex's Pretty Good Chat Module<--------------| ".center(divider_2_len, " ")))
    print(ms.magenta(divider_2 + "\n"))
    
    
    
def main_helper():
    title_card()
    print("Be sure to use the quick_test.py file to test your settings before running the bot.")
    

    print("Starting Discord Bot...")
    print("\n\n")
    
    
    
