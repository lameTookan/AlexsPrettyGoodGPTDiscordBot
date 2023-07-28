from templates.temp_sample import template_sample
import json 
from pathlib import Path

def reload_temps():
    
    with open("templates/templates.json", "r") as f:
        templates = json.load(f)

    path = Path("templates/templates.json")
    if not path.exists():
        with open("templates/templates.json", "w") as f:
            json.dump(template_sample, f, indent=4)
    while True:
        print("Welcome to the template reload script.")
        print("If you mess things up in the template file, this script will reload the default, built in templates")
        print("If you have reached this script by accident, type q to exit")
        print("Otherwise, type r to reload the templates, and save the previous templates to templates.json.bak")
        ans = input(">>").lower().strip()
        if ans in ("q", "quit", "exit"):
            break
        elif ans in ("r", "reload"):
            #rename the old templates file
            path.rename("templates/templates.json.bak")
            print("Old templates file renamed to templates.json.bak")
            #write the new templates file
            with open("templates/templates.json", "w") as f:
                json.dump(template_sample, f, indent=4)  
            print("New templates file written")
            break
        else:
            print("Invalid input, try again")
            print("Remember, type q to exit, or r to reload the templates")
            continue
reload_temps()