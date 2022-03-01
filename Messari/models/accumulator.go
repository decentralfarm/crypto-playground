package models

type Accumulator struct {
	Market          int     `json:"market"`
	PriceSum        float64 `json:"-"`
	VolumeSum       float64 `json:"total_volume"`
	BuySum          int64   `json:"-"`
	PriceXVolumeSum float64 `json:"-"`
	Count           int64   `json:"count"`
	MeanPrice       float64 `json:"mean_price"`
	MeanVolume      float64 `json:"mean_volume"`
	VWAP            float64 `json:"volume_weighted_average_price"`
	PercentageBuy   float64 `json:"percentage_buy"`
}

func (a *Accumulator) Add(t Trade) {

	a.PriceSum += t.Price
	a.VolumeSum += t.Volume
	a.BuySum += map[bool]int64{true: 1, false: 0}[t.IsBuy]
	a.PriceXVolumeSum += t.Price * t.Volume
	a.Count++
}

func (a *Accumulator) CalculateMetrics() {
	a.MeanPrice = a.PriceSum / float64(a.Count)
	a.MeanVolume = a.VolumeSum / float64(a.Count)
	a.VWAP = a.PriceXVolumeSum / a.VolumeSum
	a.PercentageBuy = float64(a.BuySum) * 100 / float64(a.Count)
}
