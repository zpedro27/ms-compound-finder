import os
import glob
import yaml
import pandas as pd
import seaborn as sns
from scripts.msdata import MSData


def load_config():
    with open("config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

    sns.set(**cfg["general_plotting"])
    return cfg


def samples_to_load(directory: str, file_extension: str = ".csv"):
    
    full_path = os.path.join(directory, f"*{file_extension}")
    all_files = glob.glob(full_path)

    return {_get_name_without_extension(file): file for file in all_files}


def _get_name_without_extension(path: str):
    return os.path.basename(path).split(".")[0]


def load_data(samples: dict):
    data_loaded = []
    for sample_name, file in samples.items():
        df = pd.read_csv(file)
        sample = MSData(sample_name, df)
        data_loaded.append(sample)
    return data_loaded


def subtract_blank_peaks(sample: MSData, blank: MSData, rounding: int = 2):
    """ 
    Determines the location (i.e. m/z values) of the peaks in the sample and in the blank.
    Values are rounded to the number of decimal places defined by the user (default: 2 decimal places).
    Returns the set of peak locations that show up in the sample, but not in the blank.
    """
    blank_peaks_rounded = _rounded_peak_mass(blank, rounding)
    sample_peaks_rounded = _rounded_peak_mass(sample, rounding)
    
    only_in_sample = _peak_difference(sample_peaks_rounded, blank_peaks_rounded)
    
    df_peaks = sample.peak
    
    print("Input:")
    print(f">> peaks in {sample.condition}: {len(sample_peaks_rounded)}")
    print(f">> peaks in {blank.condition} (blank): {len(blank_peaks_rounded)}")
    print("Output:")
    print(f">> {len(only_in_sample)} peaks in {sample.condition} not found in the {blank.condition}")
    print("********")

    return only_in_sample, df_peaks.loc[df_peaks.Mass.round(rounding).isin(list(only_in_sample))]


def _rounded_peak_mass(x: MSData, rounding: int):
    peaks = x.peak.Mass.values
    rounded_peaks = peaks.round(rounding)
    return rounded_peaks


def _peak_difference(peaks_samp, peaks_ref):
    set1 = set(peaks_ref)
    set2 = set(peaks_samp)
    return set2.difference(set1)