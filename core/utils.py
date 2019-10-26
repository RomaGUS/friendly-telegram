from core.spaces import Spaces
from core.errors import Errors
import ffmpeg
import shutil
import os

def pebble():
	"""Generate random 32 characters string"""
	return os.urandom(16).hex()

def check_fields(fields: list, data: dict):
	'''Check if given dict `data` contain given list of keys from list `fields`.'''
	for field in fields:
		if field not in data:
			return Errors.get('missing-field', '{} is not set'.format(field.title()))

	return None

class Hls():
	def __init__(self, path):
		# ToDo: add mime type check
		# ToDo: track upload progress
		# ToDo: clean up
		# ToDo: multiprocessing
		self.tmp_dir = '/tmp/hikka-{}/'.format(pebble())
		self.tmp_file = self.tmp_dir + '{}.mp4'.format(pebble())
		self.tmp_hls_dir = self.tmp_dir + 'hls/'
		self.spaces = Spaces()
		self.spaces_path = path

		if not os.path.exists(self.tmp_dir):
			os.makedirs(self.tmp_dir)

		if not os.path.exists(self.tmp_hls_dir):
			os.makedirs(self.tmp_hls_dir)

	def save(self, upload):
		with open(self.tmp_file, 'wb') as file:
			file.write(upload.read())

	def ffmpeg(self):
		input_stream = ffmpeg.input(self.tmp_file, f='mp4')
		output_stream = ffmpeg.output(input_stream, self.tmp_hls_dir + 'watch.m3u8', vcodec="copy", acodec="copy", format='hls', start_number=0, hls_time=10, hls_list_size=0)
		ffmpeg.run(output_stream)

	def process(self):
		files = [f for f in os.listdir(self.tmp_hls_dir) if os.path.isfile(os.path.join(self.tmp_hls_dir, f))]

		for file in files:
			self.spaces.upload_file(self.tmp_hls_dir + file, self.spaces_path + file)
			os.remove(self.tmp_hls_dir + file)

		shutil.rmtree(self.tmp_dir)

# def upload_hls(upload_file, spaces_path):
	# """Convert mp4 to hls and upload it to DigitalOcean spaces"""
	# tmp_dir = '/tmp/{}/'.format(pebble())
	# tmp_file = tmp_dir + '{}.mp4'.format(pebble())
	# tmp_hls_dir = tmp_dir + 'hls/'

	# ToDo: add mime type check
	# ToDo: track upload progress
	# ToDo: clean up
	# ToDo: convert this function in separate class
	# ToDo: multiprocessing

	# if not os.path.exists(tmp_dir):
		# os.makedirs(tmp_dir)

	# with open(tmp_file, 'wb') as file:
		# file.write(upload_file.read())

	# if not os.path.exists(tmp_hls_dir):
		# os.makedirs(tmp_hls_dir)

	# input_stream = ffmpeg.input(tmp_file, f='mp4')
	# output_stream = ffmpeg.output(input_stream, tmp_hls_dir + 'watch.m3u8', vcodec="copy", acodec="copy", format='hls', start_number=0, hls_time=10, hls_list_size=0)
	# ffmpeg.run(output_stream)

	# files = [f for f in os.listdir(tmp_hls_dir) if os.path.isfile(os.path.join(tmp_hls_dir, f))]
	# spaces = Spaces()

	# def upload(file):
	# 	spaces.upload_file(tmp_hls_dir + file, spaces_path + file)
	# 	os.remove(tmp_hls_dir + file)

	# with multiprocessing.Pool(8) as p:
		# p.map(upload, files)

	# shutil.rmtree(tmp_dir)

	# return True
