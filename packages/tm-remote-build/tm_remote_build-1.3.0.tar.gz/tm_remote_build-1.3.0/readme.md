# Remote Build

Build and reload openplanet plugins from your IDE.

## Setup

First install the RemoteBuild Openplanet plugin [found here](https://openplanet.dev/plugin/remotebuild) or from the
ingame plugin manager.

Then install the remote build client using pip:

```
python -m pip install --upgrade tm-remote-build
```

## Usage

### Use Case 1 - Plugin Folder in Openplanet\*/Plugins/ Folder

This is the use case if your plugin source code is located in an Openplanet\*/Plugins folder.

Invoke the remote build client and pass in the path to the folder. A relative path is also valid.

```
tm-remote-build C:\Users\Username\OpenplanetNext\Plugins\Dashboard
```

The client will connect to the running game for this folder location and load the plugin.

### Use Case 2 - Zipped Plugin \*.op

This use case is great if you have external packaging scripts since the input is a pre-existing \*.op file.

Invoke the remote build client and pass in the path to the zipped plugin file. A relative path is also valid.

```
tm-remote-build C:\Users\Username\Code\Dashboard\Dashboard.op
```

The client will find every running game and deploy and load the zipped plugin to all of them.

## Links

* Github: https://github.com/skybaks/tm-remote-build
* Pypi: https://pypi.org/project/tm-remote-build/
* Openplanet: https://openplanet.dev/plugin/remotebuild
