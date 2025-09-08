import asyncio
import flet as ft


class Shimmer(ft.Container):
    def __init__(
        self,
        ref=None,
        control=None,
        color=None,
        color1=None,
        color2=None,
        height=None,
        width=None,
        auto_generate: bool = False,
    ) -> None:
        super().__init__()

        self.color = color
        self.color1 = color1
        self.color2 = color2
        self.height = height
        self.width = width

        self.ref = ref or ft.Ref[ft.ShaderMask]()

        # Material 3: BACKGROUND -> "surface" (version-safe)
        _BG = getattr(ft.Colors, "BACKGROUND", "surface")

        if self.color1 is None and self.color2 is None and self.color is None:
            self.__color1 = _BG
            self.__color2 = ft.Colors.with_opacity(0.5, _BG)
        elif self.color is not None:
            self.__color1 = self.color
            self.__color2 = ft.Colors.with_opacity(0.5, self.color)
        elif self.color1 is not None and self.color2 is not None:
            self.__color1 = self.color1
            self.__color2 = ft.Colors.with_opacity(0.5, self.color2)

        self.control = self.create_dummy(control) if auto_generate else control

        self.__stop_shine = False
        self.i = -0.1
        self.gap = 0.075

    # ---------- Alignment helpers (version-safe) ----------
    def _align(self, name: str, fallback: "ft.Alignment"):
        """
        Return alignment token by name ('top_left', 'bottom_right', etc.)
        Works with both old ft.alignment.top_left and new ft.Alignment.TOP_LEFT.
        """
        # Old style: ft.alignment.top_left
        align_mod = getattr(ft, "alignment", None)
        if align_mod and hasattr(align_mod, name):
            return getattr(align_mod, name)
        # New style: ft.Alignment.TOP_LEFT
        if hasattr(ft, "Alignment"):
            u = name.upper()
            if hasattr(ft.Alignment, u):
                return getattr(ft.Alignment, u)
        return fallback

    def build(self):
        gradient = ft.LinearGradient(
            colors=[self.__color2, self.__color1, self.__color2],
            stops=[0 + self.i - self.gap, self.i, self.gap + self.i],
            begin=self._align("top_left", ft.Alignment(-1.0, -1.0)),
            end=self._align("bottom_right", ft.Alignment(1.0, 1.0)),
        )

        self.__shadermask = ft.ShaderMask(
            ref=self.ref,
            content=self.control,
            blend_mode=ft.BlendMode.DST_IN,
            height=self.height,
            width=self.width,
            shader=gradient,
        )

        self.content = self.__shadermask
        self.bgcolor = self.__color1

    async def shine_async(self):
        try:
            while self.i <= 5:
                gradient = ft.LinearGradient(
                    colors=[self.__color2, self.__color1, self.__color2],
                    stops=[0 + self.i - self.gap, self.i, self.gap + self.i],
                    begin=self._align("top_left", ft.Alignment(-1.0, -1.0)),
                    end=self._align("bottom_right", ft.Alignment(1.0, 1.0)),
                )
                if self.ref.current:
                    self.ref.current.shader = gradient
                    self.ref.current.update()
                self.i += 0.02
                if self.i >= 1.1:
                    self.i = -0.1
                    await asyncio.sleep(0.4)
                await asyncio.sleep(0.01)
        except Exception:
            pass

    def _control_name(self, target) -> str:
        fn = getattr(target, "_get_control_name", None)
        if callable(fn):
            try:
                return fn()
            except Exception:
                pass
        return target.__class__.__name__.lower()

    def create_dummy(self, target=None):
        opacity = 0.1
        color = ft.Colors.ON_PRIMARY_CONTAINER

        circle = lambda size=60: ft.Container(
            height=size,
            width=size,
            bgcolor=ft.Colors.with_opacity(opacity, color),
            border_radius=size,
        )
        rectangle = lambda height, content=None: ft.Container(
            content=content,
            height=height,
            width=height * 2.5,
            bgcolor=ft.Colors.with_opacity(opacity, color),
            border_radius=20,
            alignment=self._align("bottom_center", ft.Alignment(0.0, 1.0)),
            padding=20,
        )
        tube = lambda width: ft.Container(
            height=10,
            width=width,
            bgcolor=ft.Colors.with_opacity(opacity, color),
            border_radius=20,
            expand=0,
        )

        if target is None:
            target = self.control

        dummy = ft.Container()
        controls = content = title = subtitle = leading = trailing = False

        ctrl_name = self._control_name(target)

        # Best-effort: try to instantiate same control type
        for key in list(ft.__dict__.keys())[::-1]:
            if key.lower() == ctrl_name and key != ctrl_name:
                try:
                    dummy = ft.__dict__[key]()
                except Exception:
                    pass

        # Safe text length read
        try:
            attrs = target.__dict__.get("_Control__attrs", {})
            text_val = attrs.get("value", [""])
            text_len = len(text_val[0]) if text_val and isinstance(text_val[0], str) else 8
        except Exception:
            text_len = 8

        # Skeletons for common controls
        if ctrl_name in ["text"] and getattr(target, "data", None) == "shimmer_load":
            dummy = tube(text_len * 7.5)
        elif ctrl_name in ["textbutton"] and getattr(target, "data", None) == "shimmer_load":
            dummy = rectangle(40)
        elif ctrl_name in ["icon"] and getattr(target, "data", None) == "shimmer_load":
            dummy = circle(30)
        elif ctrl_name in ["image"] and getattr(target, "data", None) == "shimmer_load":
            dummy = ft.Container(bgcolor=ft.Colors.with_opacity(opacity, color), expand=True)
        elif ctrl_name in ["image"]:
            dummy = ft.Container(expand=True)

        # Detect nested props
        for key in list(target.__dict__.keys())[::-1]:
            end = key.lower().split("__")[-1]
            v = target.__dict__[key]
            if end == "controls" and v is not None:
                controls = True
            elif end == "content" and v is not None:
                content = True
            elif end == "title" and v is not None:
                title = True
            elif end == "subtitle" and v is not None:
                subtitle = True
            elif end == "leading" and v is not None:
                leading = True
            elif end == "trailing" and v is not None:
                trailing = True

        # Copy attrs except text/icon/src/color-bearing ones
        ctrl_attrs = target.__dict__.get("_Control__attrs")
        if ctrl_attrs is not None:
            for each_pos in list(ctrl_attrs.keys()):
                if each_pos not in [
                    "text",
                    "value",
                    "label",
                    # old/new image keys (safe across versions)
                    "foregroundimageurl",
                    "backgroundimageurl",
                    "foreground_image_src",
                    "background_image_src",
                    "bgcolor",
                    "name",
                    "color",
                    "icon",
                    "src",
                    "src_base64",
                ]:
                    try:
                        dummy._set_attr(each_pos, ctrl_attrs[each_pos][0])
                    except Exception as e:
                        print("EXCEPTION", e, ctrl_name, each_pos)

        # Copy common fields
        for each_pos, val in list(target.__dict__.items()):
            if val is None:
                continue
            pos = each_pos.split("__")[-1]
            if pos == "rotate":
                dummy.rotate = val
            elif pos == "scale":
                dummy.scale = val
            elif pos == "border_radius":
                dummy.border_radius = val
            elif pos == "alignment":
                dummy.alignment = val
            elif pos == "padding":
                dummy.padding = val
            elif pos == "horizontal_alignment":
                dummy.horizontal_alignment = val
            elif pos == "vertical_alignment":
                dummy.vertical_alignment = val
            elif pos == "top":
                dummy.top = val
            elif pos == "bottom":
                dummy.bottom = val
            elif pos == "left":
                dummy.left = val
            elif pos == "right":
                dummy.right = val
            elif pos == "rows":
                try:
                    dummy.rows = [
                        ft.DataRow(
                            [
                                (
                                    ft.DataCell(tube(100))
                                    if getattr(each_col.content, "data", None) == "shimmer_load"
                                    else ft.DataCell(ft.Text())
                                )
                                for each_col in each_control.cells
                            ]
                        )
                        for each_control in val
                    ]
                except Exception:
                    pass
            elif pos == "columns":
                try:
                    dummy.columns = [
                        (
                            ft.DataColumn(tube(100))
                            if getattr(each_control.label, "data", None) == "shimmer_load"
                            else ft.DataColumn(ft.Text())
                        )
                        for each_control in val
                    ]
                except Exception:
                    pass

        # Rebuild nested parts
        if content and getattr(target, "content", None) is not None:
            dummy.content = self.create_dummy(target.content)
        if title and getattr(target, "title", None) is not None:
            dummy.title = self.create_dummy(target.title)
        if subtitle and getattr(target, "subtitle", None) is not None:
            dummy.subtitle = self.create_dummy(target.subtitle)
        if leading and getattr(target, "leading", None) is not None:
            dummy.leading = self.create_dummy(target.leading)
        if trailing and getattr(target, "trailing", None) is not None:
            dummy.trailing = self.create_dummy(target.trailing)
        if controls and getattr(target, "controls", None) is not None:
            try:
                dummy.controls = [self.create_dummy(c) for c in target.controls]
            except Exception as e:
                print(e)
                temp = []
                for c in target.controls:
                    try:
                        temp.append(self.create_dummy(c))
                    except Exception:
                        pass
                dummy.controls = temp

        if getattr(target, "data", None) == "shimmer_load":
            dummy.bgcolor = ft.Colors.with_opacity(opacity, color)

        return ft.Container(ft.Stack([dummy]), bgcolor=self.__color1)

    def did_mount(self):
        self.task = self.page.run_task(self.shine_async)

    def will_unmount(self):
        self.task.cancel()
