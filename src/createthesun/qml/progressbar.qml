// import QtQuick
// import QtQuick.Controls
// import QtQuick.Layouts
// import QtQuick.Shapes

// Item {
//     id: root
    
//     width: 50
//     height: 100
       
//     anchors.horizontalCenter: parent.horizontalCenter
//     anchors.verticalCenter: parent.verticalCenter
    
    
//     property real percent: 50
//     property bool vertical: true

//     property alias fillColor: fill.color
//     property alias backgroundColor: background.color

//     property alias radius: background.radius

//     property alias border: background.border
    
//     fillColor: red
//     backgroundColor: transparent
      
//     Rectangle {
//         id: background
//         clip: true
//         anchors.fill: parent
        
//         Rectangle {
//             id: fill
//             width: (root.vertical) ? parent.width : parent.width * (root.percent / 100)
//             height: (root.vertical) ? parent.height * (root.percent / 100) : parent.height
            
            
//             anchors.bottom: parent.bottom
//             color: "red"
            
//         }
//     }

//     Item {
//         anchors.centerIn: parent
//         id: radii
//         width: background.width
//         height: background.height
//         property string color: 'transparent'
//         property int rightTopCornerRadius: 5
//         property int rightBottomCornerRadius: 5
//         property int leftBottomCornerRadius: 5
//         property int leftTopCornerRadius: 5
//     }

// }

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
    property bool vertical: false

    property alias fillColor: fill.color
    property alias backgroundColor: background.color

    property alias radius: background.radius

    property alias border: background.border
    
    Behavior on percent {
        NumberAnimation {
            duration: 100
        }
    }
    Rectangle {
        id: background
        clip: true
        anchors.fill: parent
        
        Rectangle {
            id: fill
            width: (root.vertical) ? parent.width : parent.width * (root.percent / 100)
            height: (root.vertical) ? parent.height * (root.percent / 100) : parent.height
            
            
            anchors.bottom: parent.bottom
            color: "red"
            
        }
    }
}
