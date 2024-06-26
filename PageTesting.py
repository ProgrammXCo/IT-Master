from PyQt6 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
import os
import datetime
import xml.etree.ElementTree as ET
import re
import enum
from PIL import Image
from dataclasses import dataclass
from Dialogs import DialogImageViewer

class AnswerStatus(enum.Enum):
    wrong = 0
    skip = 1
    right = 2

@dataclass
class DataResult:
    status: AnswerStatus
    user_answer: str | list | None

@dataclass
class DataResultTesting:
    date_start: datetime.datetime
    date_end: datetime.datetime
    path_course: str
    list_data_result: list[DataResult]

class TypeCellTableAnswer(enum.Enum):
    input = 0
    label = 1

@dataclass
class DataPageTest:
    answer: str | list | None
    horizontal_scrollbar_value: int = 0
    vertical__scrollbar_value: int = 0

class PushButtonNavigation(QtWidgets.QPushButton):
    """Базовый класс для кнопок навигации на панели инструменов"""
    push_button_navigation_current = None
    push_button_navigation_change_current = QtCore.pyqtSignal()
    push_button_navigation_clicked = QtCore.pyqtSignal()
    
    def __init__(self):
        super().__init__()

        self.__current = False 

        self.setObjectName("push_button_navigation")
        self.setFixedSize(50, 50)
        self.clicked.connect(self.push_button_navigation_press)
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.setProperty("current", self.current())

    def push_button_navigation_press(self):
        if self != PushButtonNavigation.push_button_navigation_current and PushButtonNavigation.push_button_navigation_current is not None:
            PushButtonNavigation.push_button_navigation_current.__set_current(False)

        if self != PushButtonNavigation.push_button_navigation_current:
            PushButtonNavigation.push_button_navigation_current = self
            self.__set_current(True)

            self.push_button_navigation_clicked.emit()

    def __set_current(self, state: bool):
        self.__current = state

        self.setProperty("current", self.current())
        self.style().unpolish(self)
        self.style().polish(self)

        self.push_button_navigation_change_current.emit()
    
    def current(self) -> bool:
        return self.__current

class PushButtonQuestion(PushButtonNavigation):
    """Класс для кнопок навигации по вопросам на панели инструменов"""
    push_button_question_clicked = QtCore.pyqtSignal(int)
    
    def __init__(self, number: int):
        super().__init__()

        self.__number = number
        self.__answered = False

        self.setObjectName("push_button_question")
        self.setText(f"{self.__number + 1}")
        self.setFont(QtGui.QFont("Segoe UI", 12))
        self.push_button_navigation_clicked.connect(self.__push_button_question_press)
        self.setProperty("answered", self.answered())

    def __push_button_question_press(self):
        self.push_button_question_clicked.emit(self.__number)

    def set_answered(self, state: bool):
        self.__answered = state

        self.setProperty("answered", self.answered())
        self.style().unpolish(self)
        self.style().polish(self)
    
    def answered(self) -> bool:
        return self.__answered

class PushButtonLesson(PushButtonNavigation):
    """Класс для кнопки теоретической части на панели инструменов"""
    push_button_lesson_clicked = QtCore.pyqtSignal()
    
    def __init__(self, path_images: str):
        super().__init__()

        self.__path_images = path_images

        self.setObjectName("push_button_lesson")
        self.setIcon(QtGui.QIcon(os.path.join(self.__path_images, r"lesson.png")))
        self.setIconSize(QtCore.QSize(35, 35))
        self.push_button_navigation_clicked.connect(self.__push_button_lesson_press)

    def __push_button_lesson_press(self):
        self.push_button_lesson_clicked.emit()

class LessonViewer(QtWebEngineWidgets.QWebEngineView):
    """Класс просмотра уроков в формате .pdf"""

    def __init__(self, path_lesson: str):
        super().__init__()

        self.__path_lesson = path_lesson

        self.settings().setAttribute(self.settings().WebAttribute.PluginsEnabled, True)
        self.settings().setAttribute(self.settings().WebAttribute.PdfViewerEnabled, True)

        self.setUrl(QtCore.QUrl.fromLocalFile(self.__path_lesson))

class LabelPromt(QtWidgets.QFrame):
    """Метка с подсказкой"""
    
    def __init__(self, promt: str, path_image: str):
        super().__init__()

        self.setObjectName("label_promt")

        self.__promt = promt
        self.__path_image = path_image

        self.__pixmap = QtGui.QPixmap(self.__path_image).scaled(18, 18, transformMode = QtCore.Qt.TransformationMode.SmoothTransformation)

        # главный макет
        self.__hbox_layout_main = QtWidgets.QHBoxLayout()
        self.__hbox_layout_main.setSpacing(0)
        self.__hbox_layout_main.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.__hbox_layout_main)

        # метка с полоской
        self.__label_line = QtWidgets.QLabel()
        self.__label_line.setObjectName("label_line")
        self.__label_line.setFixedSize(4, 30)
        
        self.__hbox_layout_main.addWidget(self.__label_line)
        self.__hbox_layout_main.addSpacing(10)

        # метка с иконкой
        self.__label_icon = QtWidgets.QLabel()
        self.__label_icon.setObjectName("label_icon")
        self.__label_icon.setPixmap(self.__pixmap )
        
        self.__hbox_layout_main.addWidget(self.__label_icon)
        self.__hbox_layout_main.addSpacing(10)

        # метка с текстом
        self.__label_text = QtWidgets.QLabel()
        self.__label_text.setObjectName("label_text")
        self.__label_text.setText(self.__promt)
        self.__label_text.setWordWrap(True)
        self.__label_text.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignLeft)
        self.__label_text.setFont(QtGui.QFont("Segoe UI", 12))
        self.__label_text.setFixedHeight(25)
        self.__label_text.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)

        self.__hbox_layout_main.addWidget(self.__label_text)

