import importlib
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Ribbon_Twist_Joints import code # change to script running temp for now
from Ribbon import ribbon_it

importlib.reload(code) # remove after debug

def run():
    ribbon_it.main()
    print("main run")
    
# run_ui()