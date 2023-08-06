import aifc
from pathlib import Path
import numpy as np
from scipy import signal
from miniaudio import convert_frames, decode_file, get_file_info, DecodeError, SampleFormat


__all__ = ['envelope', 'read_audio_file', 'resample']


def envelope(samples, *, method='analytical', param=1):
    if method == 'analytical':
        dc_offset = np.mean(samples)
        dc_removed = samples - dc_offset
        if param > 1:
            dc_removed = signal.decimate(dc_removed, param)
        envelope = np.abs(signal.hilbert(dc_removed)) + dc_offset
        return np.repeat(envelope, param)
    elif method == 'smoothing':
        if param % 2 == 0:
            param += 1
        return signal.medfilt(np.abs(samples), param)
    else:
        raise ValueError(f'Unknown envelope calculation method "{method}"')


def read_audio_file(file_path: Path | str):
    file_path = str(file_path)
    try:
        file_info = get_file_info(file_path)
        if samplerate is None:
            samplerate = file_info.sample_rate
        decoded_file = decode_file(filename=file_path, output_format=SampleFormat.FLOAT32,
                                    nchannels=1, sample_rate=samplerate)
        samples = np.asarray(decoded_file.samples)
    except DecodeError as decode_error:
        try:
            samples, file_samplerate = _read_aiff_file(file_path, mix_to_mono=True)
            if samplerate is None:
                samplerate = file_samplerate
            elif samplerate != file_samplerate:
                samples = resample(samples, file_samplerate, samplerate)
        except:
            raise decode_error
    return samples


def _read_aiff_file(file_path: Path | str, mix_to_mono: bool = False):
    with aifc.open(file_path) as f:
        width = f.getsampwidth()
        num_chan = f.getnchannels()
        samplerate = f.getframerate()
        byteorder = 'little' if f.getcomptype().decode() == 'sowt' else 'big'
        samples_byte = f.readframes(f.getnframes())
    samples_int = [int.from_bytes(samples_byte[idx:idx+width], byteorder, signed=True)
                   for idx in range(0, len(samples_byte), width)]
    samples = np.asarray(samples_int) / 2**(8*width-1)
    if num_chan > 1:
        samples = samples.reshape(-1, num_chan)
        if mix_to_mono:
            samples = np.mean(samples, axis=1)
    return samples, samplerate


def resample(samples, current_samplerate, new_samplerate):
    resampled_samples = np.frombuffer(convert_frames(
        SampleFormat.FLOAT32, 1, current_samplerate, samples.astype(np.float32).tobytes(),
        SampleFormat.FLOAT32, 1, new_samplerate
    ), dtype=np.float32)
    return np.clip(resampled_samples, -1, 1)
