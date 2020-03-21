# mcpile 
A small python project to make writing minecraft datapacks easier

mcpile works with a module based system, with a module being able to connect to a syntax handler (`sugar.py`) and then run python code on a line that meets the requirements

# Using mcpile

mcpile.py is the main file, it will prompt for a file and namespace.
The file is searched for locally, and namespace is the namespace of the functions, so if you put `helloworld` as the namespace, the main function would be called with `function helloworld:main`

## Loading modules
By default there is only one built in syntax, `IMPORT <module>` this will do a python import on that file in the modules folder
The default module is `standard` so you would put `IMPORT standard`

## Modules in code
Please Read the individual READMEs for each module in the modules folder for usage
Note any text not handled will by modules be output verbatim

`standard` - Main function of mcpile, contains loops, tags, ect.
`populate` - Basic line formatting

# Writing new modules

New modules should be .py files placed in the `/modules` directory

Modules can have any python code in them, however to actually add syntax there are a few requirements

1. `from sugar import newSyntax, returnStatus` to add the syntax callback to the handler and use returnStatus
2. A callback function to be called if condition met
3. a `newSyntax` call with your parameters `newSyntax(<One of 3 types>, <iterable (i.e. array) with your "brackets">, <callback function>)`
`brackets` are the text that will be looked for, the amount of brackets and what they mean depends on the type
---

The three types are `"lineStart"`, `"lineInternal"`, and `"startEndInternal"`

`lineStart` - Triggers if brackets[0] starts the line (Passes text with `brackets[0] + " "` removed)

`lineInternal` - Triggered if brackets[0] is in the line (Passes text before and after brackets[0])

`startEndInternal` - Triggered if brackets[1] comes after brackets[0] in the same line (passes text before, inside, and after)

---

Your callback function needs to have enough parameters for its type

`lineStart` - 2 parameters, info object, line

`lineInternal` - 3 parameters, info object, before and after

`startEndInternal` - 4 parameters, info object, before, middle, after

---

Callback needs to return a `returnStatus` class

Keyword arguments for return status do the following

`write` - What to write to the active file

`writeBefore` - What to write to the file 1 up

`skiplines` - How many lines to skip

`keepgoing` - Should more processing be done on this line?

a `returnStatus` with no keywords defaults to writing nothing and allowing continued parsing

---

## Multiline processing/preprocessing
Currently the only support for either of these is in the preprocessing step. Parsing must be done within your callback.

You can use `newPreparse` from the sugar module to access this. You call back will be passed info and text

text contains the entire file text as a signle string

Callback should return a single string consiting of the new text

---

Modules can also have a `onImport` function which will be called with the info object when imported

This function should be used to grab existsing data or set up properties to be accessed later from callbacks
