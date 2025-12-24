package main

func main() {
    var a int = other_func(1, 2)
    defer call_me()
    if((a>2)) {
        var x int = 0
    } else if((a==2)) {
        var z int = 4
    } else {
        var y int = 0
    }
    switch a {
    case 1,2,3:
        var kk := 0
    default:
        var zz := 0
    }
    for {
        var at float = 0.1
        break
        for {
            var at float = 0.1
            continue
        }
    }
    if(!(true)) {
        var b int = 10
    }
    for (true) {
        doesnt_exist.method(a, (b+c), 10)
    }
    for k, v:= range some_Collection {
        var r := k
    }
    for _, value := range normal_collection {
        var t int = value
    }
    for may_var := 1; may_var < 10; may_var += 4 {
        var k := (may_var/2)
    }
}

func other_func(a int, b int) int {
    var c int = another_function()
    return (a+(b-c))
}

func call_me() {
    var a int = 0
}

func secondary_another_function() int {
    var collection := map[UNKNOWN]UNKNOWN {
        "a":"b",
        "b":"c"
    }

    return 0
}
