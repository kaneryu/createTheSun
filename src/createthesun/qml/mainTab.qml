import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Qt.labs.platform

Item {
    id: mainTab
    property QtObject mainModel // absract list model from python
    property QtObject backend
    property QtObject theme

    Connections {
        target: backend

        function onModelChanged(model) {
            mainModel = model
        }

        function onLoadComplete() {}
    }
}