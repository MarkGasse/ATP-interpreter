# ATP

### ------------------------------------------------------------------

### Language = own language

### Latin is the primary language for scientific names.
### So is decided to write my own coding language in latin.


### ----------------------------------------------------------
###    Operator        |   Type       |
### ----------------------------------------------------------
###      adde          |     ADD      |
###      minuas        |     SUB      |
###      pullulate     |     MUL      |
###      divisa        |     DIV      |
###      assignato     |     Assign   |
###      minor         |     Lesser   |
###      major         |     Greater  |
###      par           |     Equal    |
###      dispar        |     NotEqual |
### ----------------------------------------------------------
###    Statement       |   Type       |
### ----------------------------------------------------------
###      si            |     If       |
###      dum           |     While    |
### ----------------------------------------------------------
###   End of Statement |   Type       |   Extra info
### ----------------------------------------------------------
###      finissi       |     EndIF    | 
###      finisdum      |     EndWhile |
###      tum           |     THEN     |    End of condition (if and while statement)
###      semicolon     |     EOL      |    End of Line
### ----------------------------------------------------------

### ----------------------------------------------------------
###    Example code:
### ----------------------------------------------------------
#### x assignato 0 semicolon
#### m assignato 5 semicolon
#### y assignato 2 semicolon
#### dum x minor 10 tum
####     x assignato x adde 1 semicolon
####     dum m dispar 20 tum
####        m assignato m adde 1 semicolon
####         si m major 18 tum 
####             y assignato y pullulate 2 semicolon
####         finissi
####     finisdum 
#### finisdum 