from abc import ABC, abstractmethod
from copy import deepcopy
from pathlib import Path
from math import sqrt, ceil
import warnings
import numpy as np
from scipy import fft, signal
from IPython.display import display
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
from bokeh.models.mappers import LinearColorMapper
from bokeh.models.ranges import DataRange1d
from bokeh.models.tools import PanTool, BoxZoomTool, WheelZoomTool, ZoomInTool, ZoomOutTool, SaveTool, ResetTool, HoverTool, InspectTool
from bokeh.palettes import Viridis256
from bokeh.io import output_notebook
from .bokeh_audio_tools import AudioPlayerTool
from .util import Audio
from .functional import envelope, read_audio_file, resample
from .tf_rep import overlapping_triangular_filterbank, mel_bins, twelve_tet_bins, _delta_freq_mel, _delta_freq_12tet


__all__ = ['Signal', 'TimeSignal', 'AudioSignal', 'Spectrum', 'PowerSpectrum', 'Spectrogram']


try:
    ipyname = get_ipython().__class__.__name__
    ipymodule = get_ipython().__class__.__module__
    if ipyname == 'ZMQInteractiveShell' or ipymodule == 'google.colab._shell':
        output_notebook()
except NameError:
    pass


def _get_samples_and_rate(input_signal, samplerate):
    if isinstance(input_signal, TimeSignal):
        if samplerate is not None:
            warnings.warn('Explicitly defined samplerate gets ignored when input is a {}'.format(type(input_signal)))
        samples = input_signal._samples
        samplerate = input_signal.samplerate
    elif np.ndim(input_signal) > 0:
        if samplerate is None:
            raise ValueError('The samplerate needs to be defined explicitly when input is an array or other iterable')
        samples = np.asarray(input_signal)
    else:
        raise TypeError('Only TimeSignal, Numpy arrays or other iterables are supported as input, not {}'.format(type(input_signal)))
    return samples, samplerate


def _get_samples(input_signal):
    if isinstance(input_signal, TimeSignal):
        return input_signal._samples
    elif np.ndim(input_signal) > 0:
        return np.asarray(input_signal)
    else:
        raise TypeError('Only TimeSignal, Numpy arrays or other iterables are supported as input, not {}'.format(type(input_signal)))


def _get_both_samples_and_rate(input_signal1, input_signal2, samplerate=None):
    samples1, samplerate1 = _get_samples_and_rate(input_signal1, samplerate)
    samples2, samplerate2 = _get_samples_and_rate(input_signal2, samplerate)
    if samplerate1 != samplerate2:
        raise ValueError('Both signals need to have the same samplerate')
    return samples1, samples2, samplerate1


def _get_both_samples(input_signal1, input_signal2):
    samples1 = _get_samples(input_signal1)
    samples2 = _get_samples(input_signal2)
    if isinstance(input_signal1, TimeSignal) and isinstance(input_signal2, TimeSignal) and input_signal1.samplerate != input_signal2.samplerate:
        raise ValueError('Both signals need to have the same samplerate')
    return samples1, samples2


def same_type_as(output_samples, input_signal):
    if isinstance(input_signal, TimeSignal):
        return type(input_signal)(output_samples, input_signal.samplerate)
    else:
        return output_samples


