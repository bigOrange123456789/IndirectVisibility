import numpy
import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
import glm
from pyrr import  matrix44
from math import sin, cos, radians
# from OBJ_Loader import*
import pywavefront



class threeD_viewer():
        def __init__(self):

            vertices = [[-33.64413, 0.0, 19.03057], 
                        [-33.64818, 0.0, 19.0219],
                        [-33.64921, 0.0, 19.011],
                        [-33.64913, 0.0, 19.03027], 
                        [-33.69828, 0.0, 19.0219],
                        [-33.64991, 0.0, 19.021]]

            self.vertices = numpy.array(vertices, dtype='f')

            self.cam = Camera(self.vertices[0][0], self.vertices[0][2])
            self.WIDTH, self.HEIGHT = 1280, 720
            self.lastX, self.LastY = self.WIDTH / 2, self.HEIGHT / 2
            self.first_mouse = True
            self.forward, self.backward, self.right, self.left, self.up, self.down = False, False, False, False, False, False

            self.x_start, self.y_start = self.vertices[0][0], self.vertices[0][2]

            self.vertex_obj = """
                       # version 330
                       in layout(location = 0) vec3 aPos;
                       in layout (location = 3) mat4 instanceMatrix;

                       uniform mat4 model;
                       uniform mat4 view;
                       uniform mat4 projection;

                       void main()
                       {
                           gl_Position = projection * view * instanceMatrix * vec4(aPos, 1.0);
                       }
                       """
            self.fragment_obj = """
                       #version 330
                       out vec4 FragColor;

                       void main()
                       {                           
                               FragColor = vec4(1.0,1.0,1.0, 1.0);
                       }
                        """
            self.main()

        # the keyboard input callback
        def key_input_clb(self, window, key, scancode, action, mode):
            if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
                glfw.set_window_should_close(window, True)
            if key == glfw.KEY_W and action == glfw.PRESS:
                self.forward = True
            elif key == glfw.KEY_W and action == glfw.RELEASE:
                self.forward = False
            if key == glfw.KEY_S and action == glfw.PRESS:
                self.backward = True
            elif key == glfw.KEY_S and action == glfw.RELEASE:
                self.backward = False
            if key == glfw.KEY_A and action == glfw.PRESS:
                self.left = True
            elif key == glfw.KEY_A and action == glfw.RELEASE:
                self.left = False
            if key == glfw.KEY_D and action == glfw.PRESS:
                self.right = True
            elif key == glfw.KEY_D and action == glfw.RELEASE:
                self.right = False
            if key == glfw.KEY_Q and action == glfw.PRESS:
                self.up = True
            elif key == glfw.KEY_Q and action == glfw.RELEASE:
                self.up = False
            if key == glfw.KEY_E and action == glfw.PRESS:
                self.down = True
            elif key == glfw.KEY_E and action == glfw.RELEASE:
                self.down = False

        def do_movement(self):
            if self.forward:
                self.cam.process_keyboard("FORWARD", 0.000008)
            if self.backward:
                self.cam.process_keyboard("BACKWARD", 0.000008)
            if self.right:
                self.cam.process_keyboard("RIGHT", 0.000008)
            if self.left:
                self.cam.process_keyboard("LEFT", 0.000008)
            if self.up:
                self.cam.process_keyboard("UP", 0.000008)
            if self.down:
                self.cam.process_keyboard("DOWN", 0.000008)

        def mmouse_look_clb(self, window, xpos, ypos):
            if self.first_mouse:
                self.lastX = xpos
                self.lastY = ypos
                self.first_mouse = False

            xoffset = xpos - self.lastX
            yoffset = self.lastY - ypos

            self.lastX = xpos
            self.lastY = ypos
            self.cam.process_mouse_movement(xoffset, yoffset)


        def window_resize(self, window, width, height):
            glViewport(0, 0, width, height)
            projection = pyrr.matrix44.create_perspective_projection_matrix(45, width / height,  0.0001, 100)
            proj_loc = glGetUniformLocation(self.shader_obj, "projection")
            glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)

        def main(self):

            # initializing glfw library
            if not glfw.init():
                raise Exception("glfw can not be initialized!")
            # creating the window
            window = glfw.create_window(self.WIDTH, self.HEIGHT, "My OpenGL window", None, None)
            # check if window was created
            if not window:
                glfw.terminate()
                raise Exception("glfw window can not be created!")


            # set window's position
            glfw.set_window_pos(window, 400, 200)
            # set the callback function for window resize
            glfw.set_window_size_callback(window, self.window_resize)
            glfw.set_cursor_pos_callback(window, self.mmouse_look_clb)
            glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
            glfw.set_key_callback(window, self.key_input_clb)
            # make the context current
            glfw.make_context_current(window)

            self.shader_obj = compileProgram(compileShader(self.vertex_obj, GL_VERTEX_SHADER),
                                         compileShader(self.fragment_obj, GL_FRAGMENT_SHADER))


            obj_file = pywavefront.Wavefront('OBJ_PINS/Mcdonalds.obj', collect_faces=True)
            obj_vertices = numpy.array(obj_file.vertices, dtype='f')
            faces_list = []
            for mesh in obj_file.mesh_list:
                for face in mesh.faces:
                    faces_list.append(face)

            obj_ind = numpy.array(faces_list,  dtype=numpy.int32)


            VAOs = glGenVertexArrays(1)
            glBindVertexArray(VAOs)
            # Vertex Buffer Object
            VBO = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, VBO)
            glBufferData(GL_ARRAY_BUFFER, obj_vertices.nbytes, obj_vertices, GL_STATIC_DRAW)
            # Element Buffer Object
            EBO = glGenBuffers(1)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
            glBufferData(GL_ELEMENT_ARRAY_BUFFER, obj_ind.nbytes, obj_ind, GL_STATIC_DRAW)
            # vertices
            glEnableVertexAttribArray(0)
            glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, obj_vertices.itemsize * 3, ctypes.c_void_p(0))

            # instance locations
            amount = len(self.vertices)
            #List storing the same object in different places
            modelMatrices = []
            #Storring the objects in a list
            for i in range(0, amount):
                model_o = glm.mat4(1.0)
                model_o = glm.translate(model_o, glm.vec3(self.vertices[i][0], self.vertices[i][1], self.vertices[i][2]))
                model_o = glm.scale(model_o, glm.vec3(0.0001, 0.0001, 0.0001))
                modelMatrices.append(model_o)

            #Create VBO for instancing
            instanceVBO = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, instanceVBO)
            glBufferData(GL_ARRAY_BUFFER, glm.sizeof(glm.mat4), glm.value_ptr(modelMatrices[0]), GL_STATIC_DRAW)
            #Bind each vertex attrib array of matrices (4 vectors in Matrix)
            glEnableVertexAttribArray(3)
            glVertexAttribPointer(3, 4, GL_FLOAT, GL_FALSE, glm.sizeof(glm.mat4), ctypes.c_void_p(0))
            glEnableVertexAttribArray(4)
            glVertexAttribPointer(4, 4, GL_FLOAT, GL_FALSE, glm.sizeof(glm.mat4), ctypes.c_void_p(glm.sizeof(glm.vec4)))
            glEnableVertexAttribArray(5)
            glVertexAttribPointer(5, 4, GL_FLOAT, GL_FALSE, glm.sizeof(glm.mat4), ctypes.c_void_p((2 * glm.sizeof(glm.vec4))))
            glEnableVertexAttribArray(6)
            glVertexAttribPointer(6, 4, GL_FLOAT, GL_FALSE, glm.sizeof(glm.mat4), ctypes.c_void_p((3 * glm.sizeof(glm.vec4))))
            #Set instancing
            glVertexAttribDivisor(3, 1)
            glVertexAttribDivisor(4, 1)
            glVertexAttribDivisor(5, 1)
            glVertexAttribDivisor(6, 1)

            #End VAO
            glBindVertexArray(0)


            glClearColor(0, 0.1, 0.1, 1)
            glEnable(GL_DEPTH_TEST)
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

            #projection = pyrr.matrix44.create_perspective_projection_matrix(45, self.WIDTH / self.HEIGHT, 0.0001, 1000)

            projection = glm.perspective(glm.radians(45.0), self.WIDTH / self.HEIGHT, 0.0001, 1000)

            glUseProgram(self.shader_obj)
            view_loc_obj = glGetUniformLocation(self.shader_obj, "view")
            proj_loc_obj = glGetUniformLocation(self.shader_obj, "projection")
            model_loc_obj = glGetUniformLocation(self.shader_obj, "model")
            glUniformMatrix4fv(proj_loc_obj, 1, GL_FALSE, glm.value_ptr(projection))
            glUseProgram(0)

            # the main application loop
            while not glfw.window_should_close(window):
                glfw.poll_events()
                self.do_movement()

                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

                glUseProgram(self.shader_obj)
                view = self.cam.get_view_matrix()
                glUniformMatrix4fv(proj_loc_obj, 1, GL_FALSE, glm.value_ptr(projection))
                glUniformMatrix4fv(view_loc_obj, 1, GL_FALSE, view)

                glBindVertexArray(VAOs)
                glDrawElementsInstanced(GL_TRIANGLES, len(obj_ind)*3, GL_UNSIGNED_INT, None, amount)
                glBindVertexArray(0)

                glUseProgram(0)


                glfw.swap_buffers(window)

            # terminate glfw, free up allocated resources
            glfw.terminate()


