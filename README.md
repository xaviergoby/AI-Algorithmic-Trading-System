# Forecasting with Fast Fourrier Transformations (FFT's)

**Problem**: How do I decompose a time-series into something simple (for then performing
forecasting with it)?


**Key Idea**: Decomposition

**Main idea (Key to the Algo)**: A reasonably continouos and periodic function can be represented/expressed
as the sum of a series  of sine functions/keys.

Sine/Sinusoidal Function: f(t) = Asin(wt + theta)

Where:
+ A: Amplitude
+ w: angular frequency
+ theta: Phase-shift

Period: T = 2pi / w


If I can apply a forecasting technique to each of my sine functions/signals obtained from
my OG time-series then I can then recombine my forecastings and get my forecasting result.

The more and more sine functions I use/apple, the better my approximation of the OG TS 
becomes.

FFT Steps:
1. Fun FFT on input data
2. Filter out low-amplitude or high-frequency components.
Data which has very low-amp and/or high-freq is most likely noise b/c it happens very
frequently and very irregularly.
4. Pick the first few most significant sine functions
3. Apply forecast on each of the individual components (sine functions/signals). Basically 
I need to move my phase forward (heh?).
4. Recombine the result of the above in order to get my final forecast.


Market sim updates Portfolio with:
1. Current date
2. Current price

































