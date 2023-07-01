class CustomQueue:
	
	def __init__(self, size):
		self.max_size = size
		self.queue = list()
	
	def push(self, value):
		if self.isFull():
			self.pop()
		self.queue.append(value)
	
	def pop(self):
		if len(self.queue) == 0:
			return None
		val = self.queue[0]
		self.queue.pop(0)
		return val

	def isEmpty(self):
		return len(self.queue) == 0

	def isFull(self):
		return len(self.queue) == self.max_size
		
	def flush(self):
		result = []
		for i in range(len(self.queue)):
			result.append(self.pop())
		return result