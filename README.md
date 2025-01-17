# Nonnegative Matrix Factorization
MAT423 project

## Dataset 1 statistics (*small-medium*)
- 3 datasets
- Stock market end of day (eod) prices
- Dataset1 (*small*)
  - Time taken to scrape: 5 minutes
  - entries: 9,405 (627 x 3 x 5)
- Dataset1_MoreMarkets (*small*)
  - Time taken to scrape: 51 minutes, 1 second (45 minutes of downtime, 6 minutes to scrape)
  - entries: 11,000 (220 x 10 x 5)
- Dataset1_MoreMarkets_MoreTime (*medium*)
  - Time taken to scrape: 78 minutes, 51 seconds (45 minutes of downtime, 10 minutes to scrape, 20 minutes to process)
  - entries: 741,040 (118 x 10 x 628)
    - 741,000 single-precision floats $\\approx$ 3MB

## Dataset 2 statistics (*large*)
- 1 dataset
- Video: $\\approx$ 30fps, 1280 x 780, encoded as greyscale
- $\\approx$ 10 second video
- 331 frames
- entries: 330,470,400 (1280 x 780 x 331) 
  - 330,470,400 single-precision floats $\\approx$ 330MB

## Dataset 3 statistics (*very large*)
- 1 dataset (due to large size you can download it [here](https://drive.google.com/drive/folders/1HnIdDjG_1YwkvRKqG99cYpXZIT9hLqr3?usp=drive_link))
- Time taken to generate: 21 minutes, 37 seconds
- Synthetic data, n=20, m=500, T=100,000 
- Used probability distributions 
- started at *83.9GB*, ended at *68.2GB*: $\\approx$ 15GB of data
- entries: 1,000,000,000 (20 x 500 x 100000) 
  - 1,000,000,000 single-precision floats $\\approx$ 1GB

## Results
- Dataset 1 on `Data/Dataset1/2024-12-02.csv`
```
FAST HALS
-----
Frobenius Norm Error: 67.80698904734199
iterations: 2539
multiplicative update
-----
Frobenius Norm Error: 67.96671671614328
iterations: 230
```

- Dataset 2 on `Data/Dataset2/friend_jazz_drumming_frame0.csv`
```
FAST HALS
-----
Frobenius Norm Error: 67.85951333182257
iterations: 4269
multiplicative update
-----
Frobenius Norm Error: 68.0684712196409
iterations: 220
```

- Dataset 3 on `Data/Dataset3/time_0.csv`
```
FAST HALS
-----
Frobenius Norm Error: 67.72928998644046
iterations: 3127
multiplicative update
-----
Frobenius Norm Error: 67.88559083199539
iterations: 240
```