class LabelClickable(QtWidgets.QLabel):
    """Класс для кликабельной метки"""
    clicked = QtCore.pyqtSignal(QtGui.QMouseEvent)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.clicked.emit(event)

        return super().mouseReleaseEvent(event)

class CheckboxAnswer(QtWidgets.QWidget):
    """Класс для чекбоксов для ответов с возможностью переноса слов"""
    checkbox_answer_state_changed = QtCore.pyqtSignal(bool)

    def __init__(self, text: str, path_images: str):
        super().__init__()
        self.setObjectName("checkbox_answer")
        # self.setFixedHeight(32)

        self.__text = text
        self.__path_images = path_images
        self.__checked = False

        # self.__enabled = True

        self.__image_checked = QtGui.QIcon(os.path.join(self.__path_images, "checkbox_checked.png"))
        self.__image_unchecked = QtGui.QIcon(os.path.join(self.__path_images, "checkbox_unchecked.png"))        

        # главный макет
        self.__hbox_layout_main = QtWidgets.QHBoxLayout()
        self.__hbox_layout_main.setSpacing(0)
        self.__hbox_layout_main.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.__hbox_layout_main)

        # кнопка с флажком
        self.__push_button_flag = QtWidgets.QPushButton()
        self.__push_button_flag.setObjectName("push_button_flag")
        self.__push_button_flag.clicked.connect(self.__checkbox_clicked)
        self.__push_button_flag.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        self.__push_button_flag.setIconSize(QtCore.QSize(22, 22))
        self.__push_button_flag.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)

        self.__hbox_layout_main.addWidget(self.__push_button_flag)

        # кликабельная метка c текстом
        self.__label_text = LabelClickable()
        self.__label_text.setObjectName("label_text")
        self.__label_text.setText(self.__text)
        self.__label_text.setWordWrap(True)
        self.__label_text.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignLeft)
        self.__label_text.setFont(QtGui.QFont("Segoe UI", 14))
        self.__label_text.setSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        self.__label_text.clicked.connect(self.__checkbox_clicked)
        # self.__label_text.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)

        self.__hbox_layout_main.addWidget(self.__label_text)

        self.set_checked(checked = False)

    def is_enabled(self) -> bool:
        # return self.__enabled
        return super().isEnabled()

    def set_enabled(self, enabled: bool):
        # self.__enabled = enabled
        super().setEnabled(enabled)

    def is_checked(self) -> bool:
        return self.__checked

    def text(self) -> str:
        return self.__text

    def __checkbox_clicked(self):
        if not self.is_enabled():
            return
        if self.__checked:
            self.set_checked(checked = False)
        else:
            self.set_checked(checked = True)

    def enterEvent(self, event: QtGui.QEnterEvent):
        if self.is_enabled():
            self.__push_button_flag.setProperty("hover", True)
            self.__push_button_flag.style().unpolish(self.__push_button_flag)
            self.__push_button_flag.style().polish(self.__push_button_flag)

            self.__label_text.setProperty("hover", True)
            self.__label_text.style().unpolish(self.__label_text)
            self.__label_text.style().polish(self.__label_text)

        return super().enterEvent(event)

    def leaveEvent(self, event: QtGui.QEnterEvent):
        if self.is_enabled():
            self.__push_button_flag.setProperty("hover", False)
            self.__push_button_flag.style().unpolish(self.__push_button_flag)
            self.__push_button_flag.style().polish(self.__push_button_flag)

            self.__label_text.setProperty("hover", False)
            self.__label_text.style().unpolish(self.__label_text)
            self.__label_text.style().polish(self.__label_text)

        return super().leaveEvent(event)

    def set_checked(self, checked: bool):
        if checked:
            self.__checked = True

            self.__push_button_flag.setIcon(self.__image_checked)

        else:
            self.__checked = False

            self.__push_button_flag.setIcon(self.__image_unchecked)

        self.checkbox_answer_state_changed.emit(checked)

