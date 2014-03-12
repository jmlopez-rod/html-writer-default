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
    '#doctype', 'head', 'body', 'table',
]
BLOCK.extend(RAWTEXT)


class TextNW(NodeWriter):
    """Writes text nodes with multiple spaces removed. """

    def data(self, node):
        if self.writer.pre_node:
            self.write(node.data)
            return
        text = re.sub(RE, ' ', node.data)
        if text != ' ':
            self.write(text)
        else:
            char = self.writer.last()[-1]
            if char not in ' \n' and (node.index != 0 and
                                      node.prev.name not in BLOCK and
                                      node.next is not None and
                                      node.next.name not in BLOCK):
                self.write(text)


class DefaultNW(NodeWriter):
    """Default way of writing HTML elements. """

    def start(self, node):
        if node.name == 'pre':
            self.writer.pre_node += 1
            self.writer.enable_raw()
            if 'pre' in BLOCK:
                self.writer.endl(False)
        if not self.writer.pre_node and node.name in BLOCK:
            self.writer.endl(False)
        if isinstance(node, core.ProcessingInstruction):
            self.write('<%s' % node.name, split=True)
            if '\n' in node.data:
                self.write('\n')
            else:
                self.write(' ')
            return
        att = ' '.join(['%s="%s"' % (k, v) for k, v in node.items()])
        self.write('<%s' % node.name)
        if att != '':
            self.write(' %s' % att)
        if isinstance(node, core.Void):
            self.write('/>')
        else:
            self.write('>')

    def data(self, node):
        if (node.name in RAWTEXT or
                isinstance(node, core.ProcessingInstruction)):
            enabled = self.writer.raw_enabled()
            if not enabled:
                self.writer.enable_raw()
            self.write(node.data)
            if not enabled:
                self.writer.disable_raw()
        else:
            text = re.sub(RE, ' ', node.data)
            self.write(text)

    def child(self, node):
        if self.writer.pre_node:
            return True
        for child in node.child:
            if child.name not in ['#text', '#entity']:
                return True
        data = ''.join([child.data for child in node.child])
        self.write(re.sub(RE, ' ', data))
        if not isinstance(node, core.Void):
            self.write('</%s>' % node.name)
        if node.name in BLOCK:
            self.writer.endl(False)

    def end(self, node):
        if node.name == 'pre':
            self.writer.pre_node -= 1
            if self.writer.pre_node == 0:
                self.writer.disable_raw()
        raw = self.writer.pre_node
        if node.child is None:
            if isinstance(node, core.ProcessingInstruction):
                self.write('?>')
            elif isinstance(node, core.RawText):
                self.write('</%s>' % node.name)
            if not raw and node.name not in ['img']:
                self.writer.endl(False)
        else:
            self.write('</%s>' % node.name)
            if not raw and node.name in BLOCK:
                self.writer.endl(False)


class DoctypeNW(NodeWriter):
    """Writes the doctype node: `<!DOCTYPE ...>`. """

    def start(self, node):
        self.write('<!DOCTYPE ')

    def data(self, node):
        self.write(re.sub(RE, ' ', node.data).strip())

    def end(self, node):
        self.write('>\n')


class CDataNW(NodeWriter):
    """Writes the CDATA node. """

    def start(self, node):
        self.write('<![CDATA[', split=True)

    def data(self, node):
        enabled = self.writer.raw_enabled()
        if not enabled:
            self.writer.enable_raw()
        data = node.data.split(']]>')
        for index in xrange(len(data)-1):
            self.write(data[index] + ']]]]><![CDATA[>')
        self.write(data[-1])
        if not enabled:
            self.writer.disable_raw()

    def end(self, node):
        self.write(']]>')


class CommentNW(NodeWriter):
    """Comment can also follow the tree structure. They have to be
    formatted to reflect this. """
    raw_enabled = None

    def start(self, node):
        if node.prev is not None:
            if node.prev.name == '#text':
                index = node.prev.data.rfind('\n')
                if index != -1:
                    line = node.prev.data[index+1:]
                    if line.strip() == '':
                        self.writer.endl(False)
        self.raw_enabled = self.writer.raw_enabled()
        if not self.raw_enabled:
            self.writer.enable_raw()
        self.write('<!--')

    def end(self, node):
        self.write('-->')
        if not self.raw_enabled:
            self.writer.disable_raw()
        if node.next is not None:
            nnext = node.next
            if nnext.name == '#text' and nnext.data.startswith('\n'):
                self.writer.endl()


class DocumentNW(NodeWriter):
    """Finish document with a new line character. """

    def end(self, node):
        self.writer.endl(False)


class ScriptNW(NodeWriter):
    """Handles some special types of scripts. """

    def start(self, node):
        if 'math/tex' in node['type']:
            self.write('<%s' % node.name)
            att = ' '.join(['%s="%s"' % (k, v) for k, v in node.items()])
            if att != '':
                self.write(' %s' % att)
            self.write('>')
        else:
            self.writer['__default__'].start(node)

    def data(self, node):
        self.writer['__default__'].data(node)

    def end(self, node):
        if 'math/tex' in node['type']:
            self.write('</%s>' % node.name)
        else:
            self.writer['__default__'].end(node)
