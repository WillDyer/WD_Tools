<h1 align="center">Maya Simple FK</h1>
<p align="center"}>
  <img src="https://img.shields.io/badge/Maya-37A5CC?style=for-the-badge&logo=autodeskmaya&logoColor=white">
  <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue">
</p>

This tool creates a simple FK chain using offset parent matrix.
> This tool requires a OPM module which can be found here: TBC


## Features
- **Creates a FK chain from joint selection**
- **Adds "ctr_fk" prefix**
- **Constrains ctrl to joint selected**

## Installation
### Requirements
- Autodesk Maya
- OPM module

### Running The Tool
- To run the file execute the follow code in the maya script editor or shelf tool.

```python
import sys
sys.path.append("C:\Docs\maya\2024\scripts") # change this to your path or a relative path

from simple_fk import fk

fk.CreateFkSystems()
```

