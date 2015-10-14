Lexor Language: HTML default style writer
=========================================

This style aims to have a balance between readability and a level of
compression. That is, many html have many useless white space
characters in them that in most cases do not help us read the content
of the file.

Here we separate important elements such as `div`, `p` and header
elements by one new line character and wrap the text after reaching a
certain width. For instance,

```html
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
```

gets written as follows under this style

```console
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
```

The space between `<h1>` and `First` is because the file had repeated
spaces between them which collapsed to only one. This extra space may
be important in some situations and thus it was written.


## Installation

For a local installation 

    $ lexor install html.writer.default

If there is a problem with the registry you may try a more direct
approach

    $ lexor install git+https://github.com/jmlopez-rod/html-writer-default

You may use the `-u` option to install in the python user-site
directory or `-g` for a global installation (requires sudo rights).

If you have a `lexor.config` file in place you may also want to use
the `--save` option so that the dependency gets saved.


## Options

There are currently three options which we can specify to have some
control over the output.

- `width`: The limit number of characters per line, defaults to 70.
- `add_block`: Specify a list of node names, separated by a comma so
               that they may be treated as blocks.
- `del_block`: You may disagree with some of the default blocks
               written by the author, here you can specify which
               node names to remove from the list.

To be able to specify the defaults when using a converter you can
do:

    $ lexor example.html to html[_:html._@width=80@add_block=[tag1,tag2]]

This statement says:

> lexor get the file `example.html` and convert it to html in the
> default style and write it in the html default style with a width
> set to 80 and treat elements of name tag1 and tag2 as blocks.
