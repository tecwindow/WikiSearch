import threading
import ctypes


class my_threads(threading.Thread):
	def get_id(self):
		# returns id of the respective thread
		if hasattr(self, '_thread_id'):
			return self._thread_id
		for id, thread in threading._active.items():
			if thread is self:
				return id
  
	def stop(self):
		self._is_stopped = True
		self.thread_id = self.get_id()
		self.res = ctypes.pythonapi.PyThreadState_SetAsyncExc(self.thread_id, ctypes.py_object(SystemExit))
		if self.res > 1:
			ctypes.pythonapi.PyThreadState_SetAsyncExc(self.thread_id, 0)

	def is_stopped(self):
		return self._is_stopped


