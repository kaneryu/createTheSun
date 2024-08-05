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
    anchors.fill: parent

    ListView {
    id: tabBar
    model: ItemsModel
    
    anchors.fill: parent

    orientation: ListView.Vertical
    
    spacing: 2
    delegate: Rectangle {
        id: rect
        topRightRadius: 10/2
        topLeftRadius: 10/2

        width: metrics.width + 10
        height: 43 / 2

        color: Theme.surfaceContainer

        border.color: Theme.primaryFixed
        border.width: 1/2

        Text {
            id: tabText
            text: "You have " + model.item.amount + " " + model.item.getName()
            color: Theme.onSurface
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            anchors.fill: parent

            Behavior on color {
                ColorAnimation {
                    easing.type: Easing.InOutQuad
                    duration: 200
                }
            }
        }

        TextMetrics {
            id: metrics
            text: tabText.text
            font: tabText.font
        }

        Behavior on color {
            ColorAnimation {
                easing.type: Easing.InOutQuad
                duration: 200
            }
        }
    }
}

}