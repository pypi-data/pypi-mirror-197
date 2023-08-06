from utilities.choices import ChoiceSet


class OSTypeChoices(ChoiceSet):
    key = 'StorageConfigurationDrive.type'

    CHOICE_LINUX = 'Linux'
    CHOICE_WINDOWS = 'Windows'

    CHOICES = [
        (CHOICE_LINUX, 'Linux', 'cyan'),
        (CHOICE_WINDOWS, 'Windows', 'yellow'),
    ]
