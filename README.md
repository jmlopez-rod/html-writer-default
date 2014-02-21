Lexor Language: HTML default style writer
=========================================

This style aims to have a balance between readability and a level of
compression. That is, many html have many useless white space
characters in them that in most cases do not help us read the content
of the file.

Here we separate important elements such as `div`, `p` and header
elements by one new line character and wrap the text after reaching a
certain width. For instance,

    <!doctype html>
    <html>
    <body>
        <h1>
            First Heading
        </h1>
        <p>
            First paragraph.
            <?python
    print 'This message was printed in python.'
    ?>
        </p>
    </body>
    </html>

gets written as follows under this style

    lexor example.html to html~_~ 
    <!DOCTYPE html>
    <html>
    <body>
    <h1> First Heading </h1>
    <p> First paragraph. <?python
    print 'This message was printed in python.'
    ?>
    </p>
    </body>
    </html>

The space between `<h1>` and `First` is because the file had repeated
spaces between them which collapsed to only one. This extra space may
be important in some situations and thus it was written.
