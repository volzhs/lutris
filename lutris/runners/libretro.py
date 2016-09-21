import os
from lutris.runners.runner import Runner
from lutris import settings


def get_cores():
    return [
        ('4do', '4do (3DO)'),
        ('gambatte', 'gambatte (Game Boy Color)'),
        ('genesis_plus_gx', 'genesis plus gx (Sega Genesis)'),
        ('mupen64plus', 'mupen64plus (Nintendo 64)'),
        ('pcsx_rearmed', 'pcsx_rearmed (Sony Playstation)'),
        ('reicast', 'reicast (Sega Dreamcast)'),
        ('snes9x', 'snes9x (Super Nintendo)'),
        ('yabause', 'yabause (Sega Saturn)'),
    ]


class libretro(Runner):
    human_name = "libretro"
    description = "Multi system emulator"
    platform = "libretro"
    runnable_alone = True
    game_options = [
        {
            'option': 'main_file',
            'type': 'file',
            'label': 'ROM file',
        },
        {
            'option': 'core',
            'type': 'choice',
            'label': 'Core',
            'choices': get_cores(),
        }
    ]

    runner_options = [
        {
            'option': 'fullscreen',
            'type': 'bool',
            'label': 'Fullscreen',
            'default': True
        }
    ]

    def get_executable(self):
        return os.path.join(settings.RUNNER_DIR, 'retroarch/retroarch')

    def get_core_path(self, core):
        return os.path.join(settings.RUNNER_DIR,
                            'retroarch/cores/{}_libretro.so'.format(core))

    def is_installed(self, core=None):
        is_retroarch_installed = os.path.exists(self.get_executable())
        if not core:
            return is_retroarch_installed
        is_core_installed = os.path.exists(self.get_core_path(core))
        return is_retroarch_installed and is_core_installed

    def play(self):
        command = [self.get_executable()]

        # Fullscreen
        fullscreen = self.runner_config.get('fullscreen')
        if fullscreen:
            command.append('--fullscreen')

        # Core
        core = self.game_config['core']
        command.append('--libretro="{}"'.format(self.get_core_path(core)))

        # Main file
        file = self.game_config.get('main_file')
        if file:
            command.append(file)

        return {'command': command}