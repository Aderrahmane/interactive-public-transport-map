import sys
from PyQt5 import QtGui, QtCore, QtWidgets
import psycopg2
from PyQt5.QtWidgets import QComboBox, QApplication, QCompleter, QLineEdit, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QPushButton, QSplitter
import folium, io, json
from folium.plugins import Draw
from jinja2 import Template
from branca.element import Element
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.resize(600, 600)

        main = QWidget()
        self.setCentralWidget(main)
        main.setLayout(QVBoxLayout())
        main.setFocusPolicy(QtCore.Qt.StrongFocus)

        self.tableWidget = QTableWidget()
        self.tableWidget.doubleClicked.connect(self.table_Click)
        self.rows = []

        self.webView = myWebView(self)

        controls_panel = QHBoxLayout()
        mysplit = QSplitter(QtCore.Qt.Vertical)
        mysplit.addWidget(self.tableWidget)
        mysplit.addWidget(self.webView)

        main.layout().addLayout(controls_panel)
        main.layout().addWidget(mysplit)

        _label = QtWidgets.QLabel('From: ', self)
        _label.setFixedSize(50, 20)
        self.from_box = QtWidgets.QComboBox()
        self.from_box.setEditable(True)
        self.from_box.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.from_box.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        controls_panel.addWidget(_label)
        controls_panel.addWidget(self.from_box)

        _label = QtWidgets.QLabel('  To: ', self)
        _label.setFixedSize(40, 20)
        self.to_box = QtWidgets.QComboBox()
        self.to_box.setEditable(True)
        self.to_box.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.to_box.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        controls_panel.addWidget(_label)
        controls_panel.addWidget(self.to_box)

        # List of transportation choices
        transportation_choices = ["Tram", "Subway", "Rail", "Bus", "Walk"]
        self.transport_box = QtWidgets.QComboBox()
        self.transport_box.addItems(transportation_choices)
        controls_panel.addWidget(self.transport_box)

        # Line edit for custom query input
        self.custom_query_edit = QLineEdit()
        controls_panel.addWidget(self.custom_query_edit)

        self.go_button = QtWidgets.QPushButton("Go!")
        self.go_button.clicked.connect(self.button_Go)
        controls_panel.addWidget(self.go_button)

        self.connect_DB()

        self.startingpoint = True  # Initialize the attribute

        self.show()

    def connect_DB(self):
        # You have to replace these connection parameters(info do connexion) with your actual database credentials
        self.conn = psycopg2.connect(database="l3info_40", user="l3info_40", host="10.11.11.22", password="L3INFO_40")
        self.cursor = self.conn.cursor()

        self.cursor.execute("""SELECT distinct name FROM table_stops1 ORDER BY name""")
        self.conn.commit()
        rows = self.cursor.fetchall()

        for row in rows:
            self.from_box.addItem(str(row[0]))
            self.to_box.addItem(str(row[0]))

    def table_Click(self):
        # Your table click handling code here
        pass

    def button_Go(self):
        _fromstation = str(self.from_box.currentText())
        _tostation = str(self.to_box.currentText())
        _transport = str(self.transport_box.currentText())
        _custom_query = str(self.custom_query_edit.text())

        rows = self.execute_query(_fromstation, _tostation, _transport, _custom_query)
        self.display_results(rows)

    def execute_query(self, _fromstation, _tostation, _transport, _custom_query):
        rows = []

        # Use the custom query if provided, else use the default query
        if _custom_query:
            query = _custom_query
        else:
            # Modify the query based on the selected transport
            if _transport == "Tram":
                query = f"SELECT distinct tram_2.from_stop, tram_2.route_name, tram_2.to_stop ,tram_2.duration_avg FROM tram_2 WHERE tram_2.from_stop = $${_fromstation}$$ AND tram_2.to_stop = $${_tostation}$$ "
            elif _transport == "Subway":
                query = f"SELECT distinct subway_2.from_stop, subway_2.route_name, subway_2.to_stop ,subway_2.duration_avg FROM subway_2 WHERE subway_2.from_stop = $${_fromstation}$$ AND subway_2.to_stop = $${_tostation}$$ "
            elif _transport == "Rail":
                query = f"SELECT distinct rail_2.from_stop, rail_2.route_name, rail_2.to_stop ,rail_2.duration_avg FROM rail_2 WHERE rail_2.from_stop = $${_fromstation}$$ AND rail_2.to_stop = $${_tostation}$$ "
            elif _transport == "Bus":
                query = f"SELECT distinct bus_2.from_stop, bus_2.route_name, bus_2.to_stop ,bus_2.duration_avg FROM bus_2 WHERE bus_2.from_stop = $${_fromstation}$$ AND bus_2.to_stop = $${_tostation}$$ "
            elif _transport == "Walk":
                query = f"SELECT distinct walk_2.from_stop,  walk_2.to_stop  FROM walk_2 WHERE walk_2.from_stop = $${_fromstation}$$ AND walk_2.to_stop = $${_tostation}$$ "
            else:
                query = ""

        # Execute the query
        self.cursor.execute(query)
        self.conn.commit()
        rows += self.cursor.fetchall()

        return rows

    def display_results(self, rows):
        if len(rows) == 0:
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(0)
            return

        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setColumnCount(len(rows[-1]))

        i = 0
        for row in rows:
            j = 0
            for col in row:
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(col)))
                j += 1
            i += 1

        header = self.tableWidget.horizontalHeader()
        j = 0
        while j < len(rows[-1]):
            header.setSectionResizeMode(j, QtWidgets.QHeaderView.ResizeToContents)
            j += 1

        self.update()

    def mouseClick(self, lat, lng):
        self.webView.addPointMarker(lat, lng)

        print(f"Clicked on: latitude {lat}, longitude {lng}")
        self.cursor.execute(f" WITH mytable (distance, name) AS (SELECT ( ABS(stops_table.lat-{lat}) + ABS(stops_table.lng-{lng}) ), name FROM stops_table) SELECT A.name FROM mytable as A WHERE A.distance <=  (SELECT min(B.distance) FROM mytable as B)")
        self.conn.commit()
        rows = self.cursor.fetchall()
        # print('Closest STATION is: ', rows[0][0])
        if self.startingpoint:
            self.from_box.setCurrentIndex(self.from_box.findText(rows[0][0], QtCore.Qt.MatchFixedString))
        else:
            self.to_box.setCurrentIndex(self.to_box.findText(rows[0][0], QtCore.Qt.MatchFixedString))
        self.startingpoint = not self.startingpoint

