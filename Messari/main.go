package main

import (
	"bufio"
	"challenge1/models"
	"encoding/json"
	"fmt"
	"log"
	"os"
	"sync"
)

func main() {
	marketsSummary := make(map[int](models.Accumulator))
	scanner := bufio.NewScanner(os.Stdin)
	var trade models.Trade
	for scanner.Scan() {
		if scanner.Text() == "BEGIN" {

		} else if scanner.Text() == "END" {
			var wg sync.WaitGroup
			for _, market := range marketsSummary {
				wg.Add(1)
				go func(market models.Accumulator) {
					defer wg.Done()
					market.CalculateMetrics()
					s, _ := json.Marshal(market)
					fmt.Println(string(s))
				}(market)
			}
			wg.Wait()
			return

		} else {

			json.Unmarshal([]byte(scanner.Text()), &trade)
			a := marketsSummary[trade.Market]
			if a.Count == 0 {
				a = models.Accumulator{Market: trade.Market,
					PriceSum: trade.Price, VolumeSum: trade.Volume, PriceXVolumeSum: trade.Price * trade.Volume, Count: 1}
			} else {
				a.Add(trade)
			}
			marketsSummary[trade.Market] = a

		}

	}

	if err := scanner.Err(); err != nil {
		log.Println(err)
	}
}
