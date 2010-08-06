import json

class NoSuchListError(Exception): pass

class TodoList:
	"""
	Contains the code needed to manage the todo list.
	"""
	def __init__(self, json_location):
		"""
		Sets up the list.
		"""
		self.json_location = json_location
		self.load()

	def add(self, text):
		"""
		Adds an item to the list
		"""
		try:
			last_id = self.list[-1].id
		except IndexError:
			# No items in list
			last_id = - 1 

		new_item = TodoItem(last_id + 1, text)
		self.list.append(new_item)
		return new_item

	def __str__(self):
		stringlist = []

		for item in self.list:
			stringlist.append(str(item.id) + '\t' + str(item.text))

		string = '\n'.join(stringlist)
		return string
			
	def idLessString(self):
		"""
		Returns a string of this list without the id numbers.
		"""
		string = ''
		for item in self.list:
			string = string + str(item.text) + '\n'
		string = string[:-1] # Cut out final newline
		return string

	def __len__(self):
		return len(self.list)

	def __iter__(self):
		return self.forward()

	def __getitem__(self, item_id):
		print item_id
		for todo in self.list:
			if todo.id == item_id:
				return todo
			else:
				print item_id, 'not matched for', todo.id, todo
		raise IndexError('No such item')

	def forward(self):
		current_item = 0
		while (current_item < len(self)):
			item = self.list[current_item]
			current_item += 1
			yield item

	def __contains__(self, item):
		if item in self.list:
			return True
		return False

	def remove(self, item_id):
		"""
		Removes an item from the list.
		"""
		todo = self[item_id]
		removed_text = todo.text
		self.list.remove(todo)
		return removed_text

	def load(self):
		"""
		Loads the list data from file.
		"""
		try:
			json_file = open(self.json_location, 'r')
			json_text = json_file.read()
			json_file.close()

			json_list = json.loads(json_text)
			
			self.list = []
			for item in json_list:
				self.list.append(TodoItem(item['id'], item['text']))
				print item

		except IOError:
			raise NoSuchListError

	def save(self):
		"""
		Writes the list data to file.
		"""
		json_file = open(self.json_location, 'w')
		
		json_list = []
		# Re-order indices
		id = 0 
		for item in self.list:
			item.id = id
			json_list.append(item.asdict())
			id += 1

		json_file.write(json.dumps(json_list))
		json_file.close()

class TodoItem:
	def __init__(self, id, text):
		self.id = id
		self.text = text

	def __str__(self):
		return self.text

	def asdict(self):
		return {'id': self.id, 'text': self.text }
