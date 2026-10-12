from assistant.rules import reply


def test_greeting():
    assert "Hello" in reply("hi")


def test_office_lookup():
    assert "I.101" in reply("Where is the Training Office?")


def test_unknown():
    assert "don't know" in reply("what is the meaning of life")


def test_empty():
    assert reply("   ") == "Please type a question."

def test_faculty_of_it_office():
    result = reply("Where is the Faculty of IT Office?")
    assert "I.53" in result


def test_faculty_of_chemistry():
    result = reply("Where is the Faculty of Chemistry?")
    assert "I.59B" in result
