Here is the updated **Autopilot README** with the comment syntax and DAG dependency rule added.

---

# Autopilot

> **A Ruby-inspired, statically typed scripting language.**

Autopilot combines the developer joy and readable syntax of Ruby with the performance and safety of a statically typed, compiled system. It is designed for deterministic memory management without the overhead of a global garbage collector.

## Core Philosophy

1. **Readable & Expressive:** Syntax should be familiar ("Vanilla Ruby"), minimizing boilerplate while maximizing clarity.
2. **Statically Safe:** Types are checked at compile-time. Dependencies are explicit.
3. **Deterministic Memory:** Uses Reference Counting by default. Complexity is opt-in; strict compile-time analysis detects *potential* retain cycles. The runtime "Cycle Detector" only traces and marks objects when these specific conditions are met.
4. **Architectural Integrity:** The language enforces good habits, such as preventing fragile deep-linking across module boundaries and enforcing acyclic dependencies.

---

## 1. Project Structure

Autopilot enforces a strict physical layout for code to ensure scalability.

### Modules

A **Module** is the fundamental unit of organization.

* A module consists of one or more `.ap` files in the **same folder**.
* **Rule:** The first non-comment line of every file must be the module declaration.
* **DAG Rule:** Module dependencies must form a **Directed Acyclic Graph**. Circular imports (two modules importing each other) are forbidden.

```c
// src/main.ap
module main

/* Multi-line comments use C-style syntax.
  Imports and Defines go below.
*/

```

### Imports & Path Resolution

Autopilot uses a robust import system designed to withstand refactoring. It supports standard relative paths and two unique wildcards:

* `.` **(Current/Down):** Look in the current directory or descend into a subfolder.
* `..` **(Up):** Go up one directory level.
* `^` **(Anchor Up):** Go up the tree until you find a folder with this name.
* `:` **(Deep Search):** Search recursively downwards for a unique sub-folder.

**Syntax:**

```ruby
import <Item> as <Alias> from module <Name> location <Path>

```

**Examples:**

```ruby
// 1. Standard relative path (Longer path example)
import User as AuthUser from module auth location .models.users

// 2. Renaming an item on import
import GenericReader as BufferReader from module io location ^src.utils

// 3. Anchor Search (Go up to 'src', then into 'utils')
import Logger from module logging location ^src.utils

// 4. Deep Search (Find 'legacy' anywhere inside 'src')
import Parser from module xml location ^src:legacy

// 5. Built-in Library (No location needed)
import String from library system

```

---

## 2. Memory Management

Autopilot uses a unique hybrid memory model: **Reference Counting (RC) + Compile-Time Cycle Detection**.

### The Default (RC)

By default, all Structs and Functions in Autopilot are **acyclic**.

* **Performance:** Code runs with simple, fast Reference Counting.
* **Safety:** The compiler guarantees these structures cannot form memory leaks (retain cycles).

### The Cycle Detector

If you need recursion or self-referential data (like a Graph), you must explicitly mark the type as `cyclic`.

* **Behavior:** The compiler analyzes `cyclic` types for potential retain cycles. If a potential cycle is detected, the runtime "Cycle Detector" is triggered for that specific object graph. It traces the local heap to mark and sweep self-referencing objects.
* **Cost:** You only pay the performance cost if the cycle condition actually arises.

```ruby
// Fast, simple RC (Default)
pub struct User is ... end

// Managed by Cycle Detector
pub cyclic struct Node is ... end

```

*Note: `inline` types (stack allocated) cannot be marked `cyclic`.*

---

## 3. The Type System

Autopilot is statically typed. All types must be defined.

### Primitives

| Type | Description |
| --- | --- |
| `int`, `long` | Signed Integers |
| `float`, `double` | Floating Point |
| `boolean` | `true`, `false` |
| `char`, `string` | **ASCII Only** |

### Explicit Specialization (`define`)

Autopilot does not use inline generics (e.g., `Vector<int>`). You must define a specialized type alias at the top of your file.

```ruby
// Create a specialized Vector for integers
define Vector(int) as IntVec

// Create an Optional wrapper for strings
define Optional(string) as StringOpt

```

### Structs

Structs are the primary complex data type. They define fields and methods.

```ruby
pub struct Player is
  pub name as string,
  score as int,

  pub fun add_score(points as int) do
    // No 'self' keyword; fields are accessed directly
    score = score + points
  end
end

```

### Enums & Unions

* **Enums:** Strictly for primitives (scalars).
* **Unions:** Tagged unions (Sum types) for holding one of several complex types.

```ruby
// Enum (Primitive values)
pub enum HttpStatus(int) is
  OK = 200,
  NotFound = 404
end

// Union (Complex types - e.g. for JSON parsing)
pub union JsonValue is
  obj as JsonObject,
  list as JsonArray
end

```

---

## 4. Variables & Expressions

### Declarations

* `let`: Immutable.
* `var`: Mutable.

**Type Inference:**
Inference is allowed locally, but **forbidden** for types crossing module boundaries.

```ruby
import Player from module game location .entities

let x = 10                  // OK (Inferred int)
let p as Player = ...       // OK (Explicit type required for external module)

```

### Operators & Precedence

Autopilot uses specific keywords for boolean logic (`and`, `or`, `xor`, `nand`, `nor`).

**Precedence (High to Low):**

1. Unary (`-`, `not`)
2. Exponents (`^`)
3. Multiplication (`*`, `/`, `%`)
4. Addition (`+`, `-`)
5. Comparison (`<`, `<=`, `==`, `!=`)
6. Boolean Logic

---

## 5. Control Flow

Autopilot requires the `do` keyword for blocks.

### Conditionals

```ruby
if x > 10 do
  print("High")
elif x < 5 do
  print("Low")
else
  print("Mid")
end

```

### Loops

Supports `while`, `loop` (infinite), and `for` (ranges/collections). Loops can be labeled.

```ruby
for i in 1..10 as count_loop do
  if i == 5 do
    break count_loop
  end
end

```

### Switch (Pattern Matching)

Switches must be exhaustive when handling Enums or Errors.

```ruby
switch status
  case HttpStatus.OK do
    handle_success()
  case HttpStatus.NotFound, HttpStatus.Busy do
    retry_connection()
  default do
    log_error()
end

```

---

## 6. Safety & Special Features

### No Nulls (Optionals)

Autopilot has no `null`. Missing values are handled via `Optional(T)`. Unwrapping is handled safely in control structures.

```ruby
// Unwraps 'maybe_user' if it exists; otherwise skips the block
if let u = maybe_user do
  print(u.name)
end

```

### Defer

`defer` schedules a statement to run at the end of the current scope.

* **Order:** **FIFO** (First-In, First-Out).

```ruby
fun operation() do
  defer log("Start")
  defer log("End")
  // Logs "Start" then "End" when function exits
end

```

### Module Boundary Enforcement

Method chaining (dot-syntax) is permitted but **cannot** infer types across module boundaries. Chains must be broken into explicit assignments if they return external types.

```ruby
import Order from module store location .sales

// ILLEGAL: Implicitly depends on types deep inside another module
// let item = user.get_order().get_item()

// CORRECT:
let order as Order = user.get_order()
let item = order.get_item()

```