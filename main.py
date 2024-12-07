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
                    initial_center=map.MapLatitudeLongitude(15, 10),
                    initial_zoom=4.2,
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
                                    coordinates=map.MapLatitudeLongitude(30, 15),
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
                                    coordinates=map.MapLatitudeLongitude(16, 24),
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


    main_row = ft.Column(alignment=ft.MainAxisAlignment.START)
    label = ft.Text("Aqq")
    # main_row.controls.append(label)

    def submit_on_clik(e):
        mf.visible = not mf.visible
        if int(query.value):
            value.value=str(int(value.value) + int(query.value))
        page.update()

    query = ft.TextField(label="Kod dostępu:")
    submit = ft.ElevatedButton("Wprowadź", on_click= lambda e: submit_on_clik(e))
    value = ft.Text("0")
    try:
        mf = MapFrame(page)
    except Exception as er:
        page.add(ft.Text(str(er)))
        page.update()
    mf.visible = False
    # main_row.controls.append(mf)

    page.add(ft.Row([query, submit, value], alignment=ft.MainAxisAlignment.CENTER))
    page.add(mf)

    page.update()

if __name__ == "__main__":
    site = ft.app(main, view=ft.AppView.WEB_BROWSER)