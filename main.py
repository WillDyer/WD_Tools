import importlib
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

#from Ribbon_Twist_Joints import code # change to script running temp for now
from Ribbon import ribbon_it
from mouth_setup import mouth_build

#importlib.reload(code) # remove after debug
importlib.reload(ribbon_it)
importlib.reload(mouth_build)

"""def run_code():
    code.main()
    #ribbon_it.main()
    print("main run")
"""
def run_ribbon():
    ribbon_it.main()

def run_mouth():
    mouth_build.mouth()

    
# run_ui()
