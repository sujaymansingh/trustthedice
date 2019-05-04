from io import StringIO
from datetime import date

from attr import attrs, attrib


from trustthedice import serialise


@attrs
class Person(serialise.Serialisable):
    # This is a classic example of something that can't be JSON serialised becase
    # of the date attribute.
    name: str = attrib()
    dob: date = attrib()

    def to_simple_list(self):
        return [self.name, self.dob.year, self.dob.month, self.dob.day]

    @classmethod
    def from_simple_list(self, simple_list):
        [name, year, month, day] = simple_list
        return Person(name=name, dob=date(year, month, day))


def test_serialise_and_back():
    my_file = StringIO()

    person_in = Person(name="Shahid Afridi", dob=date(1975, 3, 1))

    serialise.write(person_in, my_file)

    my_file.seek(0)
    person_out = serialise.read(my_file, Person)

    assert person_in == person_out
