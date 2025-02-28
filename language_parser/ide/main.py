import sys

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QRegExp
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QAction

from language_parser.interpreter import Interpreter
from language_parser.syntax_tree.syntax_tree import parse
from language_parser.tokenizer import Tokenizer
from language_parser.tokenizer.consts import (
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
    IN
)

STYLES = {
    NUMBER: "blue",
    IDENTIFIER: "black",
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
    def __init__(self, document):
        super().__init__(document)

    def highlightBlock(self, text):
        tokens = Tokenizer.tokenize(text)

        for token in tokens:
            expression = QRegExp(token.value)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                fmt = self.get_format_for_token(token)
                self.setFormat(index, length, fmt)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

    @staticmethod
    def get_format_for_token(token):
        fmt = QtGui.QTextCharFormat()
        color = STYLES.get(token.key, "black")
        fmt.setForeground(QtGui.QColor(color))
        return fmt


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

        self.highlighter = MyHighlighter(self.editor.document())

    def run_code(self):
        text = self.editor.toPlainText()
        tokens = Tokenizer.tokenize(text)

        try:
            ast_root = parse(tokens)

            if len(ast_root.children) == 0:
                print("Nothing to evaluate")

            interpreter = Interpreter()
            evaluated = interpreter.interpret(ast_root)
            self.output.appendPlainText(str(evaluated))

        # todo: handle exceptions properly
        except Exception as e:
            print(f"Something went wrong: {e}")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.resize(600, 400)
    window.show()

    sys.exit(app.exec_())