class RadioButtonAnswer(QtWidgets.QFrame):
    """Класс для радиокнопок для ответов с возможностью переноса слов"""
    radio_button_answer_toggled = QtCore.pyqtSignal(bool)

    def __init__(self, text: str, path_images: str):
        super().__init__()
        self.setObjectName("radio_button_answer")
        # self.setFixedHeight(32)

        self.__text = text
        self.__path_images = path_images
        self.__checked = False

        # self.__enabled = True
        
        self.__image_checked = QtGui.QIcon(os.path.join(self.__path_images, "radio_button_checked.png"))
        self.__image_unchecked = QtGui.QIcon(os.path.join(self.__path_images, "radio_button_unchecked.png"))

        # главный макет
        self.__hbox_layout_main = QtWidgets.QHBoxLayout()
        self.__hbox_layout_main.setSpacing(0)
        self.__hbox_layout_main.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.__hbox_layout_main)

        # кнопка с флажком
        self.__push_button_flag = QtWidgets.QPushButton()
        self.__push_button_flag.setObjectName("push_button_flag")
        self.__push_button_flag.clicked.connect(self.__radio_button_clicked)
        self.__push_button_flag.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        self.__push_button_flag.setIconSize(QtCore.QSize(22, 22))
        self.__push_button_flag.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)

        self.__hbox_layout_main.addWidget(self.__push_button_flag)

        # кликабельная метка c текстом
        self.__label_text = LabelClickable()
        self.__label_text.setObjectName("label_text")
        self.__label_text.setText(self.__text)
        self.__label_text.setWordWrap(True)
        self.__label_text.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignLeft)
        self.__label_text.setFont(QtGui.QFont("Segoe UI", 14))
        self.__label_text.setSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        self.__label_text.clicked.connect(self.__radio_button_clicked)
        # self.__label_text.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)

        self.__hbox_layout_main.addWidget(self.__label_text)

        self.set_checked(checked = False)

    def is_enabled(self) -> bool:
        # return self.__enabled
        return super().isEnabled()

    def set_enabled(self, enabled: bool):
        # self.__enabled = enabled
        super().setEnabled(enabled)

    def text(self) -> str:
        return self.__text

    def is_checked(self) -> bool:
        return self.__checked

    def __radio_button_clicked(self):
        if not self.is_enabled():
            return
        if not self.__checked:
            self.set_checked(checked = True)

    def enterEvent(self, event: QtGui.QEnterEvent):
        if self.is_enabled():
            self.__push_button_flag.setProperty("hover", True)
            self.__push_button_flag.style().unpolish(self.__push_button_flag)
            self.__push_button_flag.style().polish(self.__push_button_flag)

            self.__label_text.setProperty("hover", True)
            self.__label_text.style().unpolish(self.__label_text)
            self.__label_text.style().polish(self.__label_text)

        return super().enterEvent(event)

    def leaveEvent(self, event: QtGui.QEnterEvent):
        if self.is_enabled():
            self.__push_button_flag.setProperty("hover", False)
            self.__push_button_flag.style().unpolish(self.__push_button_flag)
            self.__push_button_flag.style().polish(self.__push_button_flag)

            self.__label_text.setProperty("hover", False)
            self.__label_text.style().unpolish(self.__label_text)
            self.__label_text.style().polish(self.__label_text)

        return super().leaveEvent(event)

    def set_checked(self, checked: bool):
        if checked:
            self.__checked = True

            self.__push_button_flag.setIcon(self.__image_checked)
        else:
            self.__checked = False

            self.__push_button_flag.setIcon(self.__image_unchecked)

        self.radio_button_answer_toggled.emit(checked)

class GroupRadiobuttonsAnswer(QtCore.QObject):
    """Класс для группирования RadiobuttonAnswer"""
    radio_button_checked = QtCore.pyqtSignal(RadioButtonAnswer)
    
    def __init__(self):
        super().__init__()

        self.__list_radio_buttons = []
        self.__checked_radio_button = None

    def __toggle_radio_button_answer(self):
        radio_button = self.sender()

        if radio_button.is_checked() and self.__checked_radio_button != radio_button:
            if self.__checked_radio_button is not None:
                self.__checked_radio_button.set_checked(checked = False)
            self.__checked_radio_button = radio_button

            self.radio_button_checked.emit(self.__checked_radio_button)

    def add_radio_button_answer(self, radio_button: RadioButtonAnswer):
        radio_button.radio_button_answer_toggled.connect(self.__toggle_radio_button_answer)
        self.__list_radio_buttons.append(radio_button)

class LineEditAnswer(QtWidgets.QLineEdit):
    """Класс для строки ввода ответов"""
    line_edit_answer_text_changed = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        # self.__enabled = True

        self.setObjectName("line_edit_answer")
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.textChanged.connect(self.__line_edit_text_changed)
        self.setFont(QtGui.QFont("Segoe UI", 14))
        self.setFixedHeight(42)

    def is_enabled(self) -> bool:
        # return self.__enabled
        return super().isEnabled()

    def set_enabled(self, enabled: bool):
        self.__enabled = enabled
        # if self.is_enabled():
        #     self.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        # else:
        #     self.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        super().setEnabled(enabled)

    def __line_edit_text_changed(self):
        self.line_edit_answer_text_changed.emit()

class LineEditMinimizeable(QtWidgets.QLineEdit):
    """Поле ввода с фиксированной подсказкой размера"""

    def sizeHint(self):
        return QtCore.QSize(super().fontMetrics().averageCharWidth() * 10, super().minimumSizeHint().height())

@dataclass
class DataCellTableAnswer:
    cell: LineEditMinimizeable
    type: TypeCellTableAnswer

