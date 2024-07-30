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
    
    Connections {
        target: Backend
    }

    Connections {
        target: Theme
    }


    
    background: Rectangle {
        id: background
        color: Theme.background
    }
    
    header: Text {
        id: headertext
        text: root.title
        font.pixelSize: 24

        color: Theme.primary
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
    }
    
    Item {
        id: content
        anchors.fill: parent
        anchors.top: header.bottom
        anchors.topMargin: 10
        anchors.bottomMargin: 10
        anchors.leftMargin: 10
        anchors.rightMargin: 10

        ListView {
            id: tabBar
            model: root.tabsModel
            
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top

            

            orientation: ListView.Horizontal

            spacing: 2

            delegate: Rectangle {
                id: rect
                topRightRadius: 10/2
                topLeftRadius: 10/2

                width: metrics.width + 10
                height: 43 / 2

                color: (Backend.activeTab == model.name) ? Theme.primaryContainer : Theme.surfaceContainer

                border.color: (Backend.activeTab == model.name) ? Theme.primaryFixedDim : Theme.primaryFixedDim
                border.width: 1/2

                Text {
                    id: tabText
                    text: model.name
                    color: (Backend.activeTab == model.name) ? Theme.onPrimaryContainer : Theme.onSurface
                    font.pixelSize: 18
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    anchors.fill: parent

                    Behavior on color {
                        ColorAnimation {
                            easing.type: Easing.InOutQuad
                            duration: 200
                        }
                    }
                }

                TextMetrics {
                    id: metrics
                    text: tabText.text
                    font: tabText.font
                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: Backend.activeTab = model.internalName
                }

                Behavior on color {
                    ColorAnimation {
                        easing.type: Easing.InOutQuad
                        duration: 200
                    }
                }

            }
        }

        Item {
            id: tabContent
            anchors.top: tabBar.bottom
            anchors.topMargin: 10
            anchors.fill: parent

            Loader {
                id: tabLoader
                anchors.fill: parent
                source: "qml/" + Backend.activeTab + ".qml"
            }
        }
    }
}