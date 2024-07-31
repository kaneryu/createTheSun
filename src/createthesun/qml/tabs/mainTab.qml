import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Qt.labs.platform

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
        anchors.fill: parent
        id: background
        color: Theme.primary
        
        Behavior on color {
            ColorAnimation {
                easing.type: Easing.InOutQuad
                duration: 200
            }
        }
    }

}