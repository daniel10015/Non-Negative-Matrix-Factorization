# Non-Negative Matrix Factorization

## Dataset 1 statistics (*small-medium*)
- Stock market end of day (eod) prices
- Dataset1 *(small)*
  - 5 minutes
  - entries: 9,405 (627 x 3 x 5)
- Dataset1_MoreMarkets (*small*)
  - 51 minutes, 1 second
  - entries: 11,000 (220 x 10 x 5)
- Dataset1_MoreMarkets_MoreTime (*medium*)
  - 78 minutes, 51 seconds
  - entries: 741,040 (118 x 10 x 628)
    - 741,000 single-precision floats $\\approx$ 3mB

## Dataset 2 statistics (*very large*)
- Video: $\\approx$ 30fps, 1280 x 780, encoded as greyscale
- $\\approx$10 second video
- 331 frames
- entries: 330,470,400 (1280 x 780 x 331) 
  - 330,470,400 single-precision floats $\\approx$ 330mB