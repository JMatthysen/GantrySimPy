from math import *
import numpy as np
from dearpygui.simple import *
from dearpygui.core import *
from GuiMain import *


class ViewScreen(CanvasView):
    def __init__(self, name, axes, width, height, parent, event_bus, camera_dist, s1=list(), s2=list(), s3=list()):
        CanvasView.__init__(self, name, axes, width, height, parent, event_bus)

        self.camera_dist    = camera_dist

        self.s1             = s1
        self.s2             = s2
        self.s3             = s3

        self.mid_point      = list()

        self.norm_vector    = list()
        self.plane_equation = list()

        self.camera_point   = list()

        self._initialize_screen()

    def _initialize_screen(self):
        if self._run_screen_checks():
            self._calc_mid_point()
            #  log_debug(f"MID_POINT  ::  {self.mid_point}")

            self._calc_norm_vector()
            #  log_debug(f"PLANE_EQUATION  ::  {self.plane_equation}")
            #  log_debug(f"NORM_VECTOR  ::  {self.norm_vector}")

            self._calc_camera_point()
            #  log_debug(f"CAMERA_POINT  ::  {self.camera_point}")
        else:
            pass
    
    def _run_screen_checks(self):
        x1, y1, z1 = self.s1[0], self.s1[1], self.s1[2]
        x2, y2, z2 = self.s2[0], self.s2[1], self.s2[2]
        x3, y3, z3 = self.s3[0], self.s3[1], self.s3[2]

        w = sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
        if w != self.width:
            print("Widths do not match.")
            return False

        h = sqrt((x3 - x1)**2 + (y3 - y1)**2 + (z3 - z1)**2)
        if h != self.height:
            print("Heights do not match.")
            return False

        return True

    def _calc_mid_point(self):
        self.mid_point = list()

        for i in range(3):
            self.mid_point.append( (self.s2[i] + self.s3[i]) / 2)

    def _calc_norm_vector(self):
        abc = list()

        a = np.array([[self.s1[0], self.s1[1], self.s1[2]],
                      [self.s2[0], self.s2[1], self.s2[2]],
                      [self.s3[0], self.s3[1], self.s3[2]]])
        b = np.array([1, 1, 1])
        x = np.linalg.solve(a, b)

        for i in range(3):
            self.plane_equation.append(x[i])


        self.norm_vector    = list()

        for i in range(3):
            self.norm_vector.append(self.plane_equation[i] / (sqrt( self.plane_equation[0]**2 + self.plane_equation[1]**2
                                                    + self.plane_equation[2]**2)))

    def _calc_camera_point(self):
        self.camera_point = list()

        for i in range(3):
            self.camera_point.append(self.mid_point[i] + self.camera_dist * self.norm_vector[i])
    
    def project_point(self, real_point):
        projected_point = self._get_projected_point(real_point)
        #  log_debug(f"PROJECTED_POINT :: {projected_point}")

        cos_u, cos_v    = self._calc_screen_angles(projected_point)
        #  log_debug(f"COS_U, COS_V ::  {cos_u} , {cos_v}")

        screen_point    = self._calc_rel_projection(cos_u, cos_v, projected_point)
        #  log_debug(f"SCREEN_POINT :: {screen_point}")

        return screen_point

    def _get_projected_point(self, three_d_point):
        xc, yc, zc  = self.camera_point[0], self.camera_point[1], self.camera_point[2]
        xa, ya, za  = three_d_point[0], three_d_point[1], three_d_point[2]
        a, b, c     = self.plane_equation[0], self.plane_equation[1], self.plane_equation[2]

        k = ( 1 - a * xa - b * ya - c * za) / (a * (xc - xa) + b * (yc - ya) + c * (zc - za))

        projected_point = list()
        for i in range(3):
            projected_point.append(k * (self.camera_point[i] - three_d_point[i]) + three_d_point[i])

        return projected_point

    def _calc_screen_angles(self, projected_point):
        cos_u   = ( (self.s2[0] - self.s1[0])*(projected_point[0] - self.s1[0]) + (self.s2[1] - self.s1[1]) *
                    (projected_point[1] - self.s1[1]) + (self.s2[2] - self.s2[2]) *
                    (projected_point[2] - self.s1[2]) )/ (self.width * sqrt((projected_point[0] - self.s1[0])**2 +
                                                                            (projected_point[1] - self.s1[1])**2 +
                                                                            (projected_point[2] - self.s1[2])**2 ))

        cos_v   = ( (self.s3[0] - self.s1[0])*(projected_point[0] - self.s1[0]) + (self.s3[1] - self.s1[1]) *
                    (projected_point[1] - self.s1[1]) + (self.s3[2] - self.s2[2]) *
                    (projected_point[2] - self.s1[2]) )/ (self.height * sqrt((projected_point[0] - self.s1[0])**2 +
                                                                            (projected_point[1] - self.s1[1])**2 +
                                                                            (projected_point[2] - self.s1[2])**2 ))
        return cos_u, cos_v

    def _calc_rel_projection(self, cos_u, cos_v, projected_point):
        horizontal  = sqrt((projected_point[0] - self.s1[0])**2 + (projected_point[1] - self.s1[1])**2 +
                           (projected_point[2] - self.s1[2])**2 ) * cos_u

        #  if this doesn't work, check here and use SIN_U
        vertical    = sqrt((projected_point[0] - self.s1[0])**2 + (projected_point[1] - self.s1[1])**2 +
                           (projected_point[2] - self.s1[2])**2 ) * cos_v

        return [horizontal, vertical]

    #  GUI
    def add_entity(self, axis, color):
        self.entities.append(Entity3D(axis, color))
        self._draw_entity(self.entities[-1])

    def _draw_entity(self, entity):
        hidden_point = self._pick_furthest_entity_point(entity)

        for side in entity.sides:
            if hidden_point in side:
                pass
            else:
                points = list()
                for index in side:
                    #  if you want to have a birds eye view
                    #  points.append(entity.axis.coordinates[index])
                    points.append(self.project_point(entity.axis.coordinates[index]))
                    points[-1][-1] = self.height - points[-1][-1]
                draw_polygon(self.name, points, entity.color_border, fill=entity.color)

    def _pick_furthest_entity_point(self, entity):
        max_dist = 0
        furthest_point_index = 0

        for i, point in enumerate(entity.axis.coordinates):
            distance = self.calc_3d_dist(point, self.camera_point)
            if distance >= max_dist:
                max_dist = distance
                furthest_point_index = i

        return furthest_point_index

    def _translate_view_screen(self, delta_xyz):
        # Get an input from a slider or something and then apply it to s1, s2, s3 and then re initialize the screen
        print(f"BEFORE:: {self.s1}")
        for i in range(3):
            self.s1[i] += delta_xyz[i]
            self.s2[i] += delta_xyz[i]
            self.s3[i] += delta_xyz[i]
        print(f"AFTER:: {self.s1}")

        self._initialize_screen()
        self._refresh_canvas()

    def _rotate_view_screen(self, delta_zangle):
        # get an input from a slider that would change the view ports angle relative to the z axis
        # could maybe rotate polarly the screen vertices

        pass

    @staticmethod
    def calc_3d_dist(point1, point2):
        return sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2 + (point2[2] - point1[2])**2)
