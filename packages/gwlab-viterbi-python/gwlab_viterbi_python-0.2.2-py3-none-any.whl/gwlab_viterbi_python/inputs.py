from pydantic.dataclasses import dataclass
from enum import Enum


class _InputConfig:
    validate_assignment = True
    validate_all = True
    use_enum_values = True


class DataChoice(Enum):
    """Enum to give choices for data_choice"""
    REAL = 'real'
    SIMULATED = 'simulated'


class SourceDataset(Enum):
    """Enum to give choices for source_dataset"""
    O1 = 'o1'
    O2 = 'o2'
    O3 = 'o3'


@dataclass(config=_InputConfig)
class DataInput:
    """Convenient class to hold the inputs for where the data should come from"""

    data_choice: DataChoice = DataChoice.REAL
    """Choice of 'real' or 'simulated'"""

    source_dataset: SourceDataset = SourceDataset.O3
    """Choice of 'o1', 'o2' or 'o3'"""


@dataclass(config=_InputConfig)
class DataParametersInput:
    """Convenient class to hold the inputs for the data"""

    start_frequency_band: str = "188.0"
    """Atom frequency (Hz)"""

    min_start_time: str = "1238166483"
    """Minimum start time (GPS s)"""

    max_start_time: str = "1254582483"
    """Maximum start time (GPS s)"""

    asini: str = "0.01844"
    """Orbit projected semi-major axis (s)"""

    freq_band: str = "1.2136296"
    """Width of the frequency band (Hz)"""

    alpha: str = "4.974817413935078"
    """Right ascension (rad)"""

    delta: str = "-0.4349442914295658"
    """Declination (rad)"""

    orbit_tp: str = "1238161512.786"
    """Time of ascension (GPS s)"""

    orbit_period: str = "4995.263"
    """Orbital period (s)"""

    drift_time: str = "864000"
    """Coherence time (s)"""

    d_freq: str = "5.78703704e-07"
    """Frequency step size (Hz)"""


@dataclass(config=_InputConfig)
class SearchParametersInput:
    """Convenient class to hold the inputs for the search"""

    search_start_time: str = "1238166483"
    """Start time (GPS s)"""

    search_t_block: str = "864000"
    """Duration (s)"""

    search_central_a0: str = "0.01844"
    """Central search a0 (s)"""

    search_a0_band: str = "0.00012"
    """Search a0 band width (Hz)"""

    search_a0_bins: str = "1"
    """Search a0 number of bins"""

    search_central_p: str = "4995.263"
    """Central search period (s)"""

    search_p_band: str = "0.003"
    """Search period band width (Hz)"""

    search_p_bins: str = "1"
    """Search period number of bins"""

    search_central_orbit_tp: str = "1238160263.9702501"
    """Central search time of ascension (s)"""

    search_orbit_tp_band: str = "260.8101737969591"
    """Search time of ascension band width (Hz)"""

    search_orbit_tp_bins: str = "9"
    """Search time of ascension number of bins"""

    search_l_l_threshold: str = "296.27423"
    """Log-likelihood threshold"""
