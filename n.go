package main

import (
    "strconv"
    "fmt"
)

func main() {
    t := ""
    for i := 0; i< 10000000; i++ {
         t += strconv.Itoa(i)
    }
    fmt.Print("go")
}
