"""HTML: DEFAULT NodeWriters

Collection of NodeWriter objects to write an html without
indentations and breaks lines after the first word that goes beyond a
certain column number.

"""

import re
import textwrap
from lexor.core.writer import NodeWriter
import lexor.core.elements as core
RE = re.compile(r'\s+')
TW = textwrap.TextWrapper()
RAWTEXT = (
    'script', 'style', 'textarea', 'title'
)
BLOCK = [
    'html', 'address', 'article', 'aside', 'blockquote', 'dir',
    'div', 'dl', 'fieldset', 'footer', 'form', 'h1', 'h2', 'h3',
    'h4', 'h5', 'h6', 'header', 'hgroup', 'hr', 'main', 'menu',
    'nav', 'p', 'pre', 'section', 'table', 'ol', 'ul', 'li', 'link',
    '#doctype', 'head', 'body',
]
BLOCK.extend(RAWTEXT)


class TextNW(NodeWriter):
    """Writes text nodes with multiple spaces removed. """

    def data(self, node):
        if self.writer.pre_node:
            self.wrap(node.data, raw=True)
            return
        text = re.sub(RE, ' ', node.data)
        if text != ' ' or (node.index != 0 and
                           node.prev.name not in BLOCK and
                           node.next is not None and
                           node.next.name not in BLOCK):
            self.wrap(text)


class DefaultNW(NodeWriter):
    """Default way of writing HTML elements. """

    def start(self, node):
        if node.name == 'pre':
            self.writer.pre_node += 1
            if 'pre' in BLOCK:
                self.writer.endl(False)
        if self.writer.pre_node:
            raw = True
        else:
            raw = False
            if node.name in BLOCK:
                self.writer.endl(False)
        if isinstance(node, core.ProcessingInstruction):
            self.wrap('<%s' % node.name, split=True)
            if '\n' in node.data:
                self.wrap('\n', raw=raw)
            else:
                self.wrap(' ', raw=raw)
            return
        att = ' '.join(['%s="%s"' % (k, v) for k, v in node.items()])
        self.wrap('<%s' % node.name, split=True, raw=raw)
        if att != '':
            self.wrap(' %s' % att, raw=raw)
        if isinstance(node, core.Void):
            self.wrap('/>', raw=raw)
        else:
            self.wrap('>', raw=raw)

    def data(self, node):
        if (node.name in RAWTEXT or self.writer.pre_node or
                isinstance(node, core.ProcessingInstruction)):
            self.wrap(node.data, raw=True)
        else:
            text = re.sub(RE, ' ', node.data)
            self.wrap(text)

    def child(self, node):
        if self.writer.pre_node:
            return True
        for child in node.child:
            if child.name not in ['#text', '#entity']:
                return True
        for child in node.child:
            self.wrap(re.sub(RE, ' ', child.data))
        self.wrap('</%s>' % node.name)
        if node.name in BLOCK:
            self.wrap('\n')

    def end(self, node):
        if node.name == 'pre':
            self.writer.pre_node -= 1
        if self.writer.pre_node:
            raw = True
        else:
            raw = False
        if node.child is None:
            if isinstance(node, core.ProcessingInstruction):
                self.wrap('?>')
            elif isinstance(node, core.RawText):
                self.wrap('</%s>' % node.name)
            if not raw:
                self.writer.endl()
        else:
            self.wrap('</%s>' % node.name, raw=raw)
            if not raw and node.name in BLOCK:
                self.writer.endl(False)


class DoctypeNW(NodeWriter):
    """Writes the doctype node: `<!DOCTYPE ...>`. """

    def start(self, node):
        self.wrap('<!DOCTYPE ')

    def data(self, node):
        self.wrap(re.sub(RE, ' ', node.data).strip())

    def end(self, node):
        self.wrap('>\n', raw=True)


class CDataNW(NodeWriter):
    """Writes the CDATA node. """

    def start(self, node):
        self.wrap('<![CDATA[', split=True)

    def data(self, node):
        data = node.data.split(']]>')
        for index in xrange(len(data)-1):
            self.wrap(data[index] + ']]]]><![CDATA[>', raw=True)
        self.wrap(data[-1], raw=True)

    def end(self, node):
        self.wrap(']]>')


class CommentNW(NodeWriter):
    """Comment can also follow the tree structure. They have to be
    formatted to reflect this. """

    def start(self, node):
        if node.prev is not None:
            if node.prev.name == '#text':
                index = node.prev.data.rfind('\n')
                if index != -1:
                    line = node.prev.data[index+1:]
                    if line.strip() == '':
                        self.writer.endl(False)
        self.wrap('<!--', split=True)

    def data(self, node):
        self.wrap(node.data, raw=True)

    def end(self, node):
        self.wrap('-->')
        if node.next is not None:
            nnext = node.next
            if nnext.name == '#text' and nnext.data.startswith('\n'):
                self.writer.endl()


class DocumentNW(NodeWriter):
    """Finish document with a new line character. """

    def end(self, node):
        self.writer.endl(False)
