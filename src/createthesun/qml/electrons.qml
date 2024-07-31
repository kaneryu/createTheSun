import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Qt.labs.platform

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
        text: "Electrons"
        color: Theme.primary
        font.pixelSize: 24
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
    }

}