class TableAnswer(QtWidgets.QWidget):
    """Класс для таблилы для ввода сопоставлений"""
    table_answer_changed = QtCore.pyqtSignal()

    def __init__(self, headers: list[str]):
        super().__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        self.setMinimumWidth(QtGui.QFontMetrics(QtGui.QFont("Segoe UI", 14)).averageCharWidth() * 50)
        self.setObjectName("table_answer")

        self.__headers = headers
        self.__list_cell_table_answer = list()
        self.__current_row = 0

        # self.__enabled = True        

        # главный макет
        self.__grid_layout_main = QtWidgets.QGridLayout()
        self.__grid_layout_main.setSpacing(0)
        self.__grid_layout_main.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.__grid_layout_main)

        self.__amount_columns = len(self.__headers)
        # метки заголовка
        for i, header in enumerate(self.__headers):
            label_header = QtWidgets.QLabel()
            label_header.setObjectName("label_header")
            label_header.setText(header)
            label_header.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            label_header.setFont(QtGui.QFont("Segoe UI", 14))
            label_header.setFixedHeight(42)

            if self.__amount_columns == 1:
                label_header.setProperty("only-one", True)
            elif i == 0:
                label_header.setProperty("first", True)
            elif i == self.__amount_columns - 1:
                label_header.setProperty("last", True)

            self.__grid_layout_main.addWidget(label_header, 0, i)

    def is_enabled(self) -> bool:
        # return self.__enabled
        return super().isEnabled()

    def set_enabled(self, enabled: bool):
        # self.__enabled = enabled
        if enabled:
            for row in self.__list_cell_table_answer:
                for element in row:
                    element.cell.setPlaceholderText("Введите правильное значение...")
        else:
            for row in self.__list_cell_table_answer:
                for element in row:
                    element.cell.setPlaceholderText("")

        super().setEnabled(enabled)

    def __add_empty_row(self):
        self.__current_row += 1
        self.__list_cell_table_answer.append(list())

        # поля ввода
        for i in range(len(self.__headers)):
            line_edit_answer = LineEditMinimizeable()
            line_edit_answer.setObjectName("line_edit_answer")
            line_edit_answer.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
            line_edit_answer.setFont(QtGui.QFont("Segoe UI", 14))
            line_edit_answer.setSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
            line_edit_answer.setMinimumWidth(25)
            line_edit_answer.setFixedHeight(42)
            line_edit_answer.setPlaceholderText("Введите правильное значение...")

            if self.__amount_columns == 1:
                line_edit_answer.setProperty("only-one", True)
            elif i == 0:
                line_edit_answer.setProperty("first", True)
            elif i == self.__amount_columns - 1:
                line_edit_answer.setProperty("last", True)

            self.__list_cell_table_answer[self.__current_row - 1].append(DataCellTableAnswer(cell = line_edit_answer, type = type))
            self.__grid_layout_main.addWidget(line_edit_answer, self.__current_row, i)

    def set_item(self, row: int, column: int, type: TypeCellTableAnswer, text: str = ""):
        # добавить пустуые строку если row - self.__current_row + 1 > 0
        for i in range(row - self.__current_row + 1):
            self.__add_empty_row()

        match type:
            case TypeCellTableAnswer.input:    
                self.__list_cell_table_answer[row][column].cell.setText(text)
                self.__list_cell_table_answer[row][column].cell.textChanged.connect(self.__table_answer_changed)
                self.__list_cell_table_answer[row][column].cell.setPlaceholderText("Введите правильное значение...")
            case TypeCellTableAnswer.label:
                self.__list_cell_table_answer[row][column].cell.setReadOnly(True)
                self.__list_cell_table_answer[row][column].cell.setPlaceholderText("")
                self.__list_cell_table_answer[row][column].cell.setText(text)

        self.__list_cell_table_answer[row][column].type = type

    def get_row_count(self) -> int:
        return self.__current_row
    
    def get_column_count(self) -> int:
        return self.__amount_columns

    def __table_answer_changed(self):
        self.table_answer_changed.emit()

    def get_text(self, row: int, column: int) -> str:
        return self.__list_cell_table_answer[row][column].cell.text()

    def get_type_cell(self, row: int, column: int) -> TypeCellTableAnswer:
        return self.__list_cell_table_answer[row][column].type

    def insert_text(self, row: int, column: int, text: str):
        self.__list_cell_table_answer[row][column].cell.setText(text)

