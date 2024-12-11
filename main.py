import webbrowser

import flet as ft
import flet.map as map
import random


class MapFrame(ft.Container):
    def __init__(self, page: ft.Page, lines):
        super().__init__()

        self.lines = lines

        self.expand = 1
        self.border_radius = ft.border_radius.all(10)

        marker_layer_ref = ft.Ref[map.MarkerLayer]()
        self.circle_layer_ref = ft.Ref[map.CircleLayer]()

        self.pkt = map.MapLatitudeLongitude(50.9476241, 23.1433150)

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

        main_map = map.Map(
                    expand=True,
                    initial_center=map.MapLatitudeLongitude(50.9476241, 23.1433150),
                    initial_zoom=12,
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
                            # url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                            url_template="https://mt1.google.com/vt/lyrs=s&hl=pl&x={x}&y={y}&z={z}",
                            # url_template="./{z}/{x}/{y}.jpg",
                            # url_template="http://localhost:8000/{z}/{x}/{y}.jpg",
                            on_image_error=lambda e: print("TileLayer Error"),
                        ),
                        map.RichAttribution(
                            attributions=[
                                map.TextSourceAttribution(
                                    text="OpenStreetMap Contributors",
                                    on_click=lambda e: e.page.launch_url(
                                        "https://openstreetmap.org/copyright"
                                    ),
                                ),
                                map.TextSourceAttribution(
                                    text="Flet",
                                    on_click=lambda e: e.page.launch_url("https://flet.dev"),
                                ),
                            ]
                        ),
                        map.SimpleAttribution(
                            text="Flet",
                            alignment=ft.alignment.top_right,
                            on_click=lambda e: print("Clicked SimpleAttribution"),
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
                        map.PolygonLayer(
                            polygons=[
                                map.PolygonMarker(
                                    label="Popular Touristic Area",
                                    label_text_style=ft.TextStyle(
                                        color=ft.Colors.BLACK,
                                        size=15,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    color=ft.Colors.with_opacity(0.3, ft.Colors.BLUE),
                                    coordinates=[
                                        map.MapLatitudeLongitude(10, 10),
                                        map.MapLatitudeLongitude(30, 15),
                                        map.MapLatitudeLongitude(25, 45),
                                    ],
                                ),
                            ],
                        ),
                        map.PolylineLayer(
                            polylines=[
                                map.PolylineMarker(
                                    border_stroke_width=3,
                                    border_color=ft.Colors.RED,
                                    gradient_colors=[ft.Colors.BLACK, ft.Colors.BLACK],
                                    color=ft.Colors.with_opacity(0.6, ft.Colors.GREEN),
                                    coordinates=[
                                        map.MapLatitudeLongitude(10, 10),
                                        map.MapLatitudeLongitude(30, 15),
                                        map.MapLatitudeLongitude(25, 45),
                                    ],
                                ),
                            ],
                        ),
                    ],
                )
        map_row = ft.Row([
            # label,
            # main_map
        ])

        self.content=map_row

        def elBtn_click(e):
            url = f"https://www.google.pl/maps/place/{self.pkt.latitude:.5f},{self.pkt.longitude:.5f}"
            try:
                webbrowser.open(url)
            except Exception as er:
                page.launch_url(url)


        elBtn = ft.ElevatedButton("Nawiguj", on_click=lambda e: elBtn_click(e))

        self.content = ft.Stack(controls=[main_map,
                                          ft.Row([elBtn], alignment=ft.MainAxisAlignment.CENTER, bottom=5, right=5),
                                          ]
                                , expand=1)


    def clear_layers(self):
        self.circle_layer_ref.current.circles.clear()

    def add_circle(self, lat, lon):
        self.circle_layer_ref.current.circles.append(
            map.CircleMarker(
                radius=5,
                coordinates=map.MapLatitudeLongitude(lat, lon),
                color=ft.Colors.RED,
                border_color=ft.Colors.YELLOW,
                border_stroke_width=3,
            )
        )

        self.page.update()

    def load_values(self, value):



        for line in self.lines:
            spl = line.split("\t")

            if value in spl[0]:

                self.add_circle(float(spl[2]), float(spl[1]))






def main(page: ft.Page):

    # lines = ["a"]

    with open("github.com/Rzezimioszek/WebMapTest2/blob/9445f5ef6688ff60b3acbeecaa78f3c9b2b750f5/assets/punkty.txt", "r") as file:
        lines = file.readlines()

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

    query = ft.TextField(label="Kod dostępu:",
                         col={"xs": 12, "sm": 12, "md": 4})
    submit = ft.ElevatedButton("Wprowadź", on_click= lambda e: submit_on_clik(e),
                               col={"xs": 12, "sm": 12, "md": 4})

    mf = MapFrame(page, lines)
    #mf.visible = False
    # main_row.controls.append(mf)

    page.add(ft.ResponsiveRow([label, query, submit], alignment=ft.MainAxisAlignment.CENTER))
    page.add(mf)

    page.update()

if __name__ == "__main__":
    site = ft.app(main, view=ft.AppView.WEB_BROWSER, assets_dir="assets")