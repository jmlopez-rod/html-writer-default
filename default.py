"""HTML: DEFAULT Writer Style

This style writes an html document without indentations. Writes a new
line character after the first word that goes beyond a given width
(70 by default).

"""

from lexor import init, load_aux

INFO = init(
    version=(0, 0, 1, 'final', 1),
    lang='html',
    type='writer',
    description='Writes HTML files without indentation.',
    url='http://jmlopez-rod.github.io/lexor-lang/html-writer-default',
    author='Manuel Lopez',
    author_email='jmlopez.rod@gmail.com',
    license='BSD License',
    path=__file__
)
DEFAULTS = {
    'width': '70',
}
MOD = load_aux(INFO)['nw']
MAPPING = {
    '#document': MOD.DocumentNW,
    '#text': MOD.TextNW,
    '#entity': '#text',
    '#comment': MOD.CommentNW,
    '#doctype': MOD.DoctypeNW,
    '#cdata-section': MOD.CDataNW,
    '__default__': MOD.DefaultNW,
}


def pre_process(writer, _):
    """Sets the default width for the writer. """
    writer.width = int(writer.defaults['width'])
    writer.pre_node = False