class myWebView(QWebEngineView):
    def __init__(self, main_window):
        super().__init__()

        self.maptypes = ["OpenStreetMap", "Stamen Terrain", "stamentoner", "cartodbpositron"]
        self.setMap(0)
        self.main_window = main_window

    def add_customjs(self, map_object):
        my_js = f"""{map_object.get_name()}.on("click",
                 function (e) {{
                    var data = `{{"coordinates": ${{JSON.stringify(e.latlng)}}}}`;
                    console.log(data)}}); """
        e = Element(my_js)
        html = map_object.get_root()
        html.script.get_root().render()
        html.script._children[e.get_name()] = e

        return map_object

    def handleClick(self, msg):
        data = json.loads(msg)
        lat = data['coordinates']['lat']
        lng = data['coordinates']['lng']

        self.main_window.mouseClick(lat, lng)

    def addSegment(self, lat1, lng1, lat2, lng2):
        js = Template(
            """
            L.polyline(
                [ [{{latitude1}}, {{longitude1}}], [{{latitude2}}, {{longitude2}}] ], {
                    "color": "red",
                    "opacity": 1.0,
                    "weight": 4,
                    "line_cap": "butt"
                }
            ).addTo({{map}});
            """
        ).render(map=self.mymap.get_name(), latitude1=lat1, longitude1=lng1, latitude2=lat2, longitude2=lng2)

        self.page().runJavaScript(js)

    def addMarker(self, lat, lng):
        js = Template(
            """
            L.marker([{{latitude}}, {{longitude}}] ).addTo({{map}});
            L.circleMarker(
                [{{latitude}}, {{longitude}}], {
                    "bubblingMouseEvents": true,
                    "color": "#3388ff",
                    "popup": "hello",
                    "dashArray": null,
                    "dashOffset": null,
                    "fill": false,
                    "fillColor": "#3388ff",
                    "fillOpacity": 0.2,
                    "fillRule": "evenodd",
                    "lineCap": "round",
                    "lineJoin": "round",
                    "opacity": 1.0,
                    "radius": 2,
                    "stroke": true,
                    "weight": 5
                }
            ).addTo({{map}});
            """
        ).render(map=self.mymap.get_name(), latitude=lat, longitude=lng)
        self.page().runJavaScript(js)

    def addPointMarker(self, lat, lng):
        js = Template(
            """
            L.circleMarker(
                [{{latitude}}, {{longitude}}], {
                    "bubblingMouseEvents": true,
                    "color": 'green',
                    "popup": "hello",
                    "dashArray": null,
                    "dashOffset": null,
                    "fill": false,
                    "fillColor": 'green',
                    "fillOpacity": 0.2,
                    "fillRule": "evenodd",
                    "lineCap": "round",
                    "lineJoin": "round",
                    "opacity": 1.0,
                    "radius": 2,
                    "stroke": true,
                    "weight": 5
                }
            ).addTo({{map}});
            """
        ).render(map=self.mymap.get_name(), latitude=lat, longitude=lng)
        self.page().runJavaScript(js)

    def setMap(self, i):
        self.mymap = folium.Map(location=[48.8619, 2.3519], tiles=self.maptypes[i], zoom_start=12, prefer_canvas=True)

        self.mymap = self.add_customjs(self.mymap)

        page = WebEnginePage(self)
        self.setPage(page)

        data = io.BytesIO()
        self.mymap.save(data, close_file=False)

        self.setHtml(data.getvalue().decode())

    def clearMap(self, index):
        self.setMap(index)

class WebEnginePage(QWebEnginePage):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def javaScriptConsoleMessage(self, level, msg, line, sourceID):
        # print(msg)
        if 'coordinates' in msg:
            self.parent.handleClick(msg)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
