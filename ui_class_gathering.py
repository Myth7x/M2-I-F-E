import inspect

# M2 CPython Modules
import ui

# credits to samalamabigcock
class UI_Classes:
	def is_class(self, class_attr):
		return hasattr(class_attr, "__init__")

	def is_function(self, attr):
		return hasattr(attr, "__code__")

	def concat_to_arg_string(self, data, attr_name=""):
		result = ""
		for var in data:
			if (attr_name != ""):
				result += "%s, " % (getattr(var, attr_name))
			else:
				result += "%s, " % (var)
		return result[:-2]

	def get_class_data(self, module, class_name):
		try:
			class_attr = getattr(module, class_name)
			if not self.is_class(class_attr):
				return
			attributes = {}
			for attribute_name in sorted(dir(class_attr)): #all attributes in class
				attr = getattr(class_attr, attribute_name)
				if not self.is_function(attr):
					continue
				arg_spec = inspect.getargspec(attr)
				args = arg_spec.args #all argument names
				defaults = arg_spec.defaults #all default values
				if defaults:
					for default_value in zip(args[-len(defaults):], defaults): #combine arguments and default values because they're not..
						arg_name = default_value[0] 
						if arg_name in args:
							args[args.index(arg_name)] = "%s=%s" % (arg_name, default_value[1]) #overwrite default arguments for found argument
				attributes[attribute_name] = self.concat_to_arg_string(args)
			class_bases = self.concat_to_arg_string(class_attr.__bases__, "__name__") # class MyClass(Base)
			return [class_name, class_attr, class_bases, attributes] #MyClass <MyClass.Class>, ['Base'], {'SetText' = 'self, text', ..} 
		except Exception:
			pass
		return {}

	def load_ui_data(self):
		classes = {}
		for attribute_name in sorted(dir(ui)):
			if hasattr(classes, attribute_name):
				classes[attribute_name] = self.get_class_data(ui, attribute_name)
		return classes
