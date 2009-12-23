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
			last_id = self.list[-1]['id']
		except IndexError:
			# No items in list
			last_id = 0

		new_item = {'id': last_id + 1, 'text': text}
		self.list.append(new_item)

	def __str__(self):
		string = ""
		for item in self.list:
			string = string + str(item['id']) + "\t" + str(item['text']) + "\n"
		string = string[:-1] # Cut out final newline
		return string
			
	def __len__(self):
		return len(self.list)

	def remove(self, item_id):
		"""
		Removes an item from the list.
		"""
		for todo in self.list[:]:
			if todo['id'] == item_id:
				removed_text = todo['id']
				self.list.remove(todo)
				return removed_text

		return "Nothing"

	def load(self):
		"""
		Loads the list data from file.
		"""
		try:
			json_file = open(self.json_location, "r")
			json_text = json_file.read()
			json_file.close()

			self.list = json.loads(json_text)
		except IOError:
			raise NoSuchListError

	def save(self):
		"""
		Writes the list data to file.
		"""
		json_file = open(self.json_location, "w")
		json_file.write(json.dumps(self.list))
		json_file.close()
