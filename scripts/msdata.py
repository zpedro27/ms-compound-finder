import matplotlib.pyplot as plt
from scipy.signal import find_peaks


class MSData():
    def __init__(self, cond, raw_data):
        self._condition = cond
        self._rawdata = raw_data
        self._peaks = None
        self._peak_params = None

    def __repr__(self):
        return f"{self.condition} - {self.raw_data.shape}"

    @property
    def condition(self):
        return self._condition

    @property
    def raw_data(self):
        return self._rawdata
    
    @property
    def peak(self):
        return self._peaks
    
    @property
    def peak_params(self):
        return self._peak_params
    
    def get_rawdata_without_null(self):
        return self.raw_data.loc[self.raw_data.Intensity > 0]
    
    def get_peaks(self, **kwargs):    
        """
        https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html
        """
        df = self.raw_data
        
        # Store peaks:
        idx, _ = find_peaks(df.Intensity,  **kwargs)
        df_peaks = df.iloc[idx]
        self._peaks = df_peaks
        
        # Store parameters used:
        params = {} 
        params.update(dict(**kwargs))
        self._peak_params = params
        return
    
    def plot_data(self, ax=None, display_peaks=True):
        df_peaks = self.peak
        df_data = self.raw_data
    
        if ax is None:
            f, ax = plt.subplots()

        # Display peaks:
        if (df_peaks is not None) & (display_peaks is True):
            df_peaks.plot(x="Mass", y="Intensity", color="red", marker="o", linestyle="", label="detected-peaks", ax=ax)
        
        # Display raw data:
        df_data.plot(x="Mass", y="Intensity", label="raw-data", ax=ax)

        ax.set_xlabel("m/z")
        return ax