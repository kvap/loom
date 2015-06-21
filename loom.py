import threading

# sequence of calls in one thread
class Spindle(object):
	def __init__(self):
		self.calls = []

	def __enter__(self):
		return self

	def __exit__(self, typ, value, traceback):
		pass

	def __call__(self, target, *args, **kwargs):
		self.calls.append((target, args, kwargs))

	def unwind(self):
		for target, args, kwargs in self.calls:
			target(*args, **kwargs)

# thread joining context manager
class Loom(object):
	def __init__(self, parallel=False):
		self.parallel = parallel
		self.spindles = []

	def __enter__(self):
		return self

	def __exit__(self, typ, value, traceback):
		threads = []
		for s in self.spindles:
			threads.append(threading.Thread(target=s.unwind))

		if self.parallel:
			for t in threads:
				t.start()
			for t in threads:
				t.join()
		else:
			for t in threads:
				t.start()
				t.join()

	def __call__(self, target, *args, **kwargs):
		if not hasattr(target, '__call__'):
			raise Exception("the first argument %s is not callable" % str(target))

		self.spindle()(target, *args, **kwargs)

	def spindle(self):
		s = Spindle()
		self.spindles.append(s)
		return s
