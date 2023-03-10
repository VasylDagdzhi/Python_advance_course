from abc import ABC, abstractmethod


class Laptop(ABC):
    screen_resolution: str
    keyboard_layout: str
    touchpad_size: str
    web_camera: str
    ports: list
    dynamic_sand_presence: str

    @abstractmethod
    def __init__(self, screen_resolution, keyboard_layout, touchpad_size, webcamera, ports, dynamicsand):
        pass

    @abstractmethod
    def Screen(self):
        pass

    @abstractmethod
    def Keyboard(self):
        pass

    @abstractmethod
    def Touchpad(self):
        pass

    @abstractmethod
    def WebCam(self):
        pass

    @abstractmethod
    def Ports(self):
        pass

    @abstractmethod
    def Dynamicsand(self):
        pass


class HPLaptop(Laptop):
    def __init__(self, screen_resolution, keyboard_layout, touchpad_size, webcamera, ports, dynamicsand):
        self.screen_resolution = screen_resolution
        self.keyboard_layout = keyboard_layout
        self.touchpad_size = touchpad_size
        self.web_camera = webcamera
        self.ports = ports
        self.dynamic_sand_presence = dynamicsand

    def Screen(self):
        return f"Screen resolution: {self.screen_resolution} dpi"

    def Keyboard(self):
        return f"Keyboard layout type: {self.keyboard_layout}"

    def Touchpad(self):
        return f"Touchpad size: {self.touchpad_size}"

    def WebCam(self):
        return f"Web cam presence: {self.web_camera}"

    def Ports(self):
        string = " -> Ports list:\n"
        for port in self.ports:
            string += f"\t - {port}\n"
        return string

    def Dynamicsand(self):
        return f"Dynamic sand presence: {self.dynamic_sand_presence}"

    def __str__(self):
        return f"{self.__class__}\n -> {self.Screen()}\n -> {self.Keyboard()}\n -> {self.Touchpad()}\n " \
               f"-> {self.WebCam()}\n {self.Ports()} -> {self.Dynamicsand()}"
