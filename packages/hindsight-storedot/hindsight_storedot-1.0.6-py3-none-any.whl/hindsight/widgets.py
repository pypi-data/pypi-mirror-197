import ipyvuetify as v

class WidgetFacade(object):
    class Button(v.Btn):
        def __init__(self, title: str, onclick: callable, **kwargs):
            super().__init__(children=[title], **kwargs)
            self.on_event('click', onclick)
            self.__clicks = 0

        @property
        def clicks(self):
            return self.__clicks
        
        @clicks.setter
        def clicks(self, value):
            if self.__clicks < value:
                for i in range(self.__clicks, value):
                    self.fire_event('click', None)

                self.__clicks = value