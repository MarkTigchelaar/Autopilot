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

The integers are unsigned.
int is 64 bits, and long is 128 bits.

The float type is 32 bits, and double is 64 bits.

chars are ascii, as are strings.
unicode etc. may be added at a later point.

### Compound types
Autopilot also has several types that should be familiar to most programmers.

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

#### import
import statements must also be placed above all other code, but below the module statement.
defines and imports can be above or below one another.
import statements have the following syntax:
```
import item_one, item_two, ... from module path.to.the_module.module_name
import item from library library_name
```
libraries are assumed to be compiled, and will be linked to the exe, instead of having the source code included.

#### error
error statements are definitions of error types.
Very similar to enums, and similar to error types in other languages.
In AutoPilot, error types cannot be assigned to variables that are not defined as Results (with that error as the alternatiive type)
```
error MyError as 
  errOne,
  errTwo
end
...
define Result(int, MyError) as someResult
...
let res as someResult = MyError.errOne
```

#### unittest
unittests are stand alone units of code similar to a function, but cannot recieve, or return a value.
unit tests should be familiar with most / all developers.
```
unittest test_name do
...
end
```
For the contents of unit tests, see the statment section below.

#### fun
fun (function) is used to define functions and methods.
as seen above, the signature of all functions is [acyclic | inline | pub] fun ([arg1,arg2,...]) [return type] do
...
end
In Autopilot, it is forbidden to define a function in a function.
All functions / methods are explicitly defined in their own sections of the source file.
This is not due to the complexity of parsing nested functions (although that is a consideration), it is due to the seemingly inevitable soupiness that comes with the ability to nest functions (see javascript)
One of the goals of Autopilot is to make the code cleaner, by being strict with defnitions and other pieces of syntax, function declaration is a big consideration in this regard.

For the contents of functions, see the statment section below.

#### define
All function pointers, and data structures must have their explicit types defined using the define statement.
specific user defined types can also be renamed using the define statement, such as specific functions, structs, enums, unions, or error types.
This is to help the programmer use the same type, but with a name that is more helpful in a given context.
define statements must also be above all other code, but below the module declaration.
define statements that define the same explicit types do not throw errors, but are discouraged.
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

Several of these types are actually built in interfaces, and cannot be instantiated directly:
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

#### acyclic, inline and pub keywords
- acyclic

This keyword can be used on methods / functions as well as structs.
This makes it impossible for a method / function to call itself.
for example, if the following letters represent functions, -> as calls, and A is acyclic, the following would be a compile error:
A -> B -> C-> F -> G -> A
Likewise, the same rule applies to acyclic structs.
Acyclic structs cannot have reference cycles at the type level.
- inline

This keyword can be used on methods / functions as well as structs
this will select a function for inlining, which is to copy the contents into the caller function.
This is a optimization, to save a function calls overhead.
For structs, this turns the inline struct into a copy type, where its memory footprint is on the stack, instead of the heap.
For structs, it is better to use this on smaller structs, or structs that are meant to be nested components of larger, regular structs
For funtions, this can provide a noticeable speed up, if the function would be called inside a hot loop.
Note that niether inline structs nor inline functions can refer to themselves.
If a struct / function is inline, they are also acyclic.
- pub

This keyword can be used on methods / functions as well as structs (and their fields).
pub is a simple access control. Autopilot allows you to prevent the use of fields or methods / functions by other code outside the struct, or for functions, outside the module
structs that do not have the pub attached to them cannot be used outside the module either.
use pub struct to make them useable outside the module they are defined in.
All structs, their fields, as well as methods and functions are private by default.

### statements
Autopilot continues its Ruby inspired syntax inside of methods, functions and unit tests.
ther is no use of the ; Autopilot figures out the difference between statments without them.
Here is a list of all statement types:
- Assignment
- Reassignment
- if
- elif
- else
- unless
- switch (with case, and default)
- loop
- for
- while
- break
- continue
- return
- function / method calls (with no assignment)

the defer statement is planned to be added in the near future.

##### (named) loops
Autopilot has 3 loop types:
- while
- for
- loop
Autopilot allows you to name loops:
```
while true as a_while_loop do
 ...
end
```

This allows you to break out of a inner loop, or continue on with a outer loop:
```
while true as outer do
  loop as inner do
    if true do
      break(inner)
    else
      continue(outer)
    end
  end
end
```

for loops also have this, but they are capable of more, such as evaluating collections of Options:
```
for let opt_variable in OptionCollection as for_loop do
 ...
end
```
for loops can also traverse ranges:
```
for i in 0 .. 100 do
 ...
end
```
for loops can also iterate through Map types:
```
for key, value in SomeHashMap do
 ...
end
```
and sets:
```
for item in SomeSet do
 ...
end
```

##### assignment
In Autopilot, you have the let and var keywords.
let allows one assignment only, var allows for reassigning at will:
```
let a as int = 0
a = 2 <- ERROR
```
##### reassignment
using the var keyword, variables can be reassigned values.
There are several combined assignment operators, as well as normal operators:
```
+
+=
-
-=
*
*=
/
/=
%
%=
^
^=
and
nand
or
nor
xor
not
```

```
var a as long = 0
a += 1 <- Ok
```

##### switch
switch statements work in much the same way as other languages:
```
switch test_condition
  case 'a', 'b', 'c' do
    ...
  case 'd', 'e' do
    ...
  default
    ...
end
```
switch statements MUST be exhaustive when dealing with unions and errors from Result types.

##### break
As seen above, break statements live in loops (not switches) and can refer to a label of a loop:
```
break(myLoop)
```
##### continue
As per break statements, continue statements can continue the current loop, or some named outer loop:
```
continue(outerLoop)
```
##### return
return statements are mandatory when a function or method does return some type.
In Autopilot, expressions of arbitrary size are allowed much the same as other languages:
```
return a + b / (c ^ 120) - 2016 * (- 4 / 2)
```

##### if, elif, else
if, elif and else statments work the same as any other language. if statments cannot be named:
```
if true xor false do
 ...
elif some_boolean do
 ...
else
 ...
end
```
##### unless
copying ruby, Autopilot does have unless statements.
However, unless statements mus be stand alone, and cannot be in a chain of other branching logic.
```
unless false do
 ...
else <- ERROR
 ...
end
```