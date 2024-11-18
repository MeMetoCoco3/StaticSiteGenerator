from conversion import html_nodes_finito, markdown_to_html_node
import unittest


class Test_conersion(unittest.TestCase):
    def test_markdown_to_html_node(self):
        n1 = """# This is a Header 1

        ## This is a Header 2

        ### This is a Header 3

        #### This is a Header 4

        ##### This is a Header 5

        ###### This is a Header 6

        This is a normal paragraph with **bold** and *italic* text.

        Here is a code snippet inline: `print("Hello, World!")`.

        Below is a code block:

        ```
        package main
        import "fmt"
        fmt.Println("Lets gooo!!")
        ```
        

        Here is a link: [OpenAI](https://www.openai.com).

        Here is an image: ![OpenAI Logo](https://via.placeholder.com/150)

        > This is a blockquote.  
        > It can span multiple lines.

        Unordered List:

        - Item 1
        - Item 2

        """
        r1 = """<div><h1>This is a Header 1</h1>
<h2>This is a Header 2</h2>
<h3>This is a Header 3</h3>
<h4>This is a Header 4</h4>
<h5>This is a Header 5</h5>
<h6>This is a Header 6</h6>
<p>This is a normal paragraph with <b>bold</b> and <i>italic</i> text.</p>
<p>Here is a code snippet inline: <code>print("Hello, World!")</code>.</p>
<p>Below is a code block:</p>
<pre><code>package main
import "fmt"
fmt.Println("Lets gooo!!")</code></pre>
<p>Here is a link: <a href="https://www.openai.com">OpenAI</a>.</p>
<p>Here is an image: <img src="https://via.placeholder.com/150" alt="OpenAI Logo"></p>
<blockquote><p>This is a blockquote.
It can span multiple lines.</p></blockquote>
<p>Unordered List:</p>
<ul><li> Item 1</li>
<li> Item 2</li></ul></div>"""
        a1 = html_nodes_finito(markdown_to_html_node(n1))
        self.assertEqual(r1, a1)
