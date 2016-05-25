import signal
import subprocess

class Shell(object):

	class CatchSigint:

		def	__init__(self, action):
			self.action = action

		def	__enter__(self):
			self.old = signal.signal(signal.SIGINT, self.handler)

		def	__exit__(self, type, value, traceback):
			self.new = signal.signal(signal.SIGINT, self.old)

		def	handler(self, sig, frame):
			print("\nOperation aborted\b")
			self.action._cmd.terminate()

	def __init__(self, cwd=None, out=subprocess.PIPE, err=subprocess.PIPE, background=False):
		super(Shell, self).__init__()
		self._cwd = cwd
		self._out = out
		self._err = err
		self._background = background

	def	terminate(self):
		self._cmd.terminate()

	def	poll(self):
		return self._cmd.poll()

	def	execute(self, args=None):
		if not args or not len(args) or type(args) != list:
			raise ShellError("Missing args")
		with self.CatchSigint(self):
			if not len(args):
				return
			cmd = "exec " + " ".join(args)
			self._cmd = subprocess.Popen(cmd, cwd=self._cwd, shell=True, stdout=self._out, stderr=self._err)
			if not self._background:
				self._cmd.wait()
				stdout = self._cmd.stdout.read()
				if self._cmd.returncode:
					raise ShellError("Code " + str(self._cmd.returncode))
				return stdout
			else:
				return self._cmd.communicate()

class ShellError(Exception):

	def __init__(self, value):
		self.value = "Shell Error : " + value

	def __str__(self):
		return repr(self.value)
