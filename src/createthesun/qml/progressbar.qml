import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Shapes

Item {
    id: root
    
    width: 50
    height: 100
       
    anchors.horizontalCenter: parent.horizontalCenter
    anchors.verticalCenter: parent.verticalCenter
    
    
    property real percent: 50
    property bool vertical: true

    property alias fillColor: fill.color
    property alias backgroundColor: background.color

    property alias radius: background.radius

    property alias border: background.border
    
    fillColor: red
    backgroundColor: transparent
      
    Rectangle {
        id: background
        clip: true
        anchors.fill: parent
        
        containmentMask: mask
        
        Shape {
            id: mask
            
            containsMode: shape.fillContains
            ShapePath {
                strokeWidth: 5
                strokeColor: radii.color
                startX: radii.leftTopCornerRadius > 0 ? radii.leftTopCornerRadius : 0
                startY: 0
                fillColor: "transparent"
                capStyle: ShapePath.RoundCap
                fillRule: ShapePath.WindingFill

                PathLine { y: 0; x:radii.width - radii.rightTopCornerRadius}
                PathArc {
                    x: radii.width; y: radii.rightTopCornerRadius
                    radiusX: radii.rightTopCornerRadius; radiusY: radii.rightTopCornerRadius

                }

                PathLine { x:radii.width; y:radii.height - radii.rightBottomCornerRadius}
                PathArc {
                    x:radii.width - radii.rightBottomCornerRadius; y: radii.height
                    radiusX: radii.rightBottomCornerRadius; radiusY: radii.rightBottomCornerRadius
                }

                PathLine { x:radii.leftBottomCornerRadius; y:radii.height}
                PathArc {
                    x:0; y: radii.height - radii.leftBottomCornerRadius
                    radiusX: radii.leftBottomCornerRadius; radiusY: radii.leftBottomCornerRadius
                }

                PathLine { x:0; y:radii.leftTopCornerRadius}
                PathArc {
                    x:radii.leftTopCornerRadius; y: 0
                    radiusX: radii.leftTopCornerRadius; radiusY: radii.leftTopCornerRadius
                }
            }
        }
        
        Rectangle {
            id: fill
            width: (root.vertical) ? parent.width : parent.width * (root.percent / 100)
            height: (root.vertical) ? parent.height * (root.percent / 100) : parent.height
            
            
            anchors.bottom: parent.bottom
            color: "red"
            
        }
    }

    Item {
        anchors.centerIn: parent
        id: radii
        width: background.width
        height: background.height
        property string color: 'transparent'
        property int rightTopCornerRadius: 5
        property int rightBottomCornerRadius: 5
        property int leftBottomCornerRadius: 5
        property int leftTopCornerRadius: 5
    }

}
