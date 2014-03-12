"""HTML: DEFAULT Writer Style

This style writes an html document without indentations. Writes a new
line character after the first word that goes beyond a given width
(70 by default).

"""

from lexor import init, load_aux

INFO = init(
    version=(0, 0, 1, 'final', 8),
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
    'add_block': '',
    'del_block': '',
}
MOD = load_aux(INFO)['nw']
MAPPING = {
    'script': MOD.ScriptNW,
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
    writer.disable_raw()
    writer.enable_wrap()
    writer.width = int(writer.defaults['width'])
    writer.pre_node = 0
    for name in writer.defaults['add_block'].split(','):
        if name and name not in MOD.BLOCK:
            MOD.BLOCK.append(name)
    for name in writer.defaults['del_block'].split(','):
        try:
            MOD.BLOCK.remove(name)
        except ValueError:
            pass
