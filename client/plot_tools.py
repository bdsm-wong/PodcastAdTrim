import numpy as np
import matplotlib.pyplot as plt

class Matrix:
	def __init__(self,storage_dir, full_name, frag_name):
		self._storage_dir = storage_dir
		self._full_name = full_name
		self._frag_name = frag_name

	def _load_data(self):
		# Build file paths
		_full_path = self._storage_dir + "/full/" + self._full_name + ".npz"
		_frag_path = self._storage_dir + "/frag/" + self._frag_name + ".npz"
		_corr_path = self._storage_dir + "/corr/" + self._full_name + "/" + self._frag_name + ".npz"

		# Load full matrix data
		_full_data = np.load(file=_full_path)
		self._full_audio = _full_data['audio_matrix']
		_full_num_samples = len(self._full_audio)
		print(f"full audio: {str(_full_num_samples)} samples")
		_sample_rate = _full_data['sample_rate']
		print(f"sample_rate: {str(_sample_rate)} Hz")

		# Generate clock signal
		_full_duration = _full_data['audio_duration']
		print(f"full_duration: {str(_full_duration)} seconds")
		self.clock = np.linspace(start=0, stop=_full_duration, num=_full_num_samples)

		# Load and pad correlation data
		_corr_data = np.load(file=_corr_path)
		_corr_raw = _corr_data['corr_matrix']
		_corr_num_samples = len(_corr_raw)
		_corr_rPad_len = _full_num_samples - _corr_num_samples
		self._corr_padded = np.pad(
			array=_corr_raw,
			pad_width=(0, _corr_rPad_len),
			mode='constant',
			constant_values=(0, 0)
		)
		self._exact_second = _corr_data['exact_second']
		print("exact_second: ", self._exact_second)

		# Load and shift fragment matrix data
		_frag_data = np.load(file=_frag_path)
		_frag_raw = _frag_data['audio_matrix']
		_frag_num_samples = len(_frag_raw)
		_frag_lPad_len = int(self._exact_second * _sample_rate)
		_frag_rPad_len = _full_num_samples - _frag_num_samples - _frag_lPad_len
		self._frag_aligned = np.pad(
			array=_frag_raw,
			pad_width=(_frag_lPad_len, _frag_rPad_len),
			mode='constant',
			constant_values=(0, 0)
		)


	def plot_data(self):
		# Load data and set up chart
		self._load_data()

		fig, (_ax_corr) = plt.subplots(nrows=1, ncols=1)
		#fig, (_ax_full, _ax_corr, _ax_frag) = plt.subplots(nrows=3, ncols=1)

		'''
		# Plot full audio matrix
		_ax_full.plot(self.clock, self._full_audio)
		_ax_full.set_title(f"Full Audio: {self._full_name}")
		_ax_full.set_xlabel("Elapsed Time (s)")
		_ax_full.set_ylabel("Signal Amplitude")
		'''

		# Plot correlation data
		_ax_corr.plot(self.clock, self._corr_padded)
		_ax_corr.set_title("Correlation Matrix")
		_ax_corr.set_xlabel("Elapsed Time (s)")
		_ax_corr.set_ylabel("Correlation Strength")
		_window_width = 100000000
		#_ax_corr.set(xlim=(self._exact_second - (_window_width/2), self._exact_second + (_window_width/2)))

		'''
		# Plot fragment matrix
		_ax_frag.plot(self.clock, self._frag_aligned)
		_ax_frag.set_title(f"Fragment Audio: {self._frag_name}")
		_ax_frag.set_xlabel("Elapsed Time (s)")
		_ax_frag.set_ylabel("Signal Amplitude")
		'''

		plt.show()

#load matrices from 'storage' directory
_storage_dir = '/home/jeremy/Desktop/storage'
#test_file = 'test'
_full_name = '1997-04-02 (Guest - no guest)'
_frag_name = 'Podcast_One_Intro'
debug_matrix = Matrix(storage_dir=_storage_dir, full_name=_full_name, frag_name=_frag_name)
debug_matrix.plot_data()
