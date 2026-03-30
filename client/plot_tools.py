import numpy as np
import matplotlib.pyplot as plt

class Matrix:
	def __init__(self,npz_dir,npz_file):
		self.npz_dir = npz_dir
		self.npz_file = npz_file

	def _load_data(self):
		self.npz_path = self.npz_dir + "/" + self.npz_file + ".npz"
		_data = np.load(file=self.npz_path)
		self.full_audio = _data['audio_matrix']
		num_samples = len(self.full_audio)
		print("num_samples: ", num_samples)

		# generate clock data from sample rate (e.g. 44,100 Hz) and duration
		self.sample_rate = _data['sample_rate']
		print("sample_rate: ", self.sample_rate, " Hz")
		self.duration = _data['audio_duration']
		print("duration: ", self.duration, " seconds")
		self.clock = np.linspace(start=0,stop=self.duration,num=num_samples)

	def plot_data(self):
		self._load_data()
		fig, (_axis_full) = plt.subplots(nrows=1, ncols=1)
		_axis_full.plot(self.clock, self.full_audio)
		_axis_full.set_title('Full Audio')
		_axis_full.set_xlabel("Elapsed Time (s)")
		_axis_full.set_ylabel("Signal Amplitude")
		_axis_full.set_title(self.npz_file)
		plt.show()

#load matrices from 'storage' directory
storage_dir = '/media/ubuntu01/AudioTimeStamp-Detective/storage'
#test_file = 'test'
test_file = 'full/1997-04-02 (Guest - no guest)'
test_matrix = Matrix(storage_dir,test_file)
test_matrix.plot_data()
