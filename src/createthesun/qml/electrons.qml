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

    Rectangle {
        id: textDebugFill
        color: "transparent"

        width: text.width
        height: text.height

        x: text.x
        y: text.y
    }

    Text {
        id: text
        text: Items.getItem("electrons").amount
        color: Theme.tertiary
        font.pixelSize: 24


        anchors.top: parent.top
        width: parent.width
        /* center text */
        horizontalAlignment: Text.AlignHCenter
        height: 24

        TextMetrics {
            id: textMetrics
            text: text.text
            font: text.font
        }
    }

    Kyu.ProgressBar {
        id: progressBar

        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: text.bottom
        anchors.bottom: parent.bottom 

        anchors.topMargin: 10
        
        percent: 50
        vertical: true

        fillColor: Theme.tertiary
        backgroundColor: "transparent"
        radius: 5
        border.color: Theme.tertiary
        border.width: 1
    }
}