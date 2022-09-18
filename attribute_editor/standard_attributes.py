StandardAttributes = {
    "name": {
        'type': 'text',
        'default': 'unnamed',
        'description': 'Name of the object',
        'index': 1,
    },
    "type": {
        'type': 'text',
        'default': 'object',
        'description': 'Type of the object',
        'index': 2,
    },
    "x": {
        'type': 'slider',
        'default': 0.0,
        'description': 'X position of the object',
        'index': 3,
    },
    "y": {
        'type': 'slider',
        'default': 0.0,
        'description': 'Y position of the object',
        'index': 4,
    },
    "width": {
        'type': 'slider',
        'default': 0.0,
        'description': 'Width of the object',
        'index': 5,
    },
    "height": {
        'type': 'slider',
        'default': 0.0,
        'description': 'Height of the object',
        'index': 6,
    },
    "parent": {
        'type': 'text',
        'default': 'none',
        'description': 'Parent of the object',
        'index': 7,
    },
    
}

class Attribute:
    def __init__(self, name, type, index, value, description):
        self.name = name
        self.value = value
        self.index = index
        self.description = description
        self.type = type
        self.input_options = None
