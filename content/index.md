# Basenji Fan Club

**I like Basenjis**. Read my [first post here](/firstpost) (sorry the link doesn't work yet)

> The barkless wonder.

![A very nice basenji](images/basenji.jpg)

## Reasons I like Basenjis

- You can spend years learning about their quirks and still be surprised
- They have a personality that both kids and adults adore
- The AKC _didn't ruin them_
- They’re one of the most unique dog breeds in the world

## My favorite Basenji traits (in order)

1. Their yodels
2. Their cat-like cleanliness
3. Their curled tails
4. Their endless curiosity
5. Their independence
6. Their speed
7. Their stubbornness
8. Their intelligence
9. Their playfulness

## Coding a Basenji day

```go
package main

import (
	"fmt"
	"time"
)

// BasenjiRoutine simulates a day in the life of a Basenji
func BasenjiRoutine() {
	actions := []string{
		"Wake up and stretch",
		"Refuse to go outside",
		"Zoomies around the house",
		"Steal a sock",
		"Take a nap in the sun",
		"Demand food, but pretend to be disinterested",
		"Chase imaginary prey",
		"Yodel at nothing",
		"Ignore commands",
		"Snuggle up and sleep",
	}

	fmt.Println("A day in the life of a Basenji:")
	for _, action := range actions {
		fmt.Println("- " + action)
		time.Sleep(1 * time.Second) // Simulate time passing
	}

	fmt.Println("End of the day. Ready to repeat tomorrow!")
}

func main() {
	BasenjiRoutine()
}
```
