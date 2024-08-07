import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Qt.labs.platform


Item {
    id: root

    property bool visible_: false
    property string text: ""

    property alias color: background.color
    property alias radius: background.radius
    property alias border: background.border

    property alias textColor: tooltipText.color
    property alias textSize: tooltipText.font.pixelSize

    opacity: 0.0

    property real fadeInDuration: 500
    property real fadeOutDuration: 500

    states: [
        State {
            name: "visible"
            when: root.visible_
            PropertyChanges {
                target: root
                opacity: 1.0
            }
        },
        State {
            name: "hidden"
            when: !root.visible_
            PropertyChanges {
                target: root
                opacity: 0.0
            }
        }
    ]

    transitions: [
        Transition {
            from: "hidden"
            to: "visible"
            NumberAnimation {
                target: root
                property: "opacity"
                duration: fadeInDuration
            }
        },
        Transition {
            from: "visible"
            to: "hidden"
            NumberAnimation {
                target: root
                property: "opacity"
                duration: fadeOutDuration
            }
        }
    ]

    Rectangle {
        id: background
        color: "black"
        radius: 5
        border.color: "white"
        border.width: 1
        anchors.fill: parent
    }

    Text {
        id: tooltipText
        text: root.text
        color: "white"
        anchors.centerIn: parent
    }
}