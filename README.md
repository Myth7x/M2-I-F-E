Proto_InterfaceManager
## Usage
   •  1. Clope Repo 
   
   •  2. Append following code at the of of def intrologin.LoginWindow.\__init__
```
sys.path.append('C:\\Proto_InterfaceManager\\')
import interfacemanager
self.ifmgr = interfacemanager.setup_ifmgr(setup_ifmgr)
```
