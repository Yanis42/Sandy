# Project Sandy
Multi-Platform [AutoSplit](https://github.com/Toufool/Auto-Split) Images Renamer.

This program requires a LiveSplit split file (*.lss) and PyQt6, optional: QDarkTheme to use a dark theme.

Tested under Python 3.10 but should work on any version that supports PyQt6.

# Usage
Before using this make sure:
- Non-dummy splits are in the same order as your splits from LiveSplit
- Dummy splits have ``dummy`` in the filename (i.e.: ``001_dummy_splitname.png``)

After everything's ready:
- Run ``src/main.py`` with Python (executable builds not available yet)
- Open the .lss split file (only used to get the split names)
- Open the AutoSplit images directory
- Set the global similarity (you'll need to adjust manually for now)
- Set the global pause time (you'll need to adjust manually for now)
- Click on "Rename Images" and you're done!

# Features
- Renames your AutoSplit images
- Automatically add the mask ``{m}`` and dummy ``{d}`` flags if used

# Building
This is not required to use this program, but if you want to build it run ``build.py``, the generated executable for your OS will be available in the ``dist`` folder (created when building)

# Contributions are welcome!
This project use Black to format the code properly


###### 'Time' > 'Hourglass' > 'Sand' > 'Sandy', because this little program saves some IRL time
