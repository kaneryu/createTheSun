import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Qt.labs.platform

import "./qml/" as ProgressBar

Item {
    id: root
    property QtObject mainModel // absract list model from python
    
    width: 63/2

    Connections {
        target: Backend
    }

    Connections {
        target:Theme
    }


    Text {
        id: text
        text: backend.items.electrons.count
        color: Theme.tertiary
        font.pixelSize: 24
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
    }

    ProgressBar {
        id: progress
        anchors.fill: parent
        percent: 50
        fillColor: Theme.tertiary
        backgroundColor: "transparent"
        radius: 5
        border.color: Theme.tertiary
        border.width: 2
    }

}