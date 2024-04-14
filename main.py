import datetime
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == "__main__":
    current_time = datetime.datetime.now().strftime("%H:%M:%S") 
    print('start function ran at ' + str(current_time))
    
    version = os.getenv("VERSION")
    print("version run:", version)
    
    handler_file = f"handler-{version.replace('.', '-')}.py"
    
    try:
        handler_module = __import__(f"src.{handler_file[:-3]}", fromlist=['run'])
        handler_module.run()
    except ModuleNotFoundError:
        print(f"Handler file {handler_file} not found.")