class Signal(ABC):
    """Abstract base class defining a generic signal.
    """
    def __init__(self):
        self._allowed_fig_args = figure.properties() - {'visible'} | {'active_drag', 'active_inspect', 'active_multi', 'active_scroll', 'active_tap', 'tools', 'tooltips', 'x_axis_label', 'x_axis_location', 'x_axis_type', 'y_minor_ticks', 'y_axis_label', 'y_axis_location', 'y_axis_type', 'y_minor_ticks'}
        self._default_fig_args = {
            'width': 900,
            'height': 300,
            'toolbar_location': 'above',
            'tools': [
                PanTool(),
                BoxZoomTool(),
                WheelZoomTool(),
                ZoomInTool(),
                ZoomOutTool(),
                SaveTool(),
                ResetTool(),
            ],
        }


    @property
    @abstractmethod
    def data(self):
        pass


    @data.setter
    @abstractmethod
    def data(self, in_data):
        pass


    @abstractmethod
    def plot(self, fig=None, **plot_args):
        if fig is None:
            fig_args = deepcopy(self._default_fig_args) # deepcopy is needed to avoid sharing tool instances between subsequent calls to plot
            fig_args.update({k: v for k, v in plot_args.items() if k in self._allowed_fig_args})
            if fig_args['tooltips'] is not None:
                fig_args['tools'].append(HoverTool(mode='vline'))
            fig = figure(**fig_args)
        return fig


    def _repr_html_(self):
        return show(self.plot())


    def display(self, **plot_args):
        show(self.plot(**plot_args))


    @abstractmethod
    def __len__(self):
        pass


    @abstractmethod
    def rms(self):
        pass


    @abstractmethod
    def power(self, dB=True):
        pass


    def _get_compatible_data(self, other):
        if isinstance(other, Signal):
            other_data = other.data
        else:
            other_data = np.asarray(other)
        if np.issubdtype(other_data.dtype, np.number):
            return other_data
        raise TypeError('Only Signals or numeric iterables are supported as operands, not {}'.format(type(other)))


    def _get_compatible_size_data(self, other):
        other_data = self._get_compatible_data(other)
        if other_data.size != self.data.size:
            raise ValueError('Signals need to have the same size')
        return other_data


    def __add__(self, other):
        if np.isscalar(other):
            return same_type_as(self.data + other, self)
        other_data = self._get_compatible_size_data(other)
        return same_type_as(self.data + other_data, self)


    def __radd__(self, other):
        if np.isscalar(other):
            return same_type_as(other + self.data, self)
        other_data = self._get_compatible_size_data(other)
        return same_type_as(other_data + self.data, self)


    def __sub__(self, other):
        if np.isscalar(other):
            return same_type_as(self.data - other, self)
        other_data = self._get_compatible_size_data(other)
        return same_type_as(self.data - other_data, self)


    def __rsub__(self, other):
        if np.isscalar(other):
            return same_type_as(other - self.data, self)
        other_data = self._get_compatible_size_data(other)
        return same_type_as(other_data - self.data, self)


    def __mul__(self, other):
        if np.isscalar(other):
            return same_type_as(self.data * other, self)
        other_data = self._get_compatible_size_data(other)
        return same_type_as(self.data * other_data, self)


    def __rmul__(self, other):
        if np.isscalar(other):
            return same_type_as(other * self.data, self)
        other_data = self._get_compatible_size_data(other)
        return same_type_as(other_data * self.data, self)


    def __truediv__(self, other):
        if np.isscalar(other):
            return same_type_as(self.data / other, self)
        other_data = self._get_compatible_size_data(other)
        return same_type_as(self.data / other_data, self)


    def __rtruediv__(self, other):
        if np.isscalar(other):
            return same_type_as(other / self.data, self)
        other_data = self._get_compatible_size_data(other)
        return same_type_as(other_data / self.data, self)


    def __pow__(self, other):
        if np.isscalar(other):
            return same_type_as(self.data ** other, self)
        other_data = self._get_compatible_size_data(other)
        return same_type_as(self.data ** other_data, self)


    def __rpow__(self, other):
        if np.isscalar(other):
            return same_type_as(other ** self.data, self)
        other_data = self._get_compatible_size_data(other)
        return same_type_as(other_data ** self.data, self)


    def __and__(self, other):
        if np.isscalar(other):
            return same_type_as(np.tile(self.data, other), self)
        other_data = self._get_compatible_data(other)
        return same_type_as(np.concatenate((self.data, other_data)), self)


class OneDimensionalMixin:
    """A helper class providing functionality for 1D signals.
    """
    _default_line_args = {
        'line_width': 2,
    }


    def rms(self):
        return sqrt(self.power(dB=False))


