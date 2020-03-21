# Populate module features
Dynamic text formatting
Handled in preprocessing

Group text you want to format in `$`
Supports multiple lines
Format is `text $<populatelist> text {} text`

---

populatelist - name of file in modules/PopulateFiles, must include file type
{} - Replacement token, will be filled in with each line in populatefile

---

```
IMPORT populate

$execute if solid_blocks.txt block ~ ~ ~ {} run say {}$