import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
    id: root
    width: 50
    height: 100
    property real percent: 50
    Rectangle {
        id: background
        color: "transparent"
        border.color: "black"
        border.width: 2
        radius: 5
        anchors.fill: parent
        Rectangle {
            id: fill
            color: "red"
            width: parent.width * (root.percent / 100)
            height: parent.height
        }
    }
}