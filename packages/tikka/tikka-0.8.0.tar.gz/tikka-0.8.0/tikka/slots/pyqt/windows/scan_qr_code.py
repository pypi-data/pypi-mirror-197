# Copyright 2021 Vincent Texier <vit@free.fr>
#
# This software is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import sys
from typing import List, Optional

import cv2
import numpy as np
from PyQt5 import QtMultimedia
from PyQt5.QtCore import QLine, QPoint, pyqtSignal
from PyQt5.QtGui import QColor, QFont, QImage, QPainter, QPixmap
from PyQt5.QtMultimedia import (
    QAbstractVideoBuffer,
    QAbstractVideoSurface,
    QCamera,
    QCameraInfo,
    QVideoFrame,
)
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QWidget
from substrateinterface.utils.ss58 import is_valid_ss58_address

from tikka.domains.application import Application
from tikka.domains.entities.account import Account
from tikka.domains.entities.constants import DATA_PATH
from tikka.domains.entities.events import AccountEvent
from tikka.slots.pyqt.entities.constants import ADDRESS_MONOSPACE_FONT_NAME
from tikka.slots.pyqt.resources.gui.windows.scan_qrcode_rc import Ui_ScanQRCodeDialog


def q_image_to_cv_mat(incoming_image):
    """
    Converts a QImage into an opencv MAT format

    :param incoming_image: QImage instance
    :return:
    """
    incoming_image = incoming_image.convertToFormat(QImage.Format.Format_RGB32)

    width = incoming_image.width()
    height = incoming_image.height()

    ptr = incoming_image.bits()
    ptr.setsize(height * width * 4)
    arr = np.frombuffer(ptr, np.uint8).reshape((height, width, 4))
    return arr


class QRCodeVideoSurface(QAbstractVideoSurface):

    detected = pyqtSignal(str, name="detected")

    def __init__(self, video_label: QLabel):
        super().__init__()
        self.video_label = video_label

        # initialize the OpenCV QRCode detector
        self.detector = cv2.QRCodeDetector()

    def supportedPixelFormats(
        self, type: QAbstractVideoBuffer.HandleType = QAbstractVideoBuffer.NoHandle
    ) -> List[QVideoFrame.PixelFormat]:
        result = []
        if type == QtMultimedia.QAbstractVideoBuffer.NoHandle:
            result = [
                QtMultimedia.QVideoFrame.Format_RGB32,
            ]

        return result

    def present(self, frame: QVideoFrame) -> bool:
        """
        Process image in this function

        :param frame: QVideoFrame instance
        :return:
        """
        if frame.isValid() and self.isActive():
            # copy frame buffer
            copy = QtMultimedia.QVideoFrame(frame)
            copy.map(QtMultimedia.QAbstractVideoBuffer.ReadOnly)

            # create QImage from frame buffer copy
            image_format = QtMultimedia.QVideoFrame.imageFormatFromPixelFormat(
                copy.pixelFormat()
            )
            image = QImage(
                copy.bits(),
                copy.width(),
                copy.height(),
                copy.bytesPerLine(),
                QImage.Format(image_format),
            )

            # detect QRcode data from image converted to opencv format
            data, vertices_array, _ = self.detector.detectAndDecode(
                q_image_to_cv_mat(image)
            )
            # check if there is a QRCode in the image
            if vertices_array is not None:
                if data:
                    self.detected.emit(data)
                    # print("QR Code detected, data:", data)
                    # [[[127.       162.      ]
                    #   [221.       461.      ]
                    #   [476.5759     3.548942]
                    #   [477.         0.      ]]]

                    # draw a green rectangle around the detected QRcode
                    painter = QPainter(image)
                    pen = painter.pen()
                    pen.setColor(QColor(0, 255, 0))
                    pen.setWidth(5)
                    painter.setPen(pen)

                    nr_of_points = 4
                    for i in range(nr_of_points):
                        next_point_index = (i + 1) % nr_of_points
                        painter.drawLine(
                            QLine(
                                QPoint(
                                    int(vertices_array[0][i][0]),
                                    int(vertices_array[0][i][1]),
                                ),
                                QPoint(
                                    int(vertices_array[0][next_point_index][0]),
                                    int(vertices_array[0][next_point_index][1]),
                                ),
                            )
                        )
                    painter.end()

            # display image in video label
            self.video_label.resize(image.size())
            self.video_label.setPixmap(QPixmap.fromImage(image))

            copy.unmap()
            self.video_label.update()

            return True

        return False


class ScanQRCodeWindow(QDialog, Ui_ScanQRCodeDialog):
    """
    AddressAddFromQRCodeWindow class
    """

    def __init__(self, application: Application, parent: Optional[QWidget] = None):
        """
        Init add address from qrcode window

        :param application: Application instance
        :param parent: QWidget instance
        """
        super().__init__(parent=parent)
        self.setupUi(self)

        self.application = application
        self._ = self.application.translator.gettext
        self.camera = None
        self.address: Optional[str] = None

        # set monospace font to address field
        monospace_font = QFont(ADDRESS_MONOSPACE_FONT_NAME)
        monospace_font.setStyleHint(QFont.Monospace)
        self.addressValueLabel.setFont(monospace_font)

        # fill form
        if self.check_camera_availability() is False:
            self.errorLabel.setText(self._("No camera available"))
        else:
            self.camera = QCamera()
            self.video_surface = QRCodeVideoSurface(self.videoLabel)
            self.camera.setViewfinder(self.video_surface)
            self.camera.start()

        # buttons
        self.buttonBox.button(self.buttonBox.Ok).setEnabled(False)

        # events
        if self.check_camera_availability() is True:
            self.video_surface.detected.connect(self.qrcode_detected)
        self.buttonBox.accepted.connect(self.on_accepted_button)
        self.buttonBox.rejected.connect(self.close)

    @staticmethod
    def check_camera_availability():
        """
        Check if a camera is available

        :return:
        """
        return len(QCameraInfo.availableCameras()) > 0

    def qrcode_detected(self, data: str):
        """
        Triggered when a qrcode is detected
        Set address value label to data value

        :param data: Data in QRCode
        :return:
        """
        if not is_valid_ss58_address(data):
            self.address = None
            self.errorLabel.setText(self._("Account address is not valid!"))
            self.buttonBox.button(self.buttonBox.Ok).setEnabled(False)
        else:
            self.address = data
            self.addressValueLabel.setText(data)
            self.errorLabel.setText("")
            self.buttonBox.button(self.buttonBox.Ok).setEnabled(True)

    def on_accepted_button(self) -> None:
        """
        Triggered when user click on ok button

        :return:
        """
        if self.address is not None:
            account = self.application.accounts.get_by_address(self.address)
            if account is None:
                # create account instance
                account = Account(self.address, name=self._("Added from a QRCode"))

                # add instance in application
                self.application.accounts.add(account)
            else:
                # dispatch event
                event = AccountEvent(
                    AccountEvent.EVENT_TYPE_ADD,
                    account,
                )
                self.application.event_dispatcher.dispatch_event(event)


if __name__ == "__main__":
    qapp = QApplication(sys.argv)
    application_ = Application(DATA_PATH)
    ScanQRCodeWindow(application_).exec_()
