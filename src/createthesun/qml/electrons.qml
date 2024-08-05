import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Qt.labs.platform

import "." as Kyu



Item {
    id: root
    property QtObject mainModel // absract list model from python
    


    Connections {
        target: Backend
    }

    Connections {
        target:Theme
    }


    Text {
        id: text
        text: Items.getItem("electrons").amount
        color: Theme.tertiary
        font.pixelSize: 24
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
        anchors.top: parent.top
        width: parent.width
    }

    Kyu.ProgressBar {
        id: progressBar

        anchors.top: text.bottom

        width: parent.width

        percent: 50
        vertical: true

        fillColor: Theme.tertiary
        backgroundColor: "transparent"
        radius: 5
        border.color: Theme.tertiary
        border.width: 1
    }
}