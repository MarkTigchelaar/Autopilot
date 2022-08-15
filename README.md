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

```
enum chars(char) is
  value_one = 'a',
  value_two = 'b'
end
```

#### union
As a alternative to enums with tagged values, Autopilot simply has tagged unions.
This is the type that can be used in the same way other languages (like Rust) use enums.

```
union sum_type is
  field_a as int,
  field_b as float,
  field_c as userDefType
end
```
#### struct
Autopilot is not object oriented.
structs in autopilot can have pub fields and methods, as well as other attributes

```
struct items is
  pub int id,
  float some_field

  inline pub fun method_one(var as float) int do
    some_field = var
    return id
  end
end
```

#### interface
Autopilot does have interfaces
a struct "uses" an interface, rather than having a struct that "implements" them.
This might change (uses -> implements) in the future

```
interface some_api is
  fun a_method(a as int, b as int, c as someType) someOtherType
end

struct an_api_user uses some_api is
  field as int
  acyclic fun a_method(a as int, b as int, c as someType) someOtherType do
    ...
  end
end
```

#### module
Autopilot has the module keyword, which must be placed above all other Autopilot code.
The file will need to be named the same as the module, this is just to enforce that.
```
module some_module_name
```

#### define
All function pointers, and data structures must have their explicit types defined using the define statement.
define statements must also be above all other code, but below the module declaration.
```
define fun(int, float, someType, anotherType) thirdType as ThirdTypeFunction
define Dictionary(int:float) as aIntDict
define LinkedList(someStructType) as SomeTypeList
define Option(myStructType) as myStructOption
define Result(goodNews, errortype) as NewsResult
```
Autopilot only allows you to define a data structures contents with the predefined name, having a compound definition is forbidden:
```
define fun(fun(int) int, float, someType) fun(int) as funnyFunc <- ERROR!
```
Each type would need to be build up in previous defines (no need to be in order)
```
define fun(int) int as MoreIntsFunction
define fun(MoreIntsFunction, float, someType) intFunc as funnyFunc
define fun(int) as intFunc
```
This prevents define statements from being cluttered, and makes it easier to reuse the defined types.
The define statement is a central part of Autopilot, since it is where all compound user types are defined
There are several built in data structures in Autopilot:
- Map
- Dictionary
- HashMap
- List
- LinkedList
- Vector
- Set
- HashSet
- TreeSet
- Stack
- Queue
- FIFOQueue
- PriorityQueue
- Deque
- Option
- Result

It is illegal in Autopilot to directly nest these data types:
```
define Dictionary(int : HashMap(int : someType)) as NestedDict <- ERROR
```
Instead, you are forced to place structs or unions in between nested data structures
```
define HashMap(int : someType) as myHashContainer
define Dictionary(int : structType) as NestedDict <- Ok

struct structType is
  pub data as myHashContainer
  ...
end
```
This is to prevent soupy code where the data structure is difficult to handle, since you cannot add methods and fields into the nested layers, resulting in code that processes the contents being scattered everywhere.

Several of these types are acutally built in interfaces, and cannot be instantiated directly:
- Map
- List
- Set
- Queue
If you wish to use the two types what relate to each of the following in the same function, you will have to define one of these types as well:
```
define LinkedList(int) as IntLinkedList
define Vector(int) as IntVector
define List(int) as IntList

acyclic pub fun do_stuff(IntList) do
 ...
end
```