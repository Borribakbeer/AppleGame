# AppleGame

To start game run "Data/__main__.py"


### Known possible optimization:
- Ground tagged GameObjects are always drawn. even offscreen
- Input is taken twice (update() and get_key())
- Everything from every scene is intitialized on startup
- All Graphics are in RAM from start and always are