class PushButtonImage(QtWidgets.QPushButton):
    """Класс для кнопки с изображением"""
    push_button_image_clicked = QtCore.pyqtSignal()
    
    def __init__(self, path_pixmap: str, path_images: str):
        super().__init__()

        self.setObjectName("push_button_image")
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.clicked.connect(self.__push_button_image_press)
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

        self.__path_pixmap = path_pixmap
        self.__path_images = path_images
        self.__dialog_image_viewer = None

        self.__min_size = QtCore.QSize(93, 93)
        self.__max_size = QtCore.QSize(393, 393)

        self.__pixmap = QtGui.QPixmap(self.__path_pixmap)

        zoom = 1

        if self.__pixmap.width() < self.__min_size.width() or self.__pixmap.height()  < self.__min_size.height():
            zoom = max(self.__min_size.width() / self.__pixmap.width(), self.__min_size.height() / self.__pixmap.height())
        if  self.__pixmap.width() > self.__max_size.width() or self.__pixmap.height()  > self.__max_size.height():
            zoom = min(self.__max_size.width() / self.__pixmap.width(), self.__max_size.height() / self.__pixmap.height())

        self.__pixmap = self.__pixmap.scaled(round(self.__pixmap.width() * zoom), round(self.__pixmap.height() * zoom), transformMode = QtCore.Qt.TransformationMode.SmoothTransformation)
        
        self.__target = QtGui.QPixmap(self.__pixmap.size())  
        self.__target.fill(QtCore.Qt.GlobalColor.transparent)

        painter = QtGui.QPainter(self.__target)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)

        painter_path = QtGui.QPainterPath()
        painter_path.addRoundedRect(0, 0, self.__pixmap.width(), self.__pixmap.height(), 14, 14)

        painter.setClipPath(painter_path)
        painter.drawPixmap(0, 0, self.__pixmap)
        painter.end()

        self.__image = QtGui.QIcon(self.__target)

        self.setIcon(self.__image)
        self.setIconSize(self.__target.size())
        self.setFixedSize(max(self.__target.width(), self.__min_size.width()) + 2, max(self.__target.height(), self.__min_size.height()) + 2)

        # макет для кнопки сохранить изображение
        self.__grid_layout_push_button_save = QtWidgets.QGridLayout()
        self.__grid_layout_push_button_save.setSpacing(0)
        self.__grid_layout_push_button_save.setContentsMargins(0, 0, 0, 0)
        self.__grid_layout_push_button_save.setColumnStretch(0, 1)
        self.__grid_layout_push_button_save.setColumnStretch(1, 0)
        self.__grid_layout_push_button_save.setRowStretch(0, 0)
        self.__grid_layout_push_button_save.setRowStretch(1, 1)

        self.setLayout(self.__grid_layout_push_button_save)

        # кнопка сохранить изображение
        self.__push_buttton_save_image = QtWidgets.QPushButton()
        self.__push_buttton_save_image.setObjectName("push_buttton_save_image")
        self.__push_buttton_save_image.clicked.connect(self.__save_image_as)
        self.__push_buttton_save_image.setFixedSize(40, 40)
        self.__push_buttton_save_image.setIcon(QtGui.QIcon(os.path.join(self.__path_images, r"save.png")))
        self.__push_buttton_save_image.setIconSize(QtCore.QSize(32, 32))
        self.__push_buttton_save_image.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)

        self.__push_buttton_save_image.hide()
        self.__grid_layout_push_button_save.addWidget(self.__push_buttton_save_image, 0, 1)
        
    def __push_button_image_press(self):
        self.__show_image()
        
        self.push_button_image_clicked.emit()

    def __show_image(self):
        if not self.__dialog_image_viewer:
            self.__dialog_image_viewer = DialogImageViewer(self)
            self.__dialog_image_viewer.set_window_title("Просмотр изображения")
            self.__dialog_image_viewer.set_window_icon(QtGui.QIcon(os.path.join(self.__path_images, r"image.png")))
            self.__dialog_image_viewer.load_image(self.__path_pixmap)
            self.__dialog_image_viewer.closing_window.connect(self.__closed_dialog_image_viewer)

            self.__dialog_image_viewer.show()

    def __closed_dialog_image_viewer(self):
        self.__dialog_image_viewer = None

    def close_dialog_image_viewer(self):
        if self.__dialog_image_viewer is not None:
            self.__dialog_image_viewer.close_window()
            
            self.__dialog_image_viewer = None

    def enterEvent(self, event):
        self.__push_buttton_save_image.show()

    def leaveEvent(self, event):
        self.__push_buttton_save_image.hide()

    def __save_image_as(self):
        directory_desktop = os.path.abspath(os.path.normpath(os.path.join(os.environ["HOMEPATH"], "Desktop")))
        file_formats = ["jpg", "jpeg", "jpe", "png", "tif", "tiff", "bmp"]
        extension_pixmap = os.path.splitext(self.__path_pixmap)[1][1:]
        if extension_pixmap in file_formats:
            file_formats.remove(extension_pixmap)
        file_formats.insert(0, extension_pixmap)
        file_formats = ";;".join([f".{i} (*.{i})" for i in file_formats])

        path_image, filter = QtWidgets.QFileDialog.getSaveFileName(
            self.window(), 
            "Сохранение изображения", 
            os.path.join(directory_desktop, os.path.basename(self.__path_pixmap)),
            file_formats,
            f".{extension_pixmap}"
        )

        if path_image:
            try:
                # selected_extension_file = re.search("\.\w+ \(\*\.(\w+)\)", filter).group(1)
                # if not re.match(f"^(.+?)\.{selected_extension_file}$", path_image):
                #     path_image = f"{os.path.normpath(path_image)}.{selected_extension_file}"

                pixmap = Image.open(self.__path_pixmap)
                pixmap.save(path_image)
            except Exception as error:
                msg = QtWidgets.QMessageBox(self.window())
                msg.setWindowTitle("Ошибка")
                msg.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                msg.setText("Неудалось сохранить изображение")
                msg.setInformativeText(str(error))
                msg.exec()
       
