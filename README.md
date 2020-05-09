# ATP

### Interpreter

#### Options 
>Language = own language

##### should haves:
> 1. Own languages.
> 1. Visualization (show line numbers and current state of variables).
> 1. Advanced language features (Not sure if features are should haves or are actually part of must haves ) .
>    1. support nested while and if statements .
>    1. Multiple & divide have higher priority then Add & Subtract (so calculations have correct order).

##### Why
> Latin is the primary language for scientific names.
> So is decided to write my own coding language in latin.


#### Language:

| Operator  | Type          |
| --------- | ------------- |
| adde      | ADD (+)       |
| minuas    | SUB (-)       |
| pullulate | MUL (*)       |
| divisa    | DIV (/)       |
| assignato | Assign (=)    |
| minor     | Lesser (<)    |
| major     | Greater (>)   |
| par       | Equal (==)    |
| dispar    | NotEqual (!=) |

##### End of assignment

| Name      | Meaning | Info                         |
| --------- | ------- | ---------------------------- |
| semicolon | EOL     | End of Line of an assignment |

###### Example of an assignment:

```
x assignato 5 semicolon
```
##### While loop

| Name     | Meaning  | Info                                           |
| -------- | -------- | ---------------------------------------------- |
| dum      | while    | start of while loop                            |
| tum      | EOC      | End of condition (start of statements in loop) |
| finisdum | EndWhile | End of while loop                              |

###### Example of a while loop:

```
x assignato 2 semicolon
dum x minor 10 tum
    x assignato x adde 1 semicolon
finisdum 
```

##### If statement

| Name    | Meaning | Info                                                   |
| ------- | ------- | ------------------------------------------------------ |
| si      | If      | start of if statement                                  |
| tum     | EOC     | End of condition (start of statements in if statement) |
| finissi | EndIf   | End of if statement                                    |

###### Example of an if statement:

```
x assignato 5 semicolon
si x major 4 tum 
    x assignato 4 semicolon
finissi
```

####    Example code:
> tabs are just for readability (not necessary)

``` x assignato 0 semicolon
m assignato 5 semicolon
y assignato 2 semicolon
dum x minor 10 tum
     x assignato x adde 1 semicolon
     dum m dispar 20 tum
        m assignato m adde 1 semicolon
         si m major 18 tum 
             y assignato y pullulate 2 semicolon
         finissi
     finisdum 
finisdum 
``` 
> See File.txt for other example
