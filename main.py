import flet as ft
import flet.map as map
import random


class MapFrame(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()

        self.expand = 1
        self.border_radius = ft.border_radius.all(10)

        marker_layer_ref = ft.Ref[map.MarkerLayer]()
        circle_layer_ref = ft.Ref[map.CircleLayer]()

        def handle_tap(e: map.MapTapEvent):
            print(e)
            if e.name == "tap":
                    marker_layer_ref.current.markers.append(
                        map.Marker(
                            content=ft.Icon(
                                ft.Icons.LOCATION_ON, color=ft.cupertino_colors.DESTRUCTIVE_RED
                            ),
                            coordinates=e.coordinates,
                        )
                    )
            elif e.name == "secondary_tap":
                    circle_layer_ref.current.circles.append(
                        map.CircleMarker(
                            radius=random.randint(5, 10),
                            coordinates=e.coordinates,
                            color=ft.Colors.RED,
                            border_color=ft.Colors.BLUE,
                            border_stroke_width=4,
                        )
                    )
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
                    initial_center=map.MapLatitudeLongitude(50.965125,18.286120),
                    initial_zoom=12,
                    interaction_configuration=map.MapInteractionConfiguration(
                        flags=map.MapInteractiveFlag.ALL
                    ),
                    on_init=lambda e: print(f"Initialized Map"),
                    on_tap=handle_tap,
                    on_secondary_tap=handle_tap,
                    on_long_press=handle_tap,
                    on_event=lambda e: print(e),
                    layers=[
                        map.TileLayer(
                            url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
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
                                    coordinates=map.MapLatitudeLongitude(50.965125,18.286120),
                                ),
                                map.Marker(
                                    content=ft.Icon(ft.Icons.LOCATION_ON),
                                    coordinates=map.MapLatitudeLongitude(10, 10),
                                ),
                                map.Marker(
                                    content=ft.Icon(ft.Icons.LOCATION_ON),
                                    coordinates=map.MapLatitudeLongitude(25, 45),
                                ),
                            ],
                        ),
                        map.CircleLayer(
                            ref=circle_layer_ref,
                            circles=[
                                map.CircleMarker(
                                    radius=10,
                                    coordinates=map.MapLatitudeLongitude(50.965125,18.306120),
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

        self.content = ft.Stack(controls=[main_map,
                                          ft.Row([label], alignment=ft.MainAxisAlignment.END, bottom=5, left=5),
                                          ]
                                , expand=1)



def main(page: ft.Page):

    # lines = ["a"]

    # with open("requirements.txt", "r") as file:
        # lines = file.readlines()



    label = ft.Text(f"Wprowadź kod otrzymany w zawiadomieniu", # {lines[0]}",
                    )
    # main_row.controls.append(label)

    def submit_on_clik(e):
        mf.visible = not mf.visible
        page.update()

    query = ft.TextField(label="Kod dostępu:")
    submit = ft.ElevatedButton("Wprowadź", on_click= lambda e: submit_on_clik(e))

    mf = MapFrame(page)
    #mf.visible = False
    # main_row.controls.append(mf)

    page.add(ft.Row([label, query, submit], alignment=ft.MainAxisAlignment.CENTER))
    page.add(mf)

    page.update()

if __name__ == "__main__":
    site = ft.app(main, view=ft.AppView.WEB_BROWSER)