class PageQuestion(QtWidgets.QWidget):
    """Класс для страницы с вопросом"""
    answer_changed = QtCore.pyqtSignal(int, bool)

    def __init__(self, number: int, path_course: str, element: str, answer: str | list | None, started_passing: bool, path_images: str):
        super().__init__()
        self.setObjectName("page_question")

        self.__number = number
        self.__path_course = path_course
        self.__question = element
        self.__answer = answer
        self.__started_passing = started_passing
        self.__path_images = path_images
        self.__path_pixmap = None
        self.__push_button_image = None
        
        # главный макет
        self.__vbox_layout_main = QtWidgets.QGridLayout()
        self.__vbox_layout_main.setSpacing(0)
        self.__vbox_layout_main.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.__vbox_layout_main)

        # главная рамка
        self.__frame_main = QtWidgets.QFrame()
        self.__frame_main.setObjectName("frame_main")

        self.__vbox_layout_main.addWidget(self.__frame_main)

        # внутренний макет
        self.__vbox_layout_internal = QtWidgets.QVBoxLayout()
        self.__vbox_layout_internal.setSpacing(0)
        self.__vbox_layout_internal.setContentsMargins(20, 20, 20, 20)

        self.__frame_main.setLayout(self.__vbox_layout_internal)

        # метка номера задания
        self.__label_numder_question = QtWidgets.QLabel()
        self.__label_numder_question.setObjectName("label_numder_question")
        self.__label_numder_question.setFont(QtGui.QFont("Segoe UI", 12))
        self.__label_numder_question.setText(f"Вопрос {self.__number + 1}")

        self.__vbox_layout_internal.addWidget(self.__label_numder_question)

        # метка с вопросом
        self.__label_question = QtWidgets.QLabel()
        self.__label_question.setObjectName("label_question")
        self.__label_question.setWordWrap(True)
        self.__label_question.setFont(QtGui.QFont("Segoe UI", 14))
        self.__label_question.setText(self.__question.find("title").text)
        self.__label_question.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)

        self.__vbox_layout_internal.addWidget(self.__label_question)

        # метка типа задания
        self.__label_type_question = QtWidgets.QLabel()
        self.__label_type_question.setObjectName("label_type_question")
        self.__label_type_question.setFont(QtGui.QFont("Segoe UI", 12))

        self.__vbox_layout_internal.addWidget(self.__label_type_question)
        self.__vbox_layout_internal.addSpacing(5)

        # добавление кнопки с изображением, если оно присутствует
        if (path_pixmap := self.__question.find("image")) is not None and path_pixmap.text != "None":
            self.__path_pixmap = os.path.join(os.path.split(self.__path_course)[0], path_pixmap.text) # .replace("\\", "/")

            self.__push_button_image = PushButtonImage(path_pixmap = self.__path_pixmap, path_images = self.__path_images)

            self.__vbox_layout_internal.addWidget(self.__push_button_image)
            self.__vbox_layout_internal.addSpacing(5)

        # создание виджетов выбора или ввода ответов
        match self.__question.find("type").text:
            case "selectable_answer":
                self.__label_type_question.setText("Укажите правильный вариант ответа:")

                # группа радио кнопок
                self.__group_radio_buttons = GroupRadiobuttonsAnswer()

                list_questions = self.__question.findall("answer_option")

                self.__list_radio_buttons = list()

                # создание и упаковка радиокнопок
                for i, element in enumerate(list_questions):
                    radio_button = RadioButtonAnswer(
                        text = element.text,
                        path_images = self.__path_images
                    )

                    self.__list_radio_buttons.append(radio_button)

                    self.__group_radio_buttons.add_radio_button_answer(radio_button)
                    self.__group_radio_buttons.radio_button_checked.connect(self.__radio_button_checked)

                    if self.__started_passing and element.text == self.__answer:
                        radio_button.set_checked(True)

                    self.__vbox_layout_internal.addWidget(radio_button)
                    # if i < amount_questions:
                    #     self.__vbox_layout_internal.addSpacing(10)

            case "multiple_selectable_answers":
                self.__label_type_question.setText("Укажите правильные варианты ответа:")

                list_questions = self.__question.findall("answer_option")

                self.__list_checkboxes = list()

                # создание и упаковка чекбоксов
                for i, element in enumerate(list_questions):
                    checkbox = CheckboxAnswer(
                        text = element.text, 
                        path_images = self.__path_images
                    )

                    self.__list_checkboxes.append(checkbox)

                    checkbox.checkbox_answer_state_changed.connect(self.__ceckbox_checked)

                    if self.__started_passing and element.text in self.__answer:
                        checkbox.set_checked(True)

                    self.__vbox_layout_internal.addWidget(checkbox)
                    # if i < amount_questions:
                    #     self.__vbox_layout_internal.addSpacing(10)
                    
            case "input_answer":
                self.__label_type_question.setText("Введите правильный ответ:")
                
                self.__line_edit_answer = LineEditAnswer()
                self.__line_edit_answer.line_edit_answer_text_changed.connect(self.__line_edit_answer_text_changed)

                self.__vbox_layout_internal.addWidget(self.__line_edit_answer)
                self.__vbox_layout_internal.addSpacing(5)

                # метка с подсказкой
                self.__label_promt = LabelPromt(
                    "Для записи десятичных дробей используется запятая, а не точка.",
                    os.path.join(self.__path_images, "warning.png")
                )
                self.__label_promt.hide()

                self.__vbox_layout_internal.addWidget(self.__label_promt)

                if self.__started_passing:
                    self.__line_edit_answer.insert(self.__answer)

            case "comparison_table":
                self.__label_type_question.setText("Заполните пустые ячейки таблицы:")

                list_questions = list(element.text for element in self.__question.findall("header"))

                self.__table_answer = TableAnswer(list_questions)
                self.__table_answer.table_answer_changed.connect(self.__table_answer_changed)

                for i_row, row in enumerate(self.__question.findall("row")):
                    for i_column, element in enumerate(row.findall("cell")):
                        match element.attrib["type"]:
                            case "label":
                                type = TypeCellTableAnswer.label
                                self.__table_answer.set_item(row = i_row, column = i_column, type = type, text = element.attrib["text"])
                            case "input":
                                type = TypeCellTableAnswer.input
                                if self.__started_passing:
                                    self.__table_answer.set_item(row = i_row, column = i_column, type = type, text = self.__answer[i_row][i_column - len(row.findall("cell"))])
                                else:
                                    self.__table_answer.set_item(row = i_row, column = i_column, type = type, text = "")

                self.__vbox_layout_internal.addWidget(self.__table_answer)

        self.__vbox_layout_internal.addStretch(1)
        
    def answer(self) -> str | list | None:
        return self.__answer

    def __radio_button_checked(self, radio_button: RadioButtonAnswer):
        self.__answer = radio_button.text()

        self.answer_changed.emit(self.__number, True)

    def __ceckbox_checked(self):
        text_sender = self.sender().text()

        if self.sender().is_checked() and text_sender not in self.__answer:
            self.__answer.append(text_sender)
            self.answer_changed.emit(self.__number, True if len(self.__answer) != 0 else False)
        elif not self.sender().is_checked() and text_sender in self.__answer:
            self.__answer.remove(text_sender)
            self.answer_changed.emit(self.__number, True if len(self.__answer) != 0 else False)

    def __line_edit_answer_text_changed(self):
        self.__answer = self.__line_edit_answer.text()

        if re.search("(\d\.)", self.__answer):
            self.__label_promt.show()
        else:
            self.__label_promt.hide()

        self.answer_changed.emit(self.__number, True if self.__answer != "" else False)

    def __table_answer_changed(self):
        self.__answer = list()

        for row in range(self.__table_answer.get_row_count()):
            self.__answer.append(list())
            for column in range(self.__table_answer.get_column_count()):
                if self.__table_answer.get_type_cell(row, column) == TypeCellTableAnswer.input:
                    self.__answer[row].append(self.__table_answer.get_text(row, column))

        self.answer_changed.emit(self.__number, any(list(any(i) for i in self.__answer)))

    def close_dialog_image_viewer(self):
        if self.__push_button_image is not None:  
            self.__push_button_image.close_dialog_image_viewer()

