# pylint: disable=C0114, W0613, C0116, C0115


def test_article_creation(sample_article):
    assert sample_article.title == "Sample Article Title"
    assert sample_article.text == "This is the article text."
    assert sample_article.site == "example.com"


def test_save_article(temp_folder, sample_article):
    # Call the save method
    sample_article.save(temp_folder)

    # Check if the file was created
    expected_file_path = temp_folder / "example.com - Sample_Article_Title.txt"
    assert expected_file_path.exists()

    # Check the content of the saved file
    with open(expected_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        assert content == "This is the article text."


def test_save_article_with_special_characters(temp_folder, article_with_special_characters):
    article_with_special_characters.save(temp_folder)

    expected_file_path = temp_folder / "example.com - Special_Characters_Article.txt"
    assert expected_file_path.exists()
