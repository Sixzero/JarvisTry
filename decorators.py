
from functools import wraps
from threading import Thread

def run_in_thread(func):
	@wraps(func)
	def run(*args, **kwargs):
		t = Thread(target=func, args=args, kwargs=kwargs)
		t.setDaemon(True)
		t.start()
		return t

	return run