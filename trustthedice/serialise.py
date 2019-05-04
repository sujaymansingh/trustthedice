import json


class Serialisable:
    def to_simple_list(self):
        """Return the object's attributes in a list that can JSON serialised.

        The only restriction of the format of the list to be returned is that
        if it is passed to from_simple_list, then we get something equivalent
        to the original object.
        """
        raise NotImplementedError()

    @classmethod
    def from_simple_list(cls, simple_list):
        """Return an instance of the ojbect using simple_list as its 'input'
        """
        raise NotImplementedError()


def write(serialisable_object, output_file):
    simple_list = serialisable_object.to_simple_list()
    json.dump(simple_list, output_file)
    output_file.write("\n")


def read(input_file, serialisable_class):
    line = next(input_file).strip()
    simple_list = json.loads(line)
    return serialisable_class.from_simple_list(simple_list)
