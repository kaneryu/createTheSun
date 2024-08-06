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

        Text {
            id: amtText
            text: "You have " + model.item.amount + " " + model.item.getName()
            width: root.largestTextWidth + 10
            color: Theme.onSurface
            font.pixelSize: 36 / 2
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

            text: "Purchase 0 " + model.item.getName() + " for " + model.item.cost + " ..." // in the future you will call a function to get the cost text
            disabledText: "(Can't Afford)"
            textPixelSize: 36 / 2
            
            Component.onCompleted: {
                if (model.item.name != "Quarks") {
                    buyButton.enabled = false
                }
            }

            TextMetrics {
                id: bbmetrics
                text: buyButton.text
                font: buyButton.txt.font
            }

            width: bbmetrics.width + 50

            anchors.leftMargin: 15
            anchors.left: amtText.right

            radius: 5
            hoverRadius: 10
            clickedRadius: 0

            onClicked: {
                Backend.buyItem(model.item.name)
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