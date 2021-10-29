# This Python file uses the following encoding: utf-8
import sys
import os


from PySide2.QtWidgets import QApplication, QWidget
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader


class layout:

    LEFT = 0
    RIGHT = 1

    def __init__(self):
        pass

    @classmethod
    def is_chinese(cls, ch):
        """
        检查字符是否为中文字符
        :param char: 需要检查的字符
        :return: bool
        """
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
        else:
            return False

    @classmethod
    def is_eng_punctuation(cls, ch):
        """
        判断 ',:!?;'
        """
        eng_punc = ',:!?;'
        if ch in eng_punc:
            return ch
        else:
            return False

    @classmethod
    def is_bracket(cls, ch, orientation: int):
        """
        判断 ',:!?;'
        """
        left_bracket = '<{[('
        right_bracket = ')]}>'
        if orientation == layout.LEFT:
            eng_bracket = left_bracket
        elif orientation == layout.RIGHT:
            eng_bracket = right_bracket
        else:
            eng_bracket = None

        if ch in eng_bracket:
            return ch
        else:
            return False

    @classmethod
    def split_eng_cn(cls, content):
        splited_content = ''
        pos = 0
        while pos + 1 != len(content):
            splited_content += content[pos]
            if (content[pos].encode('utf-8').isalpha() and layout.is_chinese(content[pos + 1])) or \
               (layout.is_chinese(content[pos]) and content[pos + 1].encode('utf-8').isalpha()):
                splited_content += ' '
            pos += 1

        splited_content += content[pos]

        return splited_content

    @classmethod
    def split_num(cls, content):
        splited_content = ''
        pos = 0
        while pos + 1 != len(content):
            splited_content += content[pos]
            if (content[pos].isdigit() and layout.is_chinese(content[pos + 1])) or \
               (layout.is_chinese(content[pos]) and content[pos + 1].isdigit()):
                splited_content += ' '
            pos += 1

        splited_content += content[pos]

        return splited_content

    @classmethod
    def split_eng_punctuation(cls, content):
        """
        英文标点后面插入空格
        :param content:
        :return:
        """
        splited_content = ''
        pos = 0
        while pos + 1 != len(content):
            splited_content += content[pos]
            if layout.is_eng_punctuation(content[pos]) and content[pos + 1] != ' ':
                splited_content += ' '
            pos += 1

        splited_content += content[pos]

        return splited_content

    @classmethod
    def split_brace(cls, content):
        """
        英文括号
        :param content:
        :return:
        """
        splited_content = ''
        pos = 0
        while pos + 1 != len(content):
            if content[pos] != ' ' and layout.is_bracket(content[pos + 1], layout.LEFT):
                splited_content += content[pos]
                splited_content += ' '
            else:
                splited_content += content[pos]
            if layout.is_bracket(content[pos], layout.RIGHT) and content[pos + 1] != ' ':
                splited_content += ' '
            pos += 1

        splited_content += content[pos]

        return splited_content


class Main(QWidget):
    def __init__(self):
        super(Main, self).__init__()
        self.load_ui()

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "main.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.window = loader.load(ui_file, self)
        ui_file.close()
        self.window.Input.textChanged.connect(self.layout)

    def layout(self):
        content = self.window.Input.toPlainText()
        if (content != ''):
            content = layout.split_eng_cn(content)
            content = layout.split_num(content)
            content = layout.split_eng_punctuation(content)
            content = layout.split_brace(content)

        self.window.Output.setText(content)


if __name__ == "__main__":
    app = QApplication([])
    widget = Main()
    widget.show()
    sys.exit(app.exec_())
