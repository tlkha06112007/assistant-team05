from assistant.rules import reply


def test_greeting():
    assert "Hello" in reply("hi")


def test_office_lookup():
    assert "I.101" in reply("Where is the Training Office?")


def test_unknown():
    assert "don't know" in reply("what is the meaning of life")


def test_empty():
    assert reply("   ") == "Please type a question."

def test_help():
    # Kiểm tra xem câu trả lời của lệnh help có chứa từ khóa tính năng (ví dụ: office) hay không
    assert "office" in reply("help").lower()