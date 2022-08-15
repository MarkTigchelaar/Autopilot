# Autopilot
A ruby inspired statically typed programming language

## Syntax

Autopilot does diverge from Ruby in that is has statically checked types, and a strict method of defining types

### Primitive types
Autopilot has the following primitive data types:
- int
- long
- float
- double
- char
- string
- bool

### Compound types
Autopilot also has several types that should be familiar to most programmers
#### enum
The enum type can only contain primitive types.
Although this may seem limiting given how other languages allow enums to contain values, enums in Autopilot are just a collection of defined values
ex:
```
enum chars(char) is
  value_one = 'a',
  value_two = 'b'
end
```

#### union
As a alternative to enums with tagged values, Autopilot simply has tagged unions.
This is the type that can be used in the same way other languages (like Rust) use enums.
ex:
```
union sum_type is
  field_a as int,
  field_b as float,
  field_c as userDefType
end
```
#### struct
Autopilot is not object oriented.
structs in 





### Declarations:
Declarations are done by using the let, or the var keywords.
let does not allow you to reassign the variable, var does:
let a = 10
var b = 5

----
Autopilot does have type inference, but types can be stated explicitly:
let a as int = 10
let b as long = 5

----