import os

def test_main():
    # Run the main.py script
    os.system("python main.py")

    # Check if the new_test.txt file exists
    assert os.path.exists("new_test.txt")

    # Read the content of the new_test.txt file
    with open("new_test.txt", "r") as f:
        content = f.read()

    # Check if the content matches the expected output
    expected_content = """Abandon Ability Able
Abortion About Above
Abroad Absence Absolute
"""
    assert content.strip() == expected_content.strip()
    os.remove("new_test.txt")
