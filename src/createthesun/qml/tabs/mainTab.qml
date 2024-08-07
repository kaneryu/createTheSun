import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Qt.labs.platform

import ".." as Kyu

Item {
    id: root

    property real largestTextWidth

    anchors.fill: parent

    ListView {
    id: tabBar
    model: ItemsModel
    
    anchors.fill: parent

    orientation: ListView.Vertical
    
    spacing: 2
    
    delegate: Rectangle {
        id: rect

        width: parent.width
        height: 55 / 2

        color: Theme.surface

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
                font: buyButton.txt.font
            }

            width: (bbmetrics.advanceWidth * 1.2) + 15

            anchors.leftMargin: 15
            anchors.left: amtText.right

            radius: 5
            hoverRadius: 10
            clickedRadius: 0

            onClicked: {
                ItemGameLogic.purchase(model.item.name)
            }

            fillColor: Theme.primaryContainer
            hoverFillColor: Theme.primaryFixedDim
            clickedFillColor: Theme.primaryFixed
            disabledFillColor: Theme.secondaryContainer

            borderColor: Theme.primaryFixed
            disabledBorderColor: Theme.secondaryFixed

            borderWidth: 1
            disabledBorderWidth: 1


            textColor: Theme.onPrimaryContainer
            hoverTextColor: Theme.onPrimaryFixedDim
            clickedTextColor: Theme.onPrimaryFixed
            disabledTextColor: Theme.onSecondaryContainer

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