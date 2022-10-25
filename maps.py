from tkinter import *
from tkintermapview.canvas_position_marker import CanvasPositionMarker

def set_nice_marker(self, deg_x: float, deg_y: float, text: str = None, **kwargs) -> CanvasPositionMarker:
    marker = CanvasPositionMarkerNice(self, (deg_x, deg_y), text=text, **kwargs)
    marker.draw()
    self.canvas_marker_list.append(marker)
    return marker

class CanvasPositionMarkerNice(CanvasPositionMarker):
    def delete(self):
        if self in self.map_widget.canvas_marker_list:
            self.map_widget.canvas_marker_list.remove(self)
        self.map_widget.canvas.delete(self.canvas_image)
        self.canvas_image = None
        self.map_widget.canvas.delete(self.polygon, self.big_circle, self.canvas_text, self.canvas_image)
        self.polygon, self.big_circle, self.canvas_text, self.canvas_image = None, None, None, None
        self.deleted = True
        self.map_widget.canvas.update()

    def draw(self, event=None):
        canvas_pos_x, canvas_pos_y = self.get_canvas_pos(self.position)
        if self.data == "detector":
            x_offset = 7
            y_offset = 11
            y_offset_1 = 22
            y_offset_2 = 8
            size = 3
            width = 1
        else:
            x_offset = 14
            y_offset = 23
            y_offset_1 = 45
            y_offset_2 = 17
            size = 6
            width = 2
        if not self.deleted:
            if 0 - 50 < canvas_pos_x < self.map_widget.width + 50 and 0 < canvas_pos_y < self.map_widget.height + 70:
                if self.polygon is None:
                    self.polygon = self.map_widget.canvas.create_polygon(canvas_pos_x - x_offset, canvas_pos_y - y_offset,
                                                                            canvas_pos_x, canvas_pos_y,
                                                                            canvas_pos_x + x_offset, canvas_pos_y - y_offset,
                                                                            fill=self.marker_color_outside, width=width,
                                                                            outline=self.marker_color_outside, tag="marker")
                    if self.command is not None:
                        self.map_widget.canvas.tag_bind(self.polygon, "<Enter>", self.mouse_enter)
                        self.map_widget.canvas.tag_bind(self.polygon, "<Leave>", self.mouse_leave)
                        self.map_widget.canvas.tag_bind(self.polygon, "<Button-1>", self.click)
                else:
                    self.map_widget.canvas.coords(self.polygon,
                                                    canvas_pos_x - x_offset, canvas_pos_y - y_offset,
                                                    canvas_pos_x, canvas_pos_y,
                                                    canvas_pos_x + x_offset, canvas_pos_y - y_offset)
                if self.big_circle is None:
                    self.big_circle = self.map_widget.canvas.create_oval(canvas_pos_x - x_offset, canvas_pos_y - y_offset,
                                                                            canvas_pos_x + x_offset, canvas_pos_y - y_offset,
                                                                            fill=self.marker_color_circle, width=size,
                                                                            outline=self.marker_color_outside, tag="marker")
                    if self.command is not None:
                        self.map_widget.canvas.tag_bind(self.big_circle, "<Enter>", self.mouse_enter)
                        self.map_widget.canvas.tag_bind(self.big_circle, "<Leave>", self.mouse_leave)
                        self.map_widget.canvas.tag_bind(self.big_circle, "<Button-1>", self.click)
                else:
                    self.map_widget.canvas.coords(self.big_circle,
                                                    canvas_pos_x - x_offset, canvas_pos_y - y_offset_1,
                                                    canvas_pos_x + x_offset, canvas_pos_y - y_offset_2)

                if self.text is not None:
                    if self.canvas_text is None:
                        self.canvas_text = self.map_widget.canvas.create_text(canvas_pos_x, canvas_pos_y - 23,
                                                                                anchor=S,
                                                                                text=self.text,
                                                                                fill=self.text_color,
                                                                                font=self.font,
                                                                                tag=("marker", "marker_text"))
                        if self.command is not None:
                            self.map_widget.canvas.tag_bind(self.canvas_text, "<Enter>", self.mouse_enter)
                            self.map_widget.canvas.tag_bind(self.canvas_text, "<Leave>", self.mouse_leave)
                            self.map_widget.canvas.tag_bind(self.canvas_text, "<Button-1>", self.click)
                    else:
                        self.map_widget.canvas.coords(self.canvas_text, canvas_pos_x, canvas_pos_y - 23)
                        self.map_widget.canvas.itemconfig(self.canvas_text, text=self.text)
                else:
                    if self.canvas_text is not None:
                        self.map_widget.canvas.delete(self.canvas_text)

                if self.image is not None and self.image_zoom_visibility[0] <= self.map_widget.zoom <= self.image_zoom_visibility[1]\
                        and not self.image_hidden:

                    if self.canvas_image is None:
                        self.canvas_image = self.map_widget.canvas.create_image(canvas_pos_x, canvas_pos_y - 45,
                                                                                anchor=S,
                                                                                image=self.image,
                                                                                tag=("marker", "marker_image"))
                    else:
                        self.map_widget.canvas.coords(self.canvas_image, canvas_pos_x, canvas_pos_y - 45)
                else:
                    if self.canvas_image is not None:
                        self.map_widget.canvas.delete(self.canvas_image)
                        self.canvas_image = None
            else:
                self.map_widget.canvas.delete(self.canvas_image)
                self.canvas_image = None
                self.map_widget.canvas.delete(self.polygon, self.big_circle, self.canvas_text, self.canvas_image)
                self.polygon, self.big_circle, self.canvas_text, self.canvas_image = None, None, None, None

            self.map_widget.manage_z_order()