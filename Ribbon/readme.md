<h1 align="center">Maya Ribbon Rigging</h1>
<p align="center"}>
  <img src="https://img.shields.io/badge/Maya-37A5CC?style=for-the-badge&logo=autodeskmaya&logoColor=white">
  <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue">
  <img src="https://img.shields.io/badge/Qt-41CD52?style=for-the-badge&logo=Qt&logoColor=white">
</p>

This tool creates follicles, joint and connections based off the selection of a nurbs surface.
> The UI is relative to ribbon_it.py file the main_window.ui file must be in the same location for the UI to load.


## Features
- **IK Ribbon Controls**
- **Follicle and joint creation.**

## Installation
### Requirements
- Autodesk Maya
- PYQT

### Running The Tool
- To run the file execute the follow code in the maya script editor or shelf tool.

```python
import sys
sys.path.append("C:\Docs\maya\2024\scripts") # change this to your path or a relative path

from ribbon import ribbon_it
ribbon.ribbon_it()
```
