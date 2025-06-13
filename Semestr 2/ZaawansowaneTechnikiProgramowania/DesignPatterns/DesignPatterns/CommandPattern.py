"""W tym przykładzie mamy interfejs Command, który definiuje metodę execute. Następnie mamy konkretne polecenie LightOnCommand,
które implementuje ten interfejs i ma odniesienie do obiektu odbiorcy Light, który jest odpowiedzialny za wykonanie akcji.
Klasa RemoteControl reprezentuje pilota zdalnego sterowania, który może być skonfigurowany za pomocą różnych poleceń. 
Może ustawiać konkretne polecenie i wywoływać je za pomocą metody press_button.
Wzorzec Polecenia pozwala na elastyczne zarządzanie żądaniami i ich realizacją. Możemy łatwo dodawać nowe polecenia 
bez konieczności modyfikowania istniejącego kodu klienta. To wzmacnia zasady oddzielania odpowiedzialności 
i umożliwia tworzenie systemów bardziej elastycznych i rozszerzalnych."""

# Interfejs polecenia
class Command:
    def execute(self):
        pass
# Konkretne polecenie
class LightOnCommand(Command):
    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.turn_on()
# Obiekt odbiorcy
class Light:
    def turn_on(self):
        print("Lights are on")
# Polecenie klienta
class RemoteControl:
    def __init__(self):
        self.command = None

    def set_command(self, command):
        self.command = command

    def press_button(self):
        if self.command:
            self.command.execute()

# Użycie wzorca Polecenia
light = Light()
light_on = LightOnCommand(light)

remote = RemoteControl()
remote.set_command(light_on)

remote.press_button()