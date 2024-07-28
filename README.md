# Identification of common compounds in liquid samples 

## Background
We are given two samples of media in which cells had been growing. We furthermore have good reasons to believe that, in both cases, cells released a few of the same chemical compounds into the medium - but we don't know what these compounds are. How can we identify them?

One approach is to analyze each sample by mass spectrometry (LC-MS). Since this is an extremely sensitive technique, we obtain, for each sample, a list with **thousands** of putative compounds that were ionized and detected by the spectrometer. This "raw data" is the MS1-spectrum, where each "peak" corresponds to an ionized compound, and is characterized by a value of mass-to-charge ratio, $m/z$, and an $Intensity$ that depends primarily on its abundance.

Yet, it is clear that not all those potential compounds that we detected were actually released by the cells: first, some of the "peaks" in the spectra are just noise from the device; second, some compounds might have already been in the growth medium before the cells were added.

If we manage to get rid of these two types of "confounders" from our signal, we can focus our attention on a much more reduced set of compounds, i.e., those that are shared by the two samples. The advantage of this initial analysis is that we can then re-run our samples through the LC-MS, but this time targeting just **a few dozens** of ions for fragmentation, which allows us to obtain the MS2-spectrum of each. These spectra allow for an easy identification of the compounds.


## Approach
1. Remove noisy peaks by setting an appropriate threshold on the intensity of each peak
2. Exclude from each sample the peaks that are also present in a blank
3. Find the peaks shared by the samples of interest