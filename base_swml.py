class BaseSWML:
    def to_dict(self):
        dict_representation = {key: value for key, value in self.__dict__.items() if value is not None}
        if not dict_representation:  # If dict is empty
            return self.__class__.__name__.lower()
        return dict_representation
