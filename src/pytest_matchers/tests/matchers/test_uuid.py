from uuid import NAMESPACE_DNS, uuid3, uuid4

from pytest_matchers import one_of
from pytest_matchers.matchers import UUID


def test_create():
    matcher = UUID()
    assert isinstance(matcher, UUID)
    matcher = UUID(version=4)
    assert isinstance(matcher, UUID)
    matcher = UUID(version=5)
    assert isinstance(matcher, UUID)
    matcher = UUID(version=9)
    assert isinstance(matcher, UUID)


def test_repr():
    matcher = UUID()
    assert repr(matcher) == "To be a UUID"
    matcher = UUID(str)
    assert repr(matcher) == "To be a UUID of 'str' instance"
    matcher = UUID(version=4)
    assert repr(matcher) == "To be a UUID with version equal to 4"
    matcher = UUID(version=9)
    assert repr(matcher) == "To be a UUID with version equal to 9"
    matcher = UUID(str, version=5)
    assert repr(matcher) == "To be a UUID of 'str' instance and with version equal to 5"
    matcher = UUID(str, version=one_of(3, 4))
    assert repr(matcher) == "To be a UUID of 'str' instance and with version 3 or 4"


def test_matches():
    valid_uuid_str = "550e8400-e29b-41d4-a716-446655440000"
    invalid_hex_uuid_str = "550e8400-e29b-41d4-a716-44665544000j"
    too_long_uuid = "550e8400-e29b-41d4-a716-4466554400000"
    valid_uuid_3 = uuid3(NAMESPACE_DNS, "python.org")
    matcher = UUID()
    assert matcher == valid_uuid_str
    assert matcher == str(uuid4())
    assert matcher == uuid4()
    assert matcher == valid_uuid_3
    assert matcher == str(valid_uuid_3)
    assert matcher != "not a UUID"
    assert matcher != invalid_hex_uuid_str
    assert matcher != too_long_uuid
    matcher = UUID(str)
    assert matcher == valid_uuid_str
    assert matcher == str(uuid4())
    assert matcher == str(valid_uuid_3)
    assert matcher != uuid4()
    assert matcher != valid_uuid_3
    matcher = UUID(version=4)
    assert matcher == valid_uuid_str
    assert matcher == str(uuid4())
    assert matcher == uuid4()
    assert matcher != valid_uuid_3
    matcher = UUID(str, version=3)
    assert matcher != valid_uuid_3
    assert matcher == str(valid_uuid_3)
    assert matcher != valid_uuid_str
