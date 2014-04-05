from PyQt4 import Qt
from PyQt4 import QtCore
from toutvqt import utils


class _QBitrateButton(Qt.QPushButton):
    def __init__(self, bitrate, res):
        super().__init__()

        self._bitrate = bitrate
        self._res = res

        self._setup()

    def _setup(self):
        text = '{} kbps ({}p)'.format(self._bitrate // 1000, self._res)
        self.setText(text)

    def get_bitrate(self):
        return self._bitrate


class QChooseBitrateDialog(utils.QCommonDialog, utils.QtUiLoad):
    _UI_NAME = 'choose_bitrate_dialog'
    _resolutions = [270, 288, 360, 480]
    bitrate_chosen = QtCore.pyqtSignal(int, object)

    def __init__(self, episode, bitrates):
        super().__init__()

        self._episode = episode
        self._bitrates = bitrates

        self._setup_ui()

    def _setup_ui(self):
        self._load_ui(QChooseBitrateDialog._UI_NAME)

    def _populate_bitrate_buttons(self):
        resolutions = QChooseBitrateDialog._resolutions
        for bitrate, res in zip(self._bitrates, resolutions):
            btn = _QBitrateButton(bitrate, res)
            btn.clicked.connect(self._on_bitrate_btn_clicked)
            self.buttons_vbox.addWidget(btn)

    def _on_bitrate_btn_clicked(self):
        btn = self.sender()
        self.bitrate_chosen.emit(btn.get_bitrate(), self._episode)
        self.close()

    def show_move(self, pos):
        self._populate_bitrate_buttons()
        super().show_move(pos)
