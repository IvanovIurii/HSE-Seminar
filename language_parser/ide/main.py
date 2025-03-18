import sys

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QRegExp
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QAction

from language_parser.interpreter.interpreter import Interpreter
from language_parser.syntax_tree.syntax_tree import parse
from language_parser.tokenizer import Tokenizer
from language_parser.common.consts import (
    NUMBER,
    IDENTIFIER,
    NEWLINE,
    PLUS,
    MINUS,
    MULT,
    DIV,
    EQ,
    LP,
    RP,
    ASSIGN,
    OUT,
    FUNC,
    BRANCH,
    IN,
    romans
)

# todo: keep only those what are in use
STYLES = {
    NUMBER: "blue",
    IDENTIFIER: "green",
    NEWLINE: "black",
    PLUS: "orange",
    MINUS: "orange",
    MULT: "orange",
    DIV: "orange",
    EQ: "purple",
    LP: "green",
    RP: "green",
    ASSIGN: "red",
    OUT: "red",
    FUNC: "red",
    BRANCH: "red",
    IN: "red"
}


class MyHighlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, output, document):
        self.context = {}
        self.output = output

        super().__init__(document)

    def highlightBlock(self, text):
        try:
            tokens = Tokenizer.tokenize(text + " ")  # hack: to color the last char in the block
        except Exception as e:
            print(e)
            self.output.appendPlainText(str(e))
            return

        for idx, token in enumerate(tokens):
            if token.value == "Munus":
                if len(tokens) > 1 and tokens[idx + 1].key == IDENTIFIER:
                    self.context['FUNC'] = tokens[idx + 1].value

        for token in tokens:
            expression = QRegExp(token.value)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                fmt = self.get_format_for_token(token)
                self.setFormat(index, length, fmt)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

    def get_format_for_token(self, token):
        fmt = QtGui.QTextCharFormat()
        token_key = token.key

        color = "black"
        if self.is_roman(token.value):
            color = STYLES.get(NUMBER, color)
            fmt.setForeground(QtGui.QColor(color))
            return fmt

        else:
            if token_key == IDENTIFIER and 'FUNC' in self.context and self.context['FUNC'] == token.value:
                color = "pink"
                fmt.setForeground(QtGui.QColor(color))
                return fmt

            # very ugly hack
            if token_key == NUMBER:
                color = "black"
            else:
                color = STYLES.get(token_key, color)

            fmt.setForeground(QtGui.QColor(color))
            return fmt

    def is_roman(self, text):
        return text.isupper() and all([char in romans.keys() for char in text])


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mini-IDE with highlight")

        layout = QVBoxLayout()

        self.editor = QtWidgets.QPlainTextEdit()
        font = QtGui.QFont("Consolas", 12)
        self.editor.setFont(font)

        layout.addWidget(self.editor)

        toolbar = QtWidgets.QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        button_action = QAction("RUN CODE", self)
        button_action.triggered.connect(self.run_code)
        toolbar.addAction(button_action)

        self.output = QtWidgets.QPlainTextEdit()
        self.output.setReadOnly(True)
        self.output.setFont(QtGui.QFont("Consolas", 12))
        layout.addWidget(self.output)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.highlighter = MyHighlighter(self.output, self.editor.document())

    def run_code(self):
        text = self.editor.toPlainText()
        # hack: new line to correctly parse AST
        text += "\n"

        tokens = Tokenizer.tokenize(text)

        try:
            ast_root = parse(tokens)

            if len(ast_root.children) == 0:
                print("Nothing to evaluate")

            self.find_input_and_replace(ast_root)

            interpreter = Interpreter()
            evaluated = interpreter.interpret(ast_root)

            self.output.appendPlainText(str(evaluated))

        except Exception as e:
            print(f"Something went wrong: {e}")
            self.output.appendPlainText(str(e))

    def find_input_and_replace(self, node):
        if node.type == IN:
            dialog = InputDialog()
            user_input = dialog.get_text()

            node.type = NUMBER
            node.value = user_input

            return True

        for child in node.children:
            if child:
                self.find_input_and_replace(child)


class InputDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Enter Roman Number")

        layout = QtWidgets.QVBoxLayout(self)
        self.text_edit = QtWidgets.QPlainTextEdit(self)
        layout.addWidget(self.text_edit)

        button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, self)
        layout.addWidget(button_box)

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

    def get_text(self):
        if self.exec_() == QtWidgets.QDialog.Accepted:
            return self.text_edit.toPlainText()

        return None


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.resize(600, 400)
    window.show()

    sys.exit(app.exec_())
