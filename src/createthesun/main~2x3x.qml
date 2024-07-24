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
    property QtObject mainModel // absract list model from python
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

}