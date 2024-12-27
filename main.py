import webbrowser

import flet as ft
import flet.map as map
import random

import requests

class PointButton(ft.TextButton):
    def __init__(self, page: ft.Page, lines):
        super().__init__()

class MapFrame(ft.Container):
    def __init__(self, page: ft.Page, lines, kody):
        super().__init__()

        self.lines = lines
        self.kody = kody

        self.expand = 1
        self.border_radius = ft.border_radius.all(10)
        self.bgcolor = ft.colors.WHITE
        # self.col=12

        marker_layer_ref = ft.Ref[map.MarkerLayer]()
        self.circle_layer_ref = ft.Ref[map.CircleLayer]()
        self.label_ref = ft.Ref[map.MarkerLayer]()

        self.pkt = map.MapLatitudeLongitude(50.4717587,19.3718856),

        def handle_tap(e: map.MapTapEvent):
            print(e)
            if e.name == "tap":
                #webbrowser.open("https://bitly.com/")

                self.pkt = e.coordinates

                marker_layer_ref.current.markers.clear()
                marker_layer_ref.current.markers.append(
                        map.Marker(
                            content=ft.Icon(
                                ft.Icons.LOCATION_ON, color=ft.cupertino_colors.DESTRUCTIVE_RED
                            ),
                            coordinates=e.coordinates,
                        )
                    )

            # webbrowser.open(f"https://www.google.pl/maps/place/{e.coordinates.latitude:.5f},{e.coordinates.longitude:.5f}")
            page.update()

        def handle_event(e: map.MapEvent):
            print(e)



        label = ft.Container(content=ft.Row(
                                      [ft.Text("Click anywhere to add a Marker, right-click to add a CircleMarker.")]
        ),
            border_radius=ft.border_radius.all(10),
                          bgcolor=ft.colors.with_opacity(0.6, ft.colors.PRIMARY_CONTAINER),
                          padding=5,
                          blur=15)

        self.main_map = map.Map(
                    expand=True,
                    initial_center=map.MapLatitudeLongitude(50.4717587,19.3718856),
                    initial_zoom=13,
                    interaction_configuration=map.MapInteractionConfiguration(
                        flags=map.MapInteractiveFlag.ALL
                    ),
                    on_init=lambda e: print(f"Initialized Map"),
                    on_tap=lambda e: handle_tap(e),
                    on_secondary_tap=lambda e: handle_tap(e),
                    on_long_press=lambda e: handle_tap(e),
                    on_event=lambda e: print(e),
                    layers=[
                        map.TileLayer(
                            #max_zoom=16,
                            min_zoom=10,
                            # url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                            #url_template="https://mt1.google.com/vt/lyrs=s&hl=pl&x={x}&y={y}&z={z}",
                            # url_template="./{z}/{x}/{y}.jpg",
                            #url_template="https://raw.githack.com/Rzezimioszek/WebMapTest/main/{z}/{x}/{y}.png",
                            #url_template="https://raw.githack.com/Rzezimioszek/WebMapTest/main/{z}/{x}/{y}.jpg",
                            # url_template="https://raw.githack.com/Rzezimioszek/Files/main/ortofotomapa/S17K/{z}/{x}/{y}.jpg",
                            url_template="https://raw.githack.com/Rzezimioszek/Files/main/ortofotomapa/DK78/{z}/{x}/{y}.jpg",
                            #url_template="https://raw.githack.com/Rzezimioszek/Files/main/ortofotomapa/S17K2/{z}/{x}/{y}.jpg",
                            on_image_error=lambda e: print("TileLayer Error"),
                            pan_buffer=1,
                        ),
                        map.MarkerLayer(
                            ref=marker_layer_ref,
                            markers=[
                                map.Marker(
                                    content=ft.Icon(ft.Icons.LOCATION_ON),
                                    coordinates=map.MapLatitudeLongitude(50.9476241,23.1433150),
                                ),
                            ],
                        ),
                        map.MarkerLayer(
                            ref=self.label_ref,
                            markers=[],
                        ),
                        map.CircleLayer(
                            ref=self.circle_layer_ref,
                            circles=[
                                map.CircleMarker(
                                    radius=10,
                                    coordinates=map.MapLatitudeLongitude(10,10),
                                    color=ft.Colors.RED,
                                    border_color=ft.Colors.BLUE,
                                    border_stroke_width=4,
                                ),
                            ],
                        ),
                    ],
                )
        map_row = ft.Row([
            # label,
            # main_map
        ])

        # self.content=map_row

        def elBtn_click(e):
            url = f"https://www.google.pl/maps/place/{self.pkt.latitude:.5f},{self.pkt.longitude:.5f}"
            try:
                webbrowser.open(url)
            except Exception as er:
                page.launch_url(url)


        elBtn = ft.ElevatedButton("Nawiguj", on_click=lambda e: elBtn_click(e))


        def listBtn_click(e):
            self.listControl.visible = not self.listControl.visible
            self.img_stack.visible = not self.img_stack.visible
            self.main_map.visible = not self.main_map.visible
            if listBtn.text == "Mapa":
                listBtn.text = "Zdjęcia z ziemi"
                listBtn.tooltip = "Pokaż listę punktów"
                zoom_to_allBtn.visible =True

            else:
                listBtn.text = "Mapa"
                listBtn.tooltip = "Pokaż mapę"
                zoom_to_allBtn.visible = False
            page.update()



        listBtn = ft.ElevatedButton("Zdjęcia z ziemi",
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.RED,
                                    on_click=lambda e: listBtn_click(e))

        listBtn.tooltip = "Pokaż listę punktów"

        zoom_to_allBtn = ft.ElevatedButton("Pokaż całą mapę",
                                    on_click=lambda e: self.main_map.move_to(map.MapLatitudeLongitude(50.4717587,19.3718856), 13))

        self.listControl = ft.ListView(
            expand=1,
                                       spacing=5, padding=5)
        # self.listControl.visible = False


        self.image_file = ft.Image(#expand=1,
                               src="https://raw.githack.com/Rzezimioszek/Files/main/ortofotomapa/S17K/18/147891/87921.jpg",
                               fit=ft.ImageFit.FIT_HEIGHT,
                                height=400,
        )

        self.image_label = ft.Text("",
                                   color=ft.Colors.WHITE,
                                   bgcolor=ft.Colors.BLACK,)

        self.img_stack = ft.Stack(controls=[self.image_file,
                                            ft.Container(content=self.image_label, on_click=lambda e:page.launch_url(self.image_file.src), bottom=5, left=5,)
                                            ],
                                  )

        # extras_row = ft.ResponsiveRow([self.listControl, self.image_stack])
        # extras_row.visible = False
        self.listControl.visible = False
        self.img_stack.visible = False


        self.content = ft.Stack(controls=[ft.Column([self.main_map,
                                                     self.img_stack,
                                                     self.listControl,
                                                     ], horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                    alignment=ft.MainAxisAlignment.END
                                                    )
                                                 ,
                                          ft.Column([zoom_to_allBtn, listBtn,
                                                  #elBtn
                                                  ],
                                                 alignment=ft.MainAxisAlignment.CENTER, bottom=5, right=5),

                                          ]
                                , expand=1)


    def clear_layers(self):
        self.circle_layer_ref.current.circles.clear()
        self.label_ref.current.markers.clear()

    def add_circle(self, name_tag,lat, lon):

        new_marker = map.Marker(
            content=ft.Stack([
                ft.Text(
                    spans=[
                        ft.TextSpan(
                            f"{name_tag}",
                            ft.TextStyle(
                                size=12,
                                weight=ft.FontWeight.BOLD,
                                foreground=ft.Paint(
                                color=ft.Colors.BLACK,
                                    stroke_width=2,
                                    stroke_join=ft.StrokeJoin.ROUND,
                                    style=ft.PaintingStyle.STROKE,
                                ),
                            ),
                        ),
                    ],
                    text_align=ft.TextAlign.LEFT
                ),
                ft.Text(
                    value=f"{name_tag}",
                    # bgcolor=ft.colors.with_opacity(0.2, ft.colors.WHITE),
                    color=ft.Colors.WHITE,
                    size=12,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.LEFT
                ),
            ],),
            alignment=ft.alignment.top_right,
            width=70,
            coordinates=map.MapLatitudeLongitude(lat, lon)
        )

        self.label_ref.current.markers.append(new_marker)

        self.circle_layer_ref.current.circles.append(
            map.CircleMarker(
                radius=3,
                coordinates=map.MapLatitudeLongitude(lat, lon),
                color=ft.Colors.RED,
                border_color=ft.Colors.WHITE,
                border_stroke_width=1,
            )
        )

        self.page.update()

    def point_zoom(self, e):


        spl = str(e.control.text).split(" ")

        try:
            self.image_file.src = f"https://raw.githack.com/Rzezimioszek/Files/main/pliki/graniczniki/{spl[0]}.jpg"
            self.image_label.value = f"{spl[0]}"
        except:
            self.image_file.src = "https://raw.githack.com/Rzezimioszek/Files/main/ortofotomapa/S17K/18/147891/87921.jpg"
            self.image_label.value = ""

        #print(f"click! {e.control.text}")
        #self.main_map.move_to(
        #    destination=map.MapLatitudeLongitude(float(spl[1]), float(spl[2])),
        #    #zoom=19
        #)
        self.page.update()

    def load_values(self, value):

        self.listControl.controls.clear()

        btn = dict()

        i = 0
        #
        lines = []
        plot = ""

        if value == "all":
            for line in self.lines:
                spl = line.split("\t")
                str_btn = f"{spl[-3]} {spl[-1]} {spl[-2]}".replace("\r", "")
                btn[i] = ft.ElevatedButton(str_btn, on_click=lambda e: self.point_zoom(e))
                name_tag = f"{spl[-3]}"

                self.listControl.controls.append(btn[i])
                self.add_circle(name_tag, float(spl[-1]), float(spl[-2]))
                i += 1
            return

        for kod in self.kody:

            if value in kod.split("\t")[0]:
                plot = kod.split("\t")[-1]

                for line in self.lines:


                    spl = line.split("\t")
                    str_btn = f"{spl[-3]} {spl[-1]} {spl[-2]}".replace("\r", "")
                    btn[i] = ft.ElevatedButton(str_btn, on_click=lambda e: self.point_zoom(e))
                    name_tag = f"{spl[-3]}"



                    if plot in spl[0]:

                        self.listControl.controls.append(btn[i])
                        self.add_circle(name_tag, float(spl[-1]), float(spl[-2]))
                        i += 1









