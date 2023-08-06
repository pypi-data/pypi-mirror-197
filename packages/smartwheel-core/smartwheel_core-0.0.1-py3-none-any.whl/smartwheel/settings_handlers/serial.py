import logging

from PyQt6.QtWidgets import QListView

from smartwheel.settings_handlers.base import BaseHandler


class SerialHandler(BaseHandler):
    def __init__(self, value_getter, value_setter, parent_obj=None):
        super(SerialHandler, self).__init__(value_getter, value_setter, parent_obj)
        self.logger = logging.getLogger(__name__)

    def initElem(self, elem):
        l_view = QListView()
