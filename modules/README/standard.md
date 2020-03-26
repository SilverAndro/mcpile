# Standard module features
1. Execute blocks (Executes once if condition met)
```
IMPORT standard

:execute <condition> {
  <command1>
  ...
  <commandN>
}
```
2. While loops (Runs until condition not met)
```
IMPORT standard

:while <condition> {
  <command1>
  ...
  <commandN>
}
```
3. Do-While loops (Runs once, and then until condition not met)
```
IMPORT standard

:do <condition> {
  <command1>
  ...
  <commandN>
}
```
4. Substitution (Replaces any \<text1> with \<text2> anywhere in code)
```
IMPORT standard

REPLACE <text1>[=]<text2>
```
5. Functions (Writen to a file but must be called with :run)
```
IMPORT standard

:function <function name> {
  <command1>
  ...
  <commandN>
}

// To run the function
:run <function name>
```

6. [Tags](https://minecraft.gamepedia.com/Tag#Function_Tags)
    a. Active (Next file/context writen to is tagged in the titled tag file, use `minecraft:<tag>` to place tag in minecraft namespace)
    ```
    IMPORT standard
    
    *<tag text>
    <commands>
    ```
    b. Passive (Create a tag file in a non-function enviroment, preparsed)
    ```
    IMPORT standard

    *<tag text>
    <commands>
    ```
7. Comments
```
IMPORT standard

// This is text
This is code
```