class Locker:
    def __init__(self, id, width, height):
        self.id = id
        self.width = width
        self.height = height
        self.is_empty = True
        self.package_id = None

    def is_fit(self, package_width, package_height):
        return self.is_empty and self.width >= package_width and self.height >= package_height

    def set_empty(self, is_empty=True):
        self.is_empty = is_empty

    def get_empty(self):
        return self.is_empty
