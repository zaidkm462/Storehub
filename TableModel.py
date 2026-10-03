from PyQt6.QtCore import QAbstractTableModel, Qt

class TableModel(QAbstractTableModel):
    def __init__(self, data, headers, rc, cc, window):
        super().__init__()
        self.window = window
        self._data = data
        self.k = 'الكل'
        self.rc = rc
        self.cc = cc
        self._headers = headers


    def rowCount(self, parent=None):
        #print('hiii')
        return self.rc
        #return len(self._data)

    def columnCount(self, parent=None):
        return self.cc

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
            #print(self._data['الكل'][index.row()])
            #print(self._data['الكل'][index.row()])

            #print(self._data[self.k][index.row()], len(self._data['e']))
            return self._data['e'][self._data[self.k][index.row()]][index.column()]
            #x = self._data[self.b][index.row()]
            #y = index.column()
            #print(str(x)+"--"+ str(y))
            #return self._data['الكل'][self._data[self.b][index.row()]][index.column()]
            #return self._data[index.row()][index.column()]
        elif role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignCenter
        return None

    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        if role == Qt.ItemDataRole.EditRole:
            self._data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index, [Qt.ItemDataRole.EditRole])
            return True
        return False

    def flags(self, index):
        if index.row() == 0 and not self.window.x and self.window.clasfLstVu.currentRow() > -1:
            return Qt.ItemFlag.ItemIsEnabled
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                if section < len(self._headers):
                    return self._headers[section]
            if orientation == Qt.Orientation.Vertical:
                return f"{section + 1}"
        return None