def main(page: ft.Page):

    # lines = ["a"]

    #with open("github.com/Rzezimioszek/WebMapTest2/blob/9445f5ef6688ff60b3acbeecaa78f3c9b2b750f5/assets/punkty.txt", "r") as file:
        #lines = file.readlines()

    file = requests.get("https://rzezimioszek.github.io/Files/pliki/punkty.txt").text
    # print(str(file))
    lines = str(file).split("\n")

    file = requests.get("https://rzezimioszek.github.io/Files/pliki/kod-dzialka.txt").text
    print(str(file))
    kody = str(file).split("\n")

    #with open("assets/punkty.txt", "r") as file:
    #with open("punkty.txt", "r") as file:
        #lines = file.readlines()





    label = ft.Text(f"Wprowadź kod otrzymany w zawiadomieniu", # {lines[0]}",
                    col={"xs": 12, "sm": 12, "md": 4})
    # main_row.controls.append(label)

    def submit_on_clik(e):
        #mf.visible = not mf.visible
        mf.clear_layers()
        mf.load_values(query.value)
        #query.value
        page.update()

    query = ft.TextField(label="Wprowadź kod otrzymany w zawiadomieniu",
                         on_submit= lambda e: submit_on_clik(e),
                         height=50,
                         col={"xs": 12, "sm": 12, "md": 3})
    submit = ft.ElevatedButton("Zatwierdz",
                               on_click= lambda e: submit_on_clik(e),
                               height=50,
                               col={"xs": 12, "sm": 12, "md": 1})

    mf = MapFrame(page, lines, kody)
    #mf.visible = False
    # main_row.controls.append(mf)

    page.add(ft.ResponsiveRow([
        # label,
        query,
        submit], alignment=ft.MainAxisAlignment.CENTER))
    page.add(mf)

    page.theme_mode = ft.ThemeMode.LIGHT


    page.update()

if __name__ == "__main__":
    site = ft.app(main, view=ft.AppView.WEB_BROWSER)