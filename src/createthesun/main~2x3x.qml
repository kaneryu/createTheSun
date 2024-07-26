import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Qt.labs.platform
import "./qml/" as Kyu
import CreateTheSun 1.0



ApplicationWindow {
    id: root
    visible: true
    minimumWidth: 640
    minimumHeight: 480

    title: "Create The Sun"
    property QtObject tabsModel // absract list model from python -- contains tabs
    
    Connections {
        target: Backend

        function onModelChanged(model) {
            mainModel = model
        }
        

        function onLoadComplete() {}
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
            anchors.fill: parent
            orientation: ListView.Horizontal

            spacing: 2

            delegate: Rectangle {
                id: rect
                topRightRadius: 10/2
                topLeftRadius: 10/2

                width: metrics.width + 10
                height: 43 / 2

                color: (Backend.activeTab == model.name) ? Theme.primaryContainer : Theme.secondaryContainer

                border.color: (Backend.activeTab == model.name) ? Theme.primaryFixedDim : Theme.secondaryFixedDim
                border.width: 1/2

                Text {
                    id: tabText
                    text: model.name
                    color: (Backend.activeTab == model.name) ? Theme.onPrimaryContainer : Theme.onPrimaryContainer
                    font.pixelSize: 18
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    anchors.fill: parent

                    Behavior on color {
                        ColorAnimation {
                            easing: Easing.InOutQuad
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
                    onClicked: Backend.activeTab = model.name
                }

                Behavior on color {
                    ColorAnimation {
                        easing: Easing.InOutQuad
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
                sourceComponent: Backend.activeTabComponent
            }
        }
    }
}