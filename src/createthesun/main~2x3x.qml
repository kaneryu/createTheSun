import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Qt.labs.platform
import "./qml/" as Kyu



ApplicationWindow {
    id: root
    visible: true
    minimumWidth: 640
    minimumHeight: 480

    title: "Create The Sun"
    property QtObject tabsModel // absract list model from python -- contains tabs
    property QtObject backend
    property QtObject theme
    
    Connections {
        target: backend

        function onModelChanged(model) {
            mainModel = model
        }
        

        function onLoadComplete() {}
        onUpdateTheme: {
            background.color = theme.getColor("background")
            headertext.color = theme.getColor("primary")
        }
    }

    
    background: Rectangle {
        id: background
    }
    
    header: Text {
        id: headertext
        text: root.title
        font.pixelSize: 24

        
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
    }

    ListView {
        id: tabBar
        model: root.tabsModel
        anchors.fill: parent
        layoutDirection: Qt.LeftToRight

        spacing: 10 / 2

        delegate: Item {
            width: 100
            height: 50
            Rectangle {
                
                topRightRadius: 10
                topLeftRadius: 10

                width: 149 / 2
                height: 43 / 2

                color: theme.getColor("primaryContainer")

                border.color: theme.getColor("primaryFixedDim")
                border.width: 1/2
                Text {
                    text: model.name
                }
            }
        }
    }

}