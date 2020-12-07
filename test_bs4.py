import unittest
import bs4


class TestBeautifulSoup(unittest.TestCase):
    def setUp(self):
        self.html_doc = """
        <html><head><title>The Dormouse's story</title></head>
        <body>
        <p class="title"><b>The Dormouse's story</b></p>
        <p class="story">Once upon a time there were three little sisters; and 
        their names were
        <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
        <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
        <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
        and they lived at the bottom of a well.</p>
        <p class="story">...</p>
        """
        self.soup = bs4.BeautifulSoup(self.html_doc, 'html.parser')

        self.html_doc_2 = """
        <html><head><title>Page Title</title></head>
        <body>
        <h1>My First Heading</h1>
        <p>My first paragraph</p>
        </body>
        </html>
        """
        self.soup_2 = bs4.BeautifulSoup(self.html_doc_2, 'html.parser')

        '''PageElement.wrap() wraps an element in the tag you specify. It 
        returns the new wrapper:'''

    def test_wrap(self):
        # Wrap string within two tags
        self.soup.head.string.wrap(self.soup.new_tag("b"))
        self.assertEqual(str(self.soup.head), "<head><title><b>The Dormouse's "
                                              "story</b></title></head>")
        # Wrap string within one tag
        self.soup = bs4.BeautifulSoup("<p>I wish I was bold.</p>",
                                      'html.parser')
        self.soup.p.string.wrap(self.soup.new_tag("b"))
        self.assertEqual(str(self.soup.p), "<p><b>I wish I was bold.</b></p>")

        # Wrap outside of two tags
        self.soup.p.wrap(self.soup.new_tag("div"))
        self.assertEqual(str(self.soup), "<div><p><b>I wish I was "
                                         "bold.</b></p></div>")

        # Wrap outside of one tag
        self.soup = bs4.BeautifulSoup("<p>I wish I had a div</p>",
                                      'html.parser')
        self.soup.p.wrap(self.soup.new_tag("div"))
        self.assertEqual(str(self.soup), "<div><p>I wish I "
                                         "had a div</p></div>")

        '''Tag.unwrap() is the opposite of wrap(). It replaces a tag with 
        whatever’s inside that tag. It’s good for stripping out markup.'''

    def test_unwrap(self):
        # Unwrap tag within two tags
        self.soup = bs4.BeautifulSoup("<head><title><b>The Dormouse's "
                                      "story</b></title></head>")
        self.soup.head.b.unwrap()
        self.assertEqual(str(self.soup), "<head><title>The Dormouse's "
                                         "story</title></head>")

        # Wrap string within one tag
        self.soup = bs4.BeautifulSoup("<p><b>I don't want to be bold</b></p>",
                                      'html.parser')
        self.soup.b.unwrap()
        self.assertEqual(str(self.soup), "<p>I don't want to be bold</p>")

        # Unwrap outside of one tag
        self.soup = bs4.BeautifulSoup("<div><p>I don't want to be a "
                                      "div</p></div>",
                                      'html.parser')
        self.soup.div.unwrap()
        self.assertEqual(str(self.soup), "<p>I don't want to be a div</p>")

        # Unwrap outside of two tags
        self.soup = bs4.BeautifulSoup("<div><p><b>I don't want "
                                      "to be a div</b></p></div>",
                                      'html.parser')
        self.soup.div.unwrap()
        self.assertEqual(str(self.soup), "<p><b>I don't want to be a "
                                         "div</b></p>")

        '''
        BeautifulSoup.string
        Convenience property to get the single string within this tag.
        Return:	If this tag has a single string child, return value is that 
        string. If this tag has no children, or more than one child, return 
        value is None. If this tag has one child tag, return value is the 
        ‘string’ attribute of the child tag, recursively.
        '''

    def test_string(self):
        # One child tag <head><title>The Dormouse's story</title></head>
        self.head_tag = self.soup.head
        self.assertEqual(self.head_tag.string, "The Dormouse's story")

        # One child tag <head><title>Page Title</title></head>
        self.head_tag_2 = self.soup_2.head
        self.assertEqual(self.head_tag_2.string, "Page Title")

        # Single string child <title>The Dormouse's story</title>
        self.title_tag = self.head_tag.contents[0]
        self.assertEqual(self.title_tag.string, "The Dormouse's story")

        # Single string child <title>Page Title</title>
        self.title_tag_2 = self.head_tag_2.contents[0]
        self.assertEqual(self.title_tag_2.string, "Page Title")

        # More than one child <html>...<head>...<title>...
        self.assertEqual(self.soup.html.string, None)

        # More than one child <html>...<head>...<title>...
        self.assertEqual(self.soup_2.html.string, None)

        # No children
        self.html_empty = """<html></html>"""
        self.soup_empty = bs4.BeautifulSoup(self.html_empty, 'html.parser')
        self.assertEqual(self.soup_empty.html.string, None)

        # No children
        self.html_empty_2 = """<html><body></body></html>"""
        self.soup_empty_2 = bs4.BeautifulSoup(self.html_empty_2, 'html.parser')
        self.assertEqual(self.soup_empty_2.html.string, None)

        '''
        PageElement.replace_with() removes a tag or string from the tree, 
        and replaces it with the tag or string of your choice.
        '''

    def test_string_replace_with_strings(self):
        # Replace a string within a b-tag
        # <b>The Dormouse's story</b>
        self.b_tag = self.soup.b
        self.assertEqual(self.b_tag.string, "The Dormouse's story")
        self.b_tag.string.replace_with("Someone else's story")
        self.assertEqual(self.soup.b.string, "Someone else's story")

        # Replace a string withing a title-tag
        # <title>The Dormouse's story</title>
        self.title_tag = self.soup.title
        self.assertEqual(self.title_tag.string, "The Dormouse's story")
        self.title_tag.string.replace_with("Someone else's story")
        self.assertEqual(self.soup.title.string, "Someone else's story")

        # Replace a string withing an h1-tag
        # <h1>My First Heading</h1>
        self.h1_tag = self.soup_2.h1
        self.assertEqual(self.h1_tag.string, "My First Heading")
        self.h1_tag.string.replace_with("Another Heading")
        self.assertEqual(self.soup_2.h1.string, "Another Heading")

        # Replace a string withing a p-tag
        # <p>My first paragraph</p>
        self.p_tag = self.soup_2.p
        self.assertEqual(self.p_tag.string, "My first paragraph")
        self.p_tag.string.replace_with("Another paragraph")
        self.assertEqual(self.soup_2.p.string, "Another paragraph")

        '''
        PageElement.replace_with() removes a tag or string from the tree, 
        and replaces it with the tag or string of your choice.
        '''

    def test_string_replace_with_tags(self):
        # Replace the inner tag within another tag
        # <p class="title"><b>The Dormouse's story</b></p>
        # Replace b-tag with i-tag
        self.p_tag = self.soup.p
        self.assertEqual(self.p_tag.string, "The Dormouse's story")
        self.new_tag = self.soup.new_tag("i")
        self.new_tag.string = "The Dormouse's story in Italic"
        self.p_tag.b.replace_with(self.new_tag)
        self.assertEqual(str(self.p_tag.i), "<i>The Dormouse's story in "
                                            "Italic</i>")

        # Replace the inner tag within two other tags
        self.html_tag = self.soup_2.html
        self.new_tag = self.soup.new_tag("h2")
        self.new_tag.string = "My Second Heading"
        self.html_tag.h1.replace_with(self.new_tag)
        self.assertEqual(str(self.html_tag.h2), "<h2>My Second Heading</h2>")

        # Replace a single i-tag with a b-tag
        # <i>I want to be bold</i>
        self.soup = bs4.BeautifulSoup("<i>I want to be bold</i>", 'html.parser')
        self.assertEqual(self.soup.string, "I want to be bold")
        self.new_tag = self.soup.new_tag("b")
        self.new_tag.string = "I became Bold"
        self.soup.i.replace_with(self.new_tag)
        self.assertEqual(str(self.soup), "<b>I became Bold</b>")

        # Replacing a tag with the same tag
        self.new_tag = self.soup.new_tag("b")
        self.new_tag.string = "I became Bold again"
        self.soup.b.replace_with(self.new_tag)
        self.assertEqual(str(self.soup), "<b>I became Bold again</b>")


if __name__ == '__main__':
    unittest.main()