class TimeMixin:
    """A class representing a sampled time-signal.
    """
    samplerate: float
    times: np.array


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._default_fig_args['x_axis_label'] = 'time [s]'


    def __len__(self):
        return len(self.times)


    def _get_compatible_data(self, other):
        if isinstance(other, TimeMixin) and self.samplerate != other.samplerate:
            raise ValueError('Signals need to have the same sample rates')
        return super()._get_compatible_data(other)


    def frames(self, frame_duration=None, frame_size=None, step_duration=None, step_size=None, step_ratio=None):
        return [same_type_as(frame_samples, self) for frame_samples in self.frame_data(
            frame_duration, frame_size, step_duration, step_size, step_ratio).T]


    def frame_data(self, frame_duration=None, frame_size=None, step_duration=None, step_size=None, step_ratio=None):
        frame_size, overlap_size = TimeMixin._parse_frame_params(frame_duration, frame_size, step_duration, step_size, step_ratio,
                                                       self.samplerate, 'linear', None)
        step_size = frame_size - overlap_size
        samples = np.pad(self._samples, (frame_size//2, 0), 'constant')
        num_frames = ((len(samples)-frame_size//2) // step_size) + 1
        num_fill_samples = (num_frames-1)*step_size+frame_size-len(samples)
        if num_fill_samples > 0:
            samples = np.pad(samples, (0, num_fill_samples), 'constant')
        return np.array([samples[i:i+frame_size] for i in range(0, len(samples)-frame_size+1, step_size)]).T


    @staticmethod
    def _parse_frame_params(
        frame_duration, frame_size, step_duration, step_size, step_ratio, samplerate, spacing, min_freq
    ):
        frame_specs = sum([frame_duration is not None, frame_size is not None])
        if frame_specs != 1:
            if spacing == 'linear':
                raise ValueError('Specify a frame width either as duration in seconds or size in samples')
            if min_freq is None:
                raise ValueError('Specify either a minimum frequency or a frame width in seconds or in samples')
        if frame_duration is not None:
            frame_size = round(frame_duration * samplerate)
        elif frame_size is None and min_freq is not None and spacing != 'linear':
            frame_size = ceil(samplerate / min_freq)

        if sum([step_duration is not None, step_size is not None, step_ratio is not None]) > 1:
            raise ValueError('Specify a frame step either as duration in seconds, size in samples or ratio')
        if step_duration is not None:
            overlap_size = round((frame_duration-step_duration) * samplerate)
        elif step_size is not None:
            overlap_size = frame_size - step_size
        elif step_ratio is not None:
            overlap_size = round((1-step_ratio) * frame_size)
        else:
            overlap_size = frame_size // 2
        return frame_size, overlap_size


class TimeSignal(OneDimensionalMixin, TimeMixin, Signal):
    """A class representing a one-dimensional sampled time-signal.
    """
    def __init__(self, samples, samplerate, *, times=None):
        super().__init__()
        self._samples = samples
        self.samplerate = samplerate
        self.times = np.arange(len(samples)) / samplerate if times is None else times
        self._default_fig_args['y_axis_label'] = 'amplitude'
        self._default_fig_args['tooltips'] = [('time [s]', '@x{0.000}'), ('amplitude', '@y{0.000}')]


    @classmethod
    def from_spectrogram(cls, specgram):
        if specgram.spacing != 'linear':
            raise ValueError('Inversion of non-linear spectrograms is not supported')
        if not signal.check_NOLA(specgram.window, specgram._frame_size, specgram._overlap_size):
            raise ValueError('A spectrogram created with this combination of parameters cannot be inverted')
        if not signal.check_COLA(specgram.window, specgram._frame_size, specgram._overlap_size):
            warnings.warn('A spectrogram created with this combination of parameters cannot be perfectly inverted')
        times, samples = signal.istft(
            specgram.complex, specgram._input_samplerate, specgram.window,
            specgram._frame_size, specgram._overlap_size, specgram._fft_size,
        )
        return cls(np.clip(samples, -1, 1), specgram._input_samplerate, times=times)


    @classmethod
    def from_spectrum(cls, spectrum):
        samples = fft.irfft(spectrum.complex, spectrum._fft_size, norm='forward')
        return cls(samples, spectrum._input_samplerate)


    @classmethod
    def from_processing_timesignal(cls, input_signal, block_size, processing_fn, state_data=None, output_samplerate=None):
        input_samples = _get_samples(input_signal)
        total_length = len(input_signal)
        output_samples = []

        # Pass input sliced into blocks to processing function
        for start in np.arange(0, total_length - block_size, block_size):
            input_buffer = input_samples[start:start+block_size]
            output_buffer = processing_fn(input_buffer, state_data)
            if output_buffer is not None:
                output_samples.append(output_buffer)

        # Pass partial buffer at end of signal
        start += block_size
        final_output_buffer = processing_fn(input_samples[start:], state_data)
        if final_output_buffer is not None:
            output_samples.append(final_output_buffer)

        if len(output_samples) > 0:
            if output_samplerate is None:
                output_samplerate = input_signal.samplerate
            return cls(np.hstack(output_samples), output_samplerate)


    @property
    def data(self):
        return self._samples


    @data.setter
    def data(self, in_data):
        self._samples = in_data


    def power(self, dB=True):
        power = np.mean(self.data ** 2)
        return 10*np.log10(max(power, 1e-12)) if dB else power


    def plot(self, fig=None, as_line=True, **plot_args):
        fig = super().plot(fig, **plot_args)
        line_args = {**self._default_line_args, **{k: v for k, v in plot_args.items() if k not in self._allowed_fig_args}}
        if as_line:
            fig.line(self.times, self._samples, **line_args)
        else:
            line_args.pop('mode', None)
            fig.step(np.concatenate((self.times, [len(self) / self.samplerate])), np.concatenate((self._samples, self._samples[-1:])), mode='after', **line_args)
        return fig


    def filter(self, coefficients):
        if isinstance(coefficients, tuple):
            if len(coefficients) == 1:
                numerator, = coefficients
                denominator = 1
            else:
                numerator, denominator = coefficients
                filtered_data = signal.lfilter(numerator, denominator, self.data)
        else:
            filtered_data = signal.lfilter(coefficients, 1, self.data)
        return same_type_as(filtered_data, self)


    def resample(self, samplerate):
        resampled_signal = deepcopy(self)
        if samplerate != self.samplerate:
            resampled_signal.samplerate = samplerate
            resampled_signal._samples = resample(self._samples, self.samplerate, samplerate)
            resampled_signal.times = np.arange(len(resampled_signal._samples)) / samplerate
        return resampled_signal


    def envelope(self, *, method='analytical', param=1):
        envelope_samples = envelope(self._samples, method=method, param=param)
        return TimeSignal(envelope_samples, self.samplerate)


class AudioSignal(TimeSignal):
    """A class representing an audio signal with sample values between -1 and 1.
    
    Has playback functionality through the play() method.
    """
    def __init__(self, samples, samplerate, *, times=None):
        super().__init__(samples, samplerate, times=times)
        self._default_fig_args['y_range'] = (-1.09, 1.09)
        self._default_fig_args['tools'] = [
            PanTool(dimensions='width'),
            BoxZoomTool(),
            WheelZoomTool(dimensions='width'),
            ZoomInTool(dimensions='width'),
            ZoomOutTool(dimensions='width'),
            AudioPlayerTool(samplerate=samplerate),
            SaveTool(),
            ResetTool(),
        ]


    @classmethod
    def from_file(cls, file_path, samplerate=None):
        samples = read_audio_file(file_path, samplerate)
        return cls(samples, samplerate)


    @classmethod
    def from_recording(cls, recording_device, recording_samplerate, block_size):
        recorded_samples = []
        with recording_device.recorder(samplerate=recording_samplerate, channels=1) as recorder:
            try:
                while True:
                    recorded_buffer = np.clip(np.squeeze(recorder.record(numframes=block_size)), -1, 1)
                    recorded_samples.append(recorded_buffer)
            except KeyboardInterrupt:
                return cls(np.hstack(recorded_samples), recording_samplerate)


    @classmethod
    def from_processing_recording(cls, recording_device, recording_samplerate, block_size, processing_fn, state_data=None, output_samplerate=None):
        output_samples = []
        with recording_device.recorder(samplerate=recording_samplerate, channels=1) as recorder:
            try:
                while True:
                    recorded_buffer = np.clip(np.squeeze(recorder.record(numframes=block_size)), -1, 1)
                    output_buffer = processing_fn(recorded_buffer, state_data)
                    if output_buffer is not None:
                        output_samples.append(output_buffer)
            except KeyboardInterrupt:
                if len(output_samples) > 0:
                    if output_samplerate is None:
                        output_samplerate = recording_samplerate
                    return cls(np.hstack(output_samples), output_samplerate)


    def play(self, normalize=False):
        return display(Audio(self._samples, rate=self.samplerate, normalize=normalize))


class SpectralMixin:
    def __init__(self, magnitude, phase, nyquist_freq, bin_frequencies, bin_units, fft_size, dB, spacing, window, exponent, norm_single_side_band, **kwargs):
        super().__init__(**kwargs)
        self.magnitude = magnitude
        self.phase = phase
        self.frequencies = bin_frequencies
        self._bin_units = bin_units
        self._fft_size = fft_size
        self.dB = dB
        self.spacing = spacing
        self.window = window
        self.exponent = exponent
        self._input_samplerate = 2 * nyquist_freq
        self._norm_single_side_band = norm_single_side_band


    @property
    def data(self):
        return (self.magnitude, self.phase)


    @data.setter
    def data(self, in_data):
        self.magnitude, self.phase = in_data


    @property
    def complex(self):
        if self.dB:
            magnitude = 10 ** (self.magnitude / 20)
        else:
            magnitude = self.magnitude ** (1/self.exponent)
        if self._norm_single_side_band:
            if self._fft_size % 2 == 0:
                magnitude[1:-1] /= sqrt(2)
            else:
                magnitude[1:] /= sqrt(2)
        return magnitude * np.exp(1j*self.phase)


    @staticmethod
    def _check_freq_params(spacing, num_bins, max_freq, min_freq, nyquist_freq, sig_len, len_description):
        if max_freq is None:
            max_freq = nyquist_freq
        if min_freq is not None and min_freq < 1 / sig_len:
            raise ValueError(f'The given minimum frequency is too small for {len_description}')
        if spacing == 'log':
            if num_bins is None:
                raise ValueError(f'The number of bins per semitone needs to be given as "num_bins" when requesting {spacing}-spaced frequencies')
            if min_freq is None or min_freq <= 0 or min_freq >= max_freq:
                raise ValueError(f'A minimum frequency above 0 and below the maximum frequency needs to be given when requesting {spacing}-spaced frequencies')
        elif spacing == 'linear':
            if num_bins is None:
                num_bins = sig_len
        else:
            raise ValueError('The frequency spacing needs to be one of "linear", "log" or "mel"')
        if spacing == 'mel':
            fft_size_for_spacing = ceil(2 * nyquist_freq / _delta_freq_mel(num_bins / 2, min_freq, max_freq)) # CHECK: WHY / 2?
        elif spacing == 'log':
            fft_size_for_spacing = ceil(2 * nyquist_freq / _delta_freq_12tet(min_freq, num_bins / 2)) # CHECK: WHY / 2?
        else:
            fft_size_for_spacing = num_bins
        fft_size = max(sig_len, fft_size_for_spacing)
        return max_freq, num_bins, fft_size


    @staticmethod
    def _bins_for_spacing(spacing, num_bins, min_freq, max_freq, nyquist_freq):
        if spacing == 'mel':
            return mel_bins(num_bins, min_freq, max_freq, nyquist_freq)
        if spacing == 'log':
            return twelve_tet_bins(num_bins, min_freq, max_freq, nyquist_freq)
        if spacing == 'linear':
            lin_freqs = np.arange(num_bins//2+1) * 2 * nyquist_freq / num_bins
            if min_freq is None:
                min_idx = None
            else:
                min_idx = np.argmin(np.abs(np.where(lin_freqs < min_freq, np.inf, lin_freqs) - min_freq))
            if max_freq is None:
                max_idx = None
            else:
                max_idx = np.argmin(np.abs(np.where(lin_freqs > max_freq, np.inf, lin_freqs) - max_freq))
            retained_freqs = lin_freqs[min_idx:max_idx+1]
            return retained_freqs, retained_freqs


    @staticmethod
    def _filter_and_scale(spectral_values, spacing, num_bins, min_freq, max_freq, nyquist_freq, fft_size, norm_single_side_band, dB, exponent):
        if spacing == 'linear':
            lin_freqs = np.arange(num_bins//2+1) * 2 * nyquist_freq / num_bins
            if min_freq is None:
                min_idx = None
            else:
                min_idx = np.argmin(np.abs(np.where(lin_freqs < min_freq, np.inf, lin_freqs) - min_freq))
            if max_freq is None:
                max_idx = None
            else:
                max_idx = np.argmin(np.abs(np.where(lin_freqs > max_freq, np.inf, lin_freqs) - max_freq))
            filtered_values = spectral_values[min_idx:max_idx+1]
        else:
            if spacing == 'mel':
                _, bin_frequencies = mel_bins(num_bins, min_freq, max_freq, nyquist_freq)
            if spacing == 'log':
                _, bin_frequencies = twelve_tet_bins(num_bins, min_freq, max_freq, nyquist_freq)
            filterbank = overlapping_triangular_filterbank(bin_frequencies, fft_size, 2 * nyquist_freq, normalize=False)
            filtered_values = np.matmul(filterbank, spectral_values)
        magnitude = np.abs(filtered_values)
        phase = np.angle(filtered_values)

        if norm_single_side_band:
            if fft_size % 2 == 0:
                magnitude[1:-1] *= sqrt(2)
            else:
                magnitude[1:] *= sqrt(2)
        if dB:
            magnitude = 20 * np.log10(np.maximum(magnitude, 1e-6))
        else:
            magnitude **= exponent

        return magnitude, phase


    @property
    def _bin_label(self):
        if self.spacing == 'linear':
            return 'frequency [Hz]'
        if self.spacing == 'mel':
            return 'mel'
        if self.spacing == 'log':
            return 'MIDI number'


class Spectrum(SpectralMixin, OneDimensionalMixin, Signal):
    """ A class representing a complex spectrum.
    """
    def __init__(
        self, magnitude, phase, nyquist_freq, *,
        dB=True, min_freq=None, max_freq=None, num_bins=None,
        norm_single_side_band=False, spacing='linear', window=None, exponent=1,
    ):
        max_freq, num_bins, fft_size = SpectralMixin._check_freq_params(spacing, num_bins, max_freq, min_freq, nyquist_freq, len(magnitude), 'a signal of this length')
        bin_units, bin_frequencies = SpectralMixin._bins_for_spacing(spacing, num_bins, min_freq, max_freq, nyquist_freq)
        super().__init__(magnitude, phase, nyquist_freq, bin_frequencies, bin_units, fft_size, dB, spacing, window, exponent, norm_single_side_band)
        self._default_fig_args['tooltips'] = [('frequency [Hz]', '@frequency{0.000}'), ['magnitude', '@magnitude{0.000}']]
        self._default_fig_args['x_axis_label'] = self._bin_label
        self._default_fig_args['y_axis_label'] = 'magnitude'
        if spacing in ('mel', 'log'):
            self._default_fig_args['tooltips'].insert(0, (self._bin_label, '@bin_unit{0.0}'))
        if exponent == 2 or dB:
            self._default_fig_args['y_axis_label'] = 'power'
            self._default_fig_args['tooltips'][-1][0] = 'power'
        if dB:
            self._default_fig_args['y_axis_label'] += ' [dB]'
            self._default_fig_args['tooltips'][-1][0] += ' [dB]'


    @classmethod
    def from_timesignal(cls, input_signal, *, dB=True, min_freq=None, max_freq=None, num_bins=None,
        norm_single_side_band=False, spacing='linear', window=None, exponent=1,
        samplerate=None,
    ):
        samples, samplerate = _get_samples_and_rate(input_signal, samplerate)
        nyquist_freq = samplerate / 2
        max_freq, num_bins, fft_size = cls._check_freq_params(spacing, num_bins, max_freq, min_freq, nyquist_freq, len(samples), 'a signal of this length')

        if window is not None:
            samples = samples * signal.get_window(window, len(samples), True) # do not multiply in place, otherwise in_data gets overwritten
        spectrum = fft.rfft(samples, fft_size, norm='forward')
        magnitude, phase = cls._filter_and_scale(spectrum, spacing, num_bins, min_freq, max_freq, nyquist_freq, fft_size, norm_single_side_band, dB, exponent)

        return cls(magnitude, phase, nyquist_freq,
            dB=dB, min_freq=min_freq, max_freq=max_freq, num_bins=num_bins,
            norm_single_side_band=norm_single_side_band, spacing=spacing, window=window, exponent=exponent,
        )


    def __len__(self):
        return len(self.frequencies)


    def plot(self, fig=None, **plot_args):
        fig = super().plot(fig, **plot_args)
        if isinstance(fig.x_range, DataRange1d):
            fig.x_range.range_padding = 0
        if isinstance(fig.y_range, DataRange1d):
            fig.y_range.range_padding = 0
        data_source = ColumnDataSource({'magnitude': self.magnitude, 'frequency': self.frequencies, 'bin_unit': self._bin_units})
        line_args = {**self._default_line_args, **{k: v for k, v in plot_args.items() if k not in self._allowed_fig_args}}
        fig.line(x='bin_unit', y='magnitude', source=data_source, **line_args)
        return fig


    def power(self, dB=True):
        if self.dB:
            power_per_freq = 10 ** (self.magnitude / 10)
        else:
            power_per_freq = self.magnitude ** (2/self.exponent)
        if self._norm_single_side_band:
            power = np.sum(power_per_freq)
        elif self._fft_size % 2 == 0:
            power = power_per_freq[0] + 2*np.sum(power_per_freq[1:-1]) + power_per_freq[-1]
        else:
            power = power_per_freq[0] + 2*np.sum(power_per_freq[1:])
        return 10*np.log10(max(power, 1e-12)) if dB else power


    def set_magnitude(self, value, start=None, end=None):
        start_idx = np.argmin(np.abs(self.frequencies - start)) if start is not None else 0
        end_idx = np.argmin(np.abs(self.frequencies - end)) if end is not None else len(self.frequencies)-1
        modified_spectrum = deepcopy(self)
        modified_spectrum.magnitude[start_idx:end_idx+1] = value
        return modified_spectrum


    def modify_magnitude(self, amount, start=None, end=None):
        start_idx = np.argmin(np.abs(self.frequencies - start)) if start is not None else 0
        end_idx = np.argmin(np.abs(self.frequencies - end)) if end is not None else len(self.frequencies)-1
        modified_spectrum = deepcopy(self)
        if self.dB:
            modified_spectrum.magnitude[start_idx:end_idx+1] = np.clip(modified_spectrum.magnitude[start_idx:end_idx+1] + amount, -120, None)

        else:
            modified_spectrum.magnitude[start_idx:end_idx+1] *= amount
        return modified_spectrum


class PowerSpectrum(Spectrum):
    """A class representing a complex power spectrum.
    """
    def __init__(self, magnitude, phase, nyquist_freq, **kwargs):
        exponent = kwargs.pop('exponent', None)
        if exponent is not None and exponent != 2:
            warnings.warn('Magnitude exponent is automatically set to 2 for a PowerSpectrum')
        super().__init__(magnitude, phase, nyquist_freq, exponent=2, **kwargs)


    @classmethod
    def from_timesignal(cls, input_signal, **kwargs):
        kwargs['exponent'] = 2
        return Spectrum.from_timesignal(input_signal, **kwargs)


class Spectrogram(SpectralMixin, TimeMixin, Signal):
    """A class representing a complex spectrogram.
    """
    def __init__(
        self, magnitude, phase, nyquist_freq, *,
        frame_duration=None, frame_size=None, step_duration=None, step_size=None, step_ratio=None,
        dB=True, min_freq=None, max_freq=None, num_bins=None, norm_single_side_band=False,
        spacing='linear', window='hann', exponent=1,
    ):
        self._frame_size, self._overlap_size = TimeMixin._parse_frame_params(frame_duration, frame_size,
            step_duration, step_size, step_ratio, 2 * nyquist_freq, spacing, min_freq)
        max_freq, self._num_bins, fft_size = SpectralMixin._check_freq_params(spacing, num_bins, max_freq, min_freq, nyquist_freq, self._frame_size, 'the given frame width')
        bin_units, bin_frequencies = SpectralMixin._bins_for_spacing(spacing, self._num_bins, min_freq, max_freq, nyquist_freq)
        super().__init__(magnitude, phase, nyquist_freq, bin_frequencies, bin_units, fft_size, dB, spacing, window, exponent, norm_single_side_band)
        # TimeMixin properties
        self.samplerate = 2 * nyquist_freq / (self._frame_size - self._overlap_size)
        self.times = np.arange(magnitude.shape[1]) / self.samplerate
        self._default_fig_args['height'] = 400
        self._default_fig_args['tooltips'] = [('time [s]', '@time{0.000}'), ('frequency [Hz]', '@frequency{0.000}'), ['magnitude', '@magnitude{0.000}']]
        self._default_fig_args['y_axis_label'] = self._bin_label
        if self.spacing in ('mel', 'log'):
            self._default_fig_args['tooltips'].insert(1, (self._bin_label, '@bin_unit{0.0}'))
        if self.exponent == 2 or self.dB:
            self._default_fig_args['tooltips'][-1][0] = 'power'
        if self.dB:
            self._default_fig_args['tooltips'][-1][0] += ' [dB]'


    @classmethod
    def from_timesignal(cls, input_signal, *,
        frame_duration=None, frame_size=None, step_duration=None, step_size=None, step_ratio=None,
        dB=True, min_freq=None, max_freq=None, num_bins=None, norm_single_side_band=False,
        spacing='linear', window='hann', exponent=1, samplerate=None,
    ):
        samples, samplerate = _get_samples_and_rate(input_signal, samplerate)
        nyquist_freq = samplerate / 2

        _frame_size, _overlap_size = TimeMixin._parse_frame_params(frame_duration, frame_size,
            step_duration, step_size, step_ratio, samplerate, spacing, min_freq)

        max_freq, num_bins, fft_size = cls._check_freq_params(spacing, num_bins, max_freq, min_freq, nyquist_freq, _frame_size, 'the given frame width')

        _, times, spectrogram = signal.stft(samples, fs=samplerate, window=window, nperseg=_frame_size, # CHECK if times == self.times
                                            noverlap=_overlap_size, nfft=fft_size, padded=False)
        magnitude, phase = cls._filter_and_scale(spectrogram, spacing, num_bins, min_freq, max_freq, nyquist_freq, fft_size, norm_single_side_band, dB, exponent)

        return cls(magnitude, phase,
            frame_size=_frame_size, step_size=_frame_size-_overlap_size, dB=dB, min_freq=min_freq,
            max_freq=max_freq, nyquist_freq=nyquist_freq, num_bins=num_bins,
            norm_single_side_band=norm_single_side_band, spacing=spacing, window=window, exponent=exponent,
        )


    def plot(self, fig=None, lowest_value=None, highest_value=None, palette=None, **plot_args):
        if not palette:
            palette = Viridis256
        if not lowest_value:
            lowest_value = np.min(self.magnitude)
        if not highest_value:
            highest_value = np.max(self.magnitude)

        if fig is None:
            fig_args = deepcopy(self._default_fig_args) # deepcopy is needed to avoid sharing tool instances between subsequent calls to plot
            fig_args.update({k: v for k, v in plot_args.items() if k in self._allowed_fig_args})
            if fig_args['tooltips'] is not None and self.magnitude.size > 2000000:
                fig_args['tooltips'] = None
                warnings.warn('Tooltips are automatically disabled when plotting large spectrograms for performance reasons. '
                            'Pass "tooltips=None" to silence this warning.')
            fig = figure(**fig_args)
        if isinstance(fig.x_range, DataRange1d):
            fig.x_range.range_padding = 0
        if isinstance(fig.y_range, DataRange1d):
            fig.y_range.range_padding = 0
        step_time = 1 / self.samplerate
        if [t for t in fig.tools if isinstance(t, InspectTool)]:
            all_times = np.broadcast_to(self.times, self.magnitude.shape)
            all_freqs = np.broadcast_to(self.frequencies.reshape(-1, 1), self.magnitude.shape)
            all_bin_units = np.broadcast_to(self._bin_units.reshape(-1, 1), self.magnitude.shape)
            delta_y = (self._bin_units[-1] - self._bin_units[0]) / (len(self._bin_units) - 1)
            data_source = ColumnDataSource({'magnitude': self.magnitude.reshape(-1, 1, 1).tolist(), 'time': all_times.ravel(), 'frequency': all_freqs.ravel(), 'bin_unit': all_bin_units.ravel()})
            color_indices = np.rint(np.interp(self.magnitude, (lowest_value, highest_value), (0, len(palette)-1))).astype(int)
            data_source.data['color'] = [palette[i] for i in color_indices.ravel()]
            rect_args = {k: v for k, v in plot_args.items() if k not in self._allowed_fig_args}
            fig.rect(x='time', y='bin_unit', width=step_time, height=delta_y, color='color', source=data_source, **rect_args)
        else:
            mapper = LinearColorMapper(palette=palette, low=lowest_value, high=highest_value)
            img_args = {k: v for k, v in plot_args.items() if k not in self._allowed_fig_args}
            fig.image([self.magnitude], x=self.times[0]-step_time/2, y=self._bin_units[0], dw=self.times[-1]+step_time, dh=self._bin_units[-1], color_mapper=mapper, **img_args)
        return fig


    def power(self, dB=True):
        if self.dB:
            power_per_freq = 10 ** (self.magnitude / 10)
        else:
            power_per_freq = self.magnitude ** (2/self.exponent)
        if self._norm_single_side_band:
            power = np.sum(power_per_freq, axis=0)
        elif self._fft_size % 2 == 0:
            power = power_per_freq[0] + 2*np.sum(power_per_freq[1:-1], axis=0) + power_per_freq[-1]
        else:
            power = power_per_freq[0] + 2*np.sum(power_per_freq[1:], axis=0)
        return TimeSignal(10*np.log10(np.maximum(power, 1e-12)) if dB else power, self.samplerate)


    def rms(self):
        return TimeSignal(np.sqrt(self.power(dB=False).data), self.samplerate)


    def spectrum_at(self, *, time=None, index=None):
        if (time is None and index is None) or (time is not None and index is not None):
            raise ValueError('Specify either the time or the index of the requested spectrum')
        if time is not None:
            index = np.argmin(np.abs(self.times - time))
        if self.spacing == 'linear':
            min_freq, max_freq = None, None
        else:
            min_freq, max_freq = self.frequencies[0], self.frequencies[-1]
        spectrum = Spectrum(self.magnitude[:, index], self.phase[:, index], self._input_samplerate/2, dB=self.dB, min_freq=min_freq, max_freq=max_freq, 
            num_bins=self._num_bins, norm_single_side_band=self._norm_single_side_band, spacing=self.spacing,
            window=self.window, exponent=self.exponent)
        spectrum._fft_size = self._fft_size
        spectrum.frequencies = self.frequencies
        return spectrum