class Camera:
        def __init__(self, xstart, ystart):
            self.camera_pos = glm.vec3(xstart+0.005, 0, ystart+0.01)
            #self.camera_pos = glm.vec3(0, 0, 0)
            print(xstart+0.005)
            print(ystart+0.01)

            self.camera_front = glm.vec3(0.0, 0.0, -200.0)
            self.camera_up = glm.vec3(0.0, 1.0, 0.0)
            self.camera_right = glm.vec3(1.0, 0.0, 0.0)

            self.mouse_sensitivity = 0.25
            self.jaw = -90.0
            self.pitch = 0.0

        def get_view_matrix(self):
            return matrix44.create_look_at(self.camera_pos, self.camera_pos + self.camera_front, self.camera_up)

        def process_mouse_movement(self, xoffset, yoffset, constrain_pitch=True):
            xoffset *= self.mouse_sensitivity
            yoffset *= self.mouse_sensitivity

            self.jaw += xoffset
            self.pitch += yoffset

            if constrain_pitch:
                if self.pitch > 45:
                    self.pitch = 45
                if self.pitch < -45:
                    self.pitch = -45

            self.update_camera_vectors()

        def update_camera_vectors(self):
            front = glm.vec3(0.0, 0.0, 0.0)
            front.x = cos(radians(self.jaw)) * cos(radians(self.pitch))
            front.y = sin(radians(self.pitch))
            front.z = sin(radians(self.jaw)) * cos(radians(self.pitch))

            self.camera_front = glm.normalize(front)
            self.camera_right = glm.normalize(glm.cross(self.camera_front, glm.vec3(0.0, 1.0, 0.0)))
            #self.camera_up = glm.normalize(glm.cross(self.camera_right, self.camera_front))

        # Camera method for the WASD movement
        def process_keyboard(self, direction, velocity):
            if direction == "FORWARD":
                self.camera_pos += self.camera_front * velocity
            if direction == "BACKWARD":
                self.camera_pos -= self.camera_front * velocity
            if direction == "LEFT":
                self.camera_pos -= self.camera_right * velocity
            if direction == "RIGHT":
                self.camera_pos += self.camera_right * velocity
            if direction == "UP":
                self.camera_pos += self.camera_up * velocity
            if direction == "DOWN":
                self.camera_pos -= self.camera_up * velocity

threeD_viewer()