class PageTesting(QtWidgets.QWidget):
    """Главный класс тестирования"""
    push_button_finish_cliced = QtCore.pyqtSignal(DataResultTesting)

    def __init__(self, path_course: str, path_images: str):
        super().__init__()
        self.setObjectName("page_testing")

        self.__path_images = path_images
        self.__path_course = path_course
        self.__path_lesson = None

        self.__tree = ET.parse(self.__path_course)
        self.__root = self.__tree.getroot()

        lesson = self.__root.find("lesson")
        if lesson is not None:
            self.__path_lesson = os.path.abspath(os.path.join(os.path.split(self.__path_course)[0], lesson.text))
            if lesson.text == "None":
                self.__path_lesson = None
        
        self.__page_question = None
        self.__page_lesson = None
        self.__current_number_question = 0

        self.__time_start = datetime.datetime.now()
        self.__len_course = len(self.__root.findall("question"))
        self.__list_data_page_test: list[DataPageTest] = list()
        self.__list_push_button_questions = list()
        self.__dict_questions_started_passing = {i: False for i in range(self.__len_course)}

        for i in range(self.__len_course):
            type_question = self.__root.findall("question")[i].find("type").text
            if type_question in ("multiple_selectable_answers", "comparison_table"):
                self.__list_data_page_test.append(DataPageTest(list()))
            elif type_question in ("selectable_answer", "input_answer"):
                self.__list_data_page_test.append(DataPageTest(None))

        # главный макет
        self.__vbox_layout_main = QtWidgets.QGridLayout()
        self.__vbox_layout_main.setSpacing(0)
        self.__vbox_layout_main.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.__vbox_layout_main)

        # главная рамка
        self.__frame_main = QtWidgets.QFrame()
        self.__frame_main.setObjectName("frame_main")

        self.__vbox_layout_main.addWidget(self.__frame_main)

        # внутренний макет
        self.__vbox_layout_internal = QtWidgets.QVBoxLayout()
        self.__vbox_layout_internal.setSpacing(0)
        self.__vbox_layout_internal.setContentsMargins(0, 0, 0, 0)

        self.__frame_main.setLayout(self.__vbox_layout_internal)

        # виджет стеков для страниц вопросов теста
        self.__stacked_widget = QtWidgets.QStackedWidget()
        self.__stacked_widget.setObjectName("stacked_widget")

        self.__vbox_layout_internal.addWidget(self.__stacked_widget)

        # прокручиваемая область для станица теста
        self.__scroll_area_page_test = QtWidgets.QScrollArea()
        self.__scroll_area_page_test.setObjectName("scroll_area_page_test")
        self.__scroll_area_page_test.setWidgetResizable(True)

        self.__stacked_widget.addWidget(self.__scroll_area_page_test)

        # панель инструментов
        self.__frame_tools = QtWidgets.QFrame()
        self.__frame_tools.setObjectName("frame_tools")
        
        self.__vbox_layout_internal.addWidget(self.__frame_tools)

        # макет панели инстументов
        self.__hbox_layout_tools = QtWidgets.QHBoxLayout()
        self.__hbox_layout_tools.setSpacing(0)
        self.__hbox_layout_tools.setContentsMargins(20, 10, 20, 0)

        self.__frame_tools.setLayout(self.__hbox_layout_tools)

        if self.__path_lesson:
            # кнопка для открытия урока в формате .pdf
            self.__push_button_lesson = PushButtonLesson(self.__path_images)
            self.__push_button_lesson.push_button_lesson_clicked.connect(self.__open_lesson)

            self.__hbox_layout_tools.addWidget(self.__push_button_lesson)
            self.__hbox_layout_tools.addSpacing(10)
            self.__hbox_layout_tools.setAlignment(self.__push_button_lesson, QtCore.Qt.AlignmentFlag.AlignTop)

        # прокручиваемая область для кнопок навигации по вопросам
        self.__scroll_area_push_button_questions = QtWidgets.QScrollArea()
        self.__scroll_area_push_button_questions.setObjectName("scroll_area_push_button_questions")
        self.__scroll_area_push_button_questions.setSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Fixed)
        self.__scroll_area_push_button_questions.verticalScrollBar().setEnabled(False)
        self.__scroll_area_push_button_questions.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.__scroll_area_push_button_questions.setWidgetResizable(True)

        self.__hbox_layout_tools.addWidget(self.__scroll_area_push_button_questions)
        self.__hbox_layout_tools.addSpacing(10)

        # рамка для кнопок навигации по вопросам
        self.__frame_push_button_questions = QtWidgets.QFrame()
        self.__frame_push_button_questions.setObjectName("frame_push_button_questions")

        self.__scroll_area_push_button_questions.setWidget(self.__frame_push_button_questions)

        # макет для кнопок навигации по вопросам
        self.__hbox_layout_button_questions = QtWidgets.QHBoxLayout()
        self.__hbox_layout_button_questions.setSpacing(0)
        self.__hbox_layout_button_questions.setContentsMargins(0, 0, 0, 0)

        self.__frame_push_button_questions.setLayout(self.__hbox_layout_button_questions)

        self.__hbox_layout_button_questions.addStretch(1)

        for i in range(self.__len_course):
            push_button_question = PushButtonQuestion(number = i)
            push_button_question.push_button_question_clicked.connect(self.__switch_question)
            self.__list_push_button_questions.append(push_button_question)

            self.__hbox_layout_button_questions.addWidget(push_button_question)
            if i < self.__len_course:
                self.__hbox_layout_button_questions.addSpacing(10)

        self.__hbox_layout_button_questions.addStretch(1)

        # кнопка завершить тест
        self.__push_button_finish = QtWidgets.QPushButton()
        self.__push_button_finish.setObjectName("push_button_finish")
        self.__push_button_finish.clicked.connect(self.__finish_test)
        self.__push_button_finish.setText("Завершить тест")
        self.__push_button_finish.setFont(QtGui.QFont("Segoe UI", 12))
        self.__push_button_finish.setFixedHeight(50)
        self.__push_button_finish.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)

        self.__hbox_layout_tools.addWidget(self.__push_button_finish)
        self.__hbox_layout_tools.setAlignment(self.__push_button_finish, QtCore.Qt.AlignmentFlag.AlignTop)

        if self.__path_lesson:
            # открыть урок
            self.__push_button_lesson.push_button_navigation_press()
        else:
            # открыть первую страницу теста
            self.__list_push_button_questions[self.__current_number_question].push_button_navigation_press()

    def __open_lesson(self):
        # создание и упаковка новой страницы для просмотра урока в формате .pdf
        if self.__page_lesson is None:
            self.__page_lesson = LessonViewer(path_lesson = self.__path_lesson)

            self.__stacked_widget.addWidget(self.__page_lesson)

        self.__stacked_widget.setCurrentWidget(self.__page_lesson)

    def __finish_test(self):
        if self.__page_question is not None:
            self.__page_question.close_dialog_image_viewer()
            # получение ответа текущей страницы
            self.__list_data_page_test[self.__current_number_question].answer = self.__page_question.answer()

        list_data_result = list()

        for i in range(self.__len_course):
            user_answer = self.__list_data_page_test[i].answer
            type_question = self.__root.findall("question")[i].find("type").text
            if type_question != "comparison_table":
                right_answer = list(i.text for i in self.__root.findall("question")[i].findall("correct_answer"))
            else:
                right_answer = list()
                for i_row, row in enumerate(self.__root.findall("question")[i].findall("row")):
                    right_answer.append(list())
                    for element in row.findall("correct_answer"):
                        right_answer[i_row].append(element.text)
            status = None

            if self.__dict_questions_started_passing[i]:
                # если один выбираемый ответ
                match type_question:
                    case "selectable_answer":
                        if user_answer == right_answer[0]:
                            status = AnswerStatus.right
                        else:
                            status = AnswerStatus.wrong

                    # если несколько выбираемых ответов
                    case "multiple_selectable_answers":
                        right_answer.sort()
                        user_answer.sort()

                        if user_answer == right_answer:
                            status = AnswerStatus.right
                        else:
                            status = AnswerStatus.wrong

                    # если ввод ответа
                    case "input_answer":
                        # убирает пробелы в начале и конце
                        right_answer = re.sub(r"^\s*|\s*$", r"", right_answer[0])
                        user_answer = re.sub(r"^\s*|\s*$", r"", user_answer)

                        if right_answer == user_answer:
                            status = AnswerStatus.right
                        else:
                            status = AnswerStatus.wrong

                    # если сопоставление
                    case "comparison_table":
                        if right_answer == user_answer:
                            status = AnswerStatus.right
                        else:
                            status = AnswerStatus.wrong
            else:
                status = AnswerStatus.skip

            list_data_result.append(DataResult(
                status = status, 
                user_answer = user_answer
            ))

        data_result_testing = DataResultTesting(
            date_start = self.__time_start,
            date_end = datetime.datetime.now(),
            path_course = self.__path_course,
            list_data_result = list_data_result
        )

        self.push_button_finish_cliced.emit(data_result_testing)

    def __switch_question(self, number: int):
        current_question = self.__root.findall("question")[number]

        if self.__page_question is not None:
            self.__page_question.close_dialog_image_viewer()

            # сохранение ответа текущей страницы в список ответов
            self.__list_data_page_test[self.__current_number_question].answer = self.__page_question.answer()
            self.__list_data_page_test[self.__current_number_question].horizontal_scrollbar_value = self.__scroll_area_page_test.horizontalScrollBar().value()
            self.__list_data_page_test[self.__current_number_question].vertical__scrollbar_value = self.__scroll_area_page_test.verticalScrollBar().value()

            # удаление старой страницы
            self.__scroll_area_page_test.widget().deleteLater()

        self.__current_number_question = number

        # создание и упаковка новой страницы вопроса
        self.__page_question = PageQuestion(
            number = self.__current_number_question,
            path_course = self.__path_course, 
            element = current_question,
            answer = self.__list_data_page_test[number].answer, 
            started_passing = self.__dict_questions_started_passing[number],
            path_images = self.__path_images     
        )
        self.__page_question.answer_changed.connect(self.__on_change_answer)

        self.__scroll_area_page_test.setWidget(self.__page_question)
        self.__scroll_area_page_test.horizontalScrollBar().setValue(self.__list_data_page_test[self.__current_number_question].horizontal_scrollbar_value)
        self.__scroll_area_page_test.verticalScrollBar().setValue(self.__list_data_page_test[self.__current_number_question].vertical__scrollbar_value)
        self.__stacked_widget.setCurrentWidget(self.__scroll_area_page_test)

    def __on_change_answer(self, number: int, answered: bool):
        self.__list_push_button_questions[number].set_answered(answered)
        self.__dict_questions_started_passing[number] = answered

    def close_dialog_image_viewer(self):
        if self.__page_question is not None:
            self.__page_question.close_dialog_image_viewer()
