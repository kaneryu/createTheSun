import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Qt.labs.platform

import ".." as Kyu

Item {
    id: root

    property real largestTextWidth

    anchors.fill: parent

    Rectangle {
        id: buyX
        width: parent.width
        height: 55 / 2
        color: "transparent"

        Text {
            id: buyXText
            text: "Buy x "
            color: Theme.onSurface
            font.pixelSize: 18
            anchors.left: parent.left
        }

        TextField {
            id: buyXField
            width: 50
            height: parent.height
            anchors.left: buyXText.right
            anchors.right: buyXButton.left
            anchors.rightMargin: 5
            text: "1"

            validator: IntValidator { bottom: 1 }
            inputMethodHints: Qt.ImhDigitsOnly
            font.pixelSize: 18
            color: Theme.onSurface
            verticalAlignment: Text.AlignVCenter

            background: Rectangle {
                color: "transparent"
                border.color: Theme.onSurface
                border.width: 1

                Behavior on color {
                    ColorAnimation {
                        easing.type: Easing.InOutQuad
                        duration: 200
                    }
                }
            }
        }

        Kyu.CustomButton {
            id: buyXButton
            height: parent.height
            text: "Max All"
            textPixelSize: 18
            width: 65
            anchors.right: parent.right
            anchors.rightMargin: 15
        }
    }
    ListView {
    id: tabBar
    model: ItemsModel
    
    anchors.top: buyX.bottom
    anchors.left: parent.left
    anchors.right: parent.right
    height: parent.height - buyX.height

    orientation: ListView.Vertical
    
    spacing: 2
    
    delegate: Rectangle {
        id: rect

        width: parent.width
        height: 55 / 2

        color: "transparent"

        ToolTip {
            id: tooltip
            text: model.item.description
            delay: 200
            timeout: 2000
        }

        Text {
            id: amtText
            text: "You have " + model.item.amount + " " + model.item.getName()
            width: root.largestTextWidth + 10
            color: Theme.onSurface
            font.pixelSize: 18
            verticalAlignment: Text.AlignVCenter
            anchors.left: parent.left

            Behavior on color {
                ColorAnimation {
                    easing.type: Easing.InOutQuad
                    duration: 200
                }
            }

            TextMetrics {
                id: metrics
                text: amtText.text
                font: amtText.font
            }

            Component.onCompleted: {
                if (metrics.width > root.largestTextWidth) {
                    root.largestTextWidth = metrics.width
                }
            }
        }


        Kyu.CustomButton {
            id: buyButton

            height: parent.height

            text: ItemGameLogic.parseCost(model.item.name)
            disabledText: ItemGameLogic.parseCost(model.item.name)
            textPixelSize: 18

            enabled: model.item.affordable

            TextMetrics {
                id: bbmetrics
                text: buyButton.text
                font: buyButton.textFont
            }

            width: bbmetrics.advanceWidth + 15

            anchors.leftMargin: 15
            anchors.left: amtText.right

            onClicked: {
                ItemGameLogic.purchase(model.item.name)
            }
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