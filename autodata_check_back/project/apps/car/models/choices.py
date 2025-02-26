from django.db import models


class DriveTypeChoices(models.TextChoices):
    REAR = 'rear', 'Задний'
    FRONT = 'front', 'Передний'
    FULL_4WD = 'full_4wd', 'Полный'    # noqa: WPS114
    OPTIONAL_4WD = 'optional_4wd', 'Полный'    # noqa: WPS114


class EngineTypeChoices(models.TextChoices):
    PETROL = 'petrol', 'Бензин'
    HYBRID = 'hybrid', 'Гибрид'
    DIESEL = 'diesel', 'Дизель'
    PETROL_AND_GAS = 'petrol_and_gas', 'Газобаллонное оборудование'
    ELECTRIC = 'electric', 'Электро'


class GearboxTypeChoices(models.TextChoices):
    MANUAL = 'manual', 'Механическая'
    AUTOMATIC = 'automatic', 'Автоматическая'
    VARIATOR = 'variator', 'Вариатор'
    ROBOTIZED = 'robotized', 'Робот'


class BodyTypeChoices(models.TextChoices):
    COUPE = 'coupe', 'Купе'
    ROADSTER = 'roadster', 'Родстер'
    SEDAN = 'sedan', 'Седан'
    HATCHBACK = 'hatchback', 'Хэтчбек'
    SUV = 'suv', 'Внедорожник'
    UNIVERSAL = 'universal', 'Универсал'
    CABRIOLET = 'cabriolet', 'Кабриолет'
    LIFTBACK = 'liftback', 'Лифтбек'
    PICKUP = 'pickup', 'Пикап'
    COMPACTVAN = 'compactvan', 'Компактвэн'
    SPEEDSTER = 'speedster', 'Спидстер'
    FASTBACK = 'fastback', 'Фастбэк'
    TARGA = 'targa', 'Тарга'
    MINIVAN = 'minivan', 'Минивэн'
    MICROVAN = 'microvan', 'Микровэн'
    LONG = 'long', 'Лимузин'
    VAN = 'van', 'Фургон'
    PHAETON = 'phaeton', 'Фаэтон'
    FULLMETAL_VAN = 'fullmetal_van', 'Цельнометаллический фургон'
    AMBULANCE = 'ambulance', 'Микроавтобус'
    MINIBUS = 'minibus', 'Микроавтобус'
    REFRIGERATOR = 'refrigerator', 'Рефрижератор'
    FLATBED_TRUCK = 'flatbed_truck', 'Бортовой'
    CARGO_VAN = 'cargo_van', 'Фургон'
    TENT_TRUCK = 'tent_truck', 'Тентованный фургон'
    CHASSIS = 'chassis', 'Шасси'
    ISOTHERMAL = 'isothermal', 'Изотермический фургон'
    EVACUATOR = 'evacuator', 'Эвакуатор'
    TIPPER = 'tipper', 'Самосвал'
    CISTERN = 'cistern', 'Автоцистерна'
