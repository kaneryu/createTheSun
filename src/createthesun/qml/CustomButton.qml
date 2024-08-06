import QtQml
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Qt.labs.platform

import "." as Kyu

Item {
    id: root

    property bool enabled: true

    property string hoverBorderColor
    property string borderColor
    property string clickedBorderColor
    property string disabledBorderColor

    property real hoverBorderWidth
    property real borderWidth
    property real clickedBorderWidth
    property real disabledBorderWidth

    property string hoverFillColor
    property string fillColor
    property string clickedFillColor
    property string disabledFillColor

    property string hoverTextColor
    property string textColor
    property string clickedTextColor
    property string disabledTextColor

    property real hoverRadius
    property real radius
    property real clickedRadius
    property real disabledRadius

    property string hoverText
    property string text
    property string clickedText
    property string disabledText
    
    property alias textPixelSize: txt.font.pixelSize

    signal clicked()

    onEnabledChanged: {
        if (!enabled) {
            fill.color = (disabledFillColor !== undefined && disabledFillColor !== null) ? disabledFillColor : fillColor
            fill.border.color = (disabledBorderColor !== undefined && disabledBorderColor !== null) ? disabledBorderColor : borderColor
            fill.border.width = (disabledBorderWidth !== undefined && disabledBorderWidth !== null) ? disabledBorderWidth : borderWidth
            txt.color = (disabledTextColor !== undefined && disabledTextColor !== null) ? disabledTextColor : textColor
            fill.radius = (disabledRadius !== undefined && disabledRadius !== null) ? disabledRadius : radius
            txt.text = (disabledText !== undefined && disabledText !== null) ? disabledText : text
        }
    }

    Rectangle {
        id: fill
        anchors.fill: parent
        color: fillColor
        border.color: borderColor
        border.width: borderWidth
        radius: root.radius

        Behavior on color {
            ColorAnimation {
                easing.type: Easing.InOutQuad
                duration: 200
            }
        }

        Behavior on border.color {
            ColorAnimation {
                easing.type: Easing.InOutQuad
                duration: 200
            }
        }

        Behavior on border.width {
            NumberAnimation {
                easing.type: Easing.InOutQuad
                duration: 200
            }
        }

        Behavior on radius {
            NumberAnimation {
                easing.type: Easing.InOutQuad
                duration: 200
            }
        }

        Text {
            id: txt
            text: root.text
            color: textColor
            anchors.centerIn: parent
            font.pixelSize: 24
        }
    }

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: true


        function hoverColorSetter() {
            if (!root.enabled) {
                return
            }
            fill.color = (hoverFillColor !== undefined && hoverFillColor !== null) ? hoverFillColor : fillColor
            fill.border.color = (hoverBorderColor !== undefined && hoverBorderColor !== null) ? hoverBorderColor : borderColor
            fill.border.width = (hoverBorderWidth !== undefined && hoverBorderWidth !== null) ? hoverBorderWidth : borderWidth
            txt.color = (hoverTextColor !== undefined && hoverTextColor !== null) ? hoverTextColor : textColor
            fill.radius = (hoverRadius !== undefined && hoverRadius !== null) ? hoverRadius : radius
        }
        function exitColorSetter() {
            if (!root.enabled) {
                return
            }
            fill.color = fillColor
            fill.border.color = borderColor
            fill.border.width = borderWidth
            txt.color = textColor
            fill.radius = radius
        }


        onPressed: {
            if (!root.enabled) {
                return
            }
            fill.color = (clickedFillColor !== undefined && clickedFillColor !== null) ? clickedFillColor : fillColor
            fill.border.color = (clickedBorderColor !== undefined && clickedBorderColor !== null) ? clickedBorderColor : borderColor
            fill.border.width = (clickedBorderWidth !== undefined && clickedBorderWidth !== null) ? clickedBorderWidth : borderWidth
            txt.color = (clickedTextColor !== undefined && clickedTextColor !== null) ? clickedTextColor : textColor
            fill.radius = (clickedRadius !== undefined && clickedRadius !== null) ? clickedRadius : radius
        }

        onReleased: {
            if (!root.enabled) {
                return
            }
            fill.color = (hoverFillColor !== undefined && hoverFillColor !== null) ? hoverFillColor : fillColor
            fill.border.color = (hoverBorderColor !== undefined && hoverBorderColor !== null) ? hoverBorderColor : borderColor
            fill.border.width = (hoverBorderWidth !== undefined && hoverBorderWidth !== null) ? hoverBorderWidth : borderWidth
            txt.color = (hoverTextColor !== undefined && hoverTextColor !== null) ? hoverTextColor : textColor
            fill.radius = (hoverRadius !== undefined && hoverRadius !== null) ? hoverRadius : radius
        }

        onClicked: {
            if (!root.enabled) {
                return
            }
            root.clicked()
        }


        onEntered: {
            hoverColorSetter()
        }

        onExited: {
            exitColorSetter()
        }
    }
}