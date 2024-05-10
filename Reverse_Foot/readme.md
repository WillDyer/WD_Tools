<h1 align="center">Maya Reverse Foot Rigging</h1>
<p align="center"}>
  <img src="https://img.shields.io/badge/Maya-37A5CC?style=for-the-badge&logo=autodeskmaya&logoColor=white">
  <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue">
  <img src="https://img.shields.io/badge/Qt-41CD52?style=for-the-badge&logo=Qt&logoColor=white">
</p>

This tool creates reverse foot joints and attrs setup via the node editor with no set driven key for ease of editing.
> The UI is relative to reverse_foot_code.py file the main_window.ui file must be in the same location for the UI to load.


## Features
- **Custom, Roll, Bank, Heel & Toe Twist attribute setup via node editor**

## Installation
### Requirements
- Autodesk Maya
- PYQT

### Running The Tool
- To run the file execute the follow code in the maya script editor or shelf tool.

```python
import sys
sys.path.append("C:\Docs\maya\2024\scripts") # change this to your path or a relative path

import importlib
from rev_foot import rev_foot_code

importlib.reload(rev_foot_code)
rev_foot_code.main()
```
