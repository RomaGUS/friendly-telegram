from core import utils
from core import spaces
import ffmpeg
import shutil
import os

class Hls():
	def __init__(self, path):
		# ToDo: add mime type check
		# ToDo: track upload progress
		self.tmp_dir = '/tmp/hikka-{}/'.format(utils.pebble())
		self.tmp_file = self.tmp_dir + '{}.mp4'.format(utils.pebble())
		self.tmp_hls_dir = self.tmp_dir + 'hls/'
		self.fs = spaces.init_fs()
		self.spaces_path = path

		if not os.path.exists(self.tmp_dir):
			os.makedirs(self.tmp_dir)

		if not os.path.exists(self.tmp_hls_dir):
			os.makedirs(self.tmp_hls_dir)

	def save(self, upload):
		# ToDo: Move to separate class
		with open(self.tmp_file, 'wb') as file:
			file.write(upload.read())

	def ffmpeg(self):
		input_stream = ffmpeg.input(self.tmp_file, f='mp4')
		output_stream = ffmpeg.output(input_stream, self.tmp_hls_dir + 'watch.m3u8', vcodec="copy", acodec="copy", format='hls', start_number=0, hls_time=10, hls_list_size=0)
		ffmpeg.run(output_stream)
		os.remove(self.tmp_file)

	def process(self):
		files = [f for f in os.listdir(self.tmp_hls_dir) if os.path.isfile(os.path.join(self.tmp_hls_dir, f))]

		for file in files:
			self.fs.put(self.tmp_hls_dir + file, self.spaces_path + file)
			self.fs.chmod(self.spaces_path + file, 'public-read')
			os.remove(self.tmp_hls_dir + file)

		shutil.rmtree(self.tmp_dir)
