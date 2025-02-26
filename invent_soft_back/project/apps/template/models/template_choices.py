from django.db import models


class TemplateFieldChoices(models.TextChoices):
    # Загрузка товаров
    PIN_NOT_DOWNLOAD = 'pin_not_download', 'Не загружать'
    PIN_NOT_DOWNLOAD_1 = 'pin_not_download_1', 'Не загружать'
    PIN_NOT_DOWNLOAD_2 = 'pin_not_download_2', 'Не загружать'
    PIN_NOT_DOWNLOAD_3 = 'pin_not_download_3', 'Не загружать'
    PIN_NOT_DOWNLOAD_4 = 'pin_not_download_4', 'Не загружать'
    PIN_NOT_DOWNLOAD_5 = 'pin_not_download_5', 'Не загружать'
    PIN_NOT_DOWNLOAD_6 = 'pin_not_download_6', 'Не загружать'
    PIN_NOT_DOWNLOAD_7 = 'pin_not_download_7', 'Не загружать'
    PIN_NOT_DOWNLOAD_8 = 'pin_not_download_8', 'Не загружать'
    PIN_NOT_DOWNLOAD_9 = 'pin_not_download_9', 'Не загружать'
    PIN_NOT_DOWNLOAD_10 = 'pin_not_download_10', 'Не загружать'

    PIN_ADDITIONAL_TITLE = 'pin_additional_title', 'Доп наименование товара'
    PIN_ADDITIONAL_TITLE_1 = 'pin_additional_title_1', 'Доп наименование товара 1'
    PIN_ADDITIONAL_TITLE_2 = 'pin_additional_title_2', 'Доп наименование товара 2'
    PIN_ADDITIONAL_TITLE_3 = 'pin_additional_title_3', 'Доп наименование товара 3'
    PIN_ADDITIONAL_TITLE_4 = 'pin_additional_title_4', 'Доп наименование товара 4'
    PIN_ADDITIONAL_TITLE_5 = 'pin_additional_title_5', 'Доп наименование товара 5'
    PIN_ADDITIONAL_TITLE_6 = 'pin_additional_title_6', 'Доп наименование товара 6'
    PIN_ADDITIONAL_TITLE_7 = 'pin_additional_title_7', 'Доп наименование товара 7'
    PIN_ADDITIONAL_TITLE_8 = 'pin_additional_title_8', 'Доп наименование товара 8'
    PIN_ADDITIONAL_TITLE_9 = 'pin_additional_title_9', 'Доп наименование товара 9'
    PIN_ADDITIONAL_TITLE_10 = 'pin_additional_title_10', 'Доп наименование товара 10'

    PIN_HIDDEN_TITLE_ATTR = 'pin_hidden_title_attr', 'Скрытый атрибут названия'
    PIN_HIDDEN_TITLE_ATTR_1 = 'pin_hidden_title_attr_1', 'Скрытый атрибут названия 1'
    PIN_HIDDEN_TITLE_ATTR_2 = 'pin_hidden_title_attr_2', 'Скрытый атрибут названия 2'
    PIN_HIDDEN_TITLE_ATTR_3 = 'pin_hidden_title_attr_3', 'Скрытый атрибут названия 3'
    PIN_HIDDEN_TITLE_ATTR_4 = 'pin_hidden_title_attr_4', 'Скрытый атрибут названия 4'
    PIN_HIDDEN_TITLE_ATTR_5 = 'pin_hidden_title_attr_5', 'Скрытый атрибут названия 5'
    PIN_HIDDEN_TITLE_ATTR_6 = 'pin_hidden_title_attr_6', 'Скрытый атрибут названия 6'
    PIN_HIDDEN_TITLE_ATTR_7 = 'pin_hidden_title_attr_7', 'Скрытый атрибут названия 7'
    PIN_HIDDEN_TITLE_ATTR_8 = 'pin_hidden_title_attr_8', 'Скрытый атрибут названия 8'
    PIN_HIDDEN_TITLE_ATTR_9 = 'pin_hidden_title_attr_9', 'Скрытый атрибут названия 9'
    PIN_HIDDEN_TITLE_ATTR_10 = 'pin_hidden_title_attr_10', 'Скрытый атрибут названия 10'

    VENDOR_CODE = 'vendor_code', 'Код товара'
    TITLE = 'title', 'Наименование товара'
    BARCODE = 'barcode', 'Штрих-код'
    BARCODE_X5 = 'barcode_x5', 'Штрих-код Х5'
    PRICE = 'price', 'Цена товара'
    REMAINDER = 'remainder', 'Остаток'
    REMAINDER_2 = 'remainder_2', 'Остаток 2'
    MEASURE = 'measure', 'Единица измерения'
    NAME_SK = 'name_sk', 'Название по ШК'
    AM = 'am', 'Признак акцизной марки'
    DM = 'dm', 'ДатаМатрикс(DataMatrix)'
    ZONE_CODE = 'zone_code', 'Код Зоны'
    ZONE_NAME = 'zone_name', 'Наименование Зоны'
    STORE_NUMBER = 'store_number', 'Номер магазина (для РеТрейдинг)'

    # ADDITIONAL_PRODUCT_NAME_1 = 'additional_product_name_1', 'Доп. наименование товара 1'  # noqa: E800
    # ADDITIONAL_PRODUCT_NAME_2 = 'additional_product_name_2', 'Доп. наименование товара 2'  # noqa: E800
    # ADDITIONAL_PRODUCT_NAME_3 = 'additional_product_name_3', 'Доп. наименование товара 3'  # noqa: E800
    # PRODUCT_GROUP = 'product_group', 'Группа товара'  # noqa: E800
    # TRADEMARK = 'trademark', 'Торговая марка'  # noqa: E800
    # SIZE = 'size', 'Размер'  # noqa: E800
    # COLOR = 'color', 'Цвет'  # noqa: E800
    # REQUIRED_MARKING = 'required_marking', 'Обязательная маркировка'  # noqa: E800
    # LOCKED_DATE = 'locked_date', 'Дата запрета оборота'  # noqa: E800
    # NAME_SK_1 = 'name_sk_1', 'Название по ШК 1'  # noqa: E800
    # NAME_SK_2 = 'name_sk_2', 'Название по ШК 2'  # noqa: E800
    # NAME_SK_3 = 'name_sk_3', 'Название по ШК 3'  # noqa: E800
    # PRICE_SK = 'price_sk', 'Цена по ШК'  # noqa: E800
    # STORAGE_CODE = 'storage_code', 'Код склада'  # noqa: E800
    # STORAGE_PLACE_CODE = 'storage_place_code', 'Код места хранения'  # noqa: E800
    # STORAGE_PLACE_TYPE = 'storage_place_type', 'Тип места хранения'  # noqa: E800
    # PERS_NUMBER = 'pers_number', 'Табельный номер'  # noqa: E800
    # COUNTER_STATUS = 'counter_status', 'Статус счётчика'  # noqa: E800
    # FULL_NAME = 'full_name', 'ФИО'  # noqa: E800
    # SERIAL_NUMBER = 'serial_number', 'Порядковый номер сотрудника'  # noqa: E800


class TemplateExportFieldChoices(models.TextChoices):
    # Группировать по ним, если первые в шаблоне
    ZONE_NAME = 'zone_name', 'Наименование Зоны'
    ZONE_NUMBER = 'zone_number', 'Номер зоны'

    BARCODE = 'barcode', 'Штрих-код'
    BARCODE_X5 = 'barcode_x5', 'Штрих-код Х5'
    VENDOR_CODE = 'vendor_code', 'Код товара'
    TITLE = 'title', 'Наименование товара'
    PRICE = 'price', 'Цена товара'
    DISCREPANCY = 'discrepancy', 'Расхождение'
    DISCREPANCY_DECIMAL = 'discrepancy_decimal', 'Расхождение, с десятичной частью'
    COUNT_SCANNED_PRODUCT = 'count_scanned_product', 'Количество отсканированных товаров'
    COUNT = 'count', 'Количество'
    COUNTER_CODE = 'counter_code', 'Код счетчика'
    DATA_MATRIX_CODE = 'data_matrix_code', 'Код DataMatrix'
    STORE_NUMBER = 'store_number', 'Номер магазина (для РеТрейдинг)'

    REMAINDER = 'remainder', 'Остаток'
    REMAINDER_2 = 'remainder_2', 'Остаток 2'
    MEASURE = 'measure', 'Единица измерения'
    NAME_SK = 'name_sk', 'Название по ШК'
    AM = 'am', 'Признак акцизной марки'
    DM = 'dm', 'ДатаМатрикс(DataMatrix)'
    ZONE_CODE = 'zone_code', 'Код Зоны'

    # PRODUCT_GROUP = 'product_group', 'Группа товара'  # noqa: E800
    # STORAGE_CODE = 'storage_code', 'Код склада'  # noqa: E800
    # TRADEMARK = 'trademark', 'Торговая марка'  # noqa: E800
    # SIZE = 'size', 'Размер'  # noqa: E800
    # COLOR = 'color', 'Цвет'  # noqa: E800
    # BOX_NUMBER = 'box_number', 'Номер короба'  # noqa: E800
    # PALLET_NUMBER = 'pallet_number', 'Номер паллеты'  # noqa: E800

    # ADDITIONAL_PRODUCT_NAME_1 = 'additional_product_name_1', 'Доп. наименование товара 1'  # noqa: E800
    # ADDITIONAL_PRODUCT_NAME_2 = 'additional_product_name_2', 'Доп. наименование товара 2'  # noqa: E800
    # ADDITIONAL_PRODUCT_NAME_3 = 'additional_product_name_3', 'Доп. наименование товара 3'  # noqa: E800
    # NAME_SK = 'name_sk', 'Название по ШК'  # noqa: E800
    # NAME_SK_1 = 'name_sk_1', 'Название по ШК 1'  # noqa: E800
    # NAME_SK_2 = 'name_sk_2', 'Название по ШК 2'  # noqa: E800
    # NAME_SK_3 = 'name_sk_3', 'Название по ШК 3'  # noqa: E800
    # PRICE_SK = 'price_sk', 'Цена по ШК'  # noqa: E800

    PIN_NOT_DOWNLOAD_1 = 'pin_not_download_1', 'Не загружать'
    PIN_NOT_DOWNLOAD_2 = 'pin_not_download_2', 'Не загружать'
    PIN_NOT_DOWNLOAD_3 = 'pin_not_download_3', 'Не загружать'
    PIN_NOT_DOWNLOAD_4 = 'pin_not_download_4', 'Не загружать'
    PIN_NOT_DOWNLOAD_5 = 'pin_not_download_5', 'Не загружать'
    PIN_NOT_DOWNLOAD_6 = 'pin_not_download_6', 'Не загружать'
    PIN_NOT_DOWNLOAD_7 = 'pin_not_download_7', 'Не загружать'
    PIN_NOT_DOWNLOAD_8 = 'pin_not_download_8', 'Не загружать'
    PIN_NOT_DOWNLOAD_9 = 'pin_not_download_9', 'Не загружать'
    PIN_NOT_DOWNLOAD_10 = 'pin_not_download_10', 'Не загружать'

    PIN_ADDITIONAL_TITLE_1 = 'pin_additional_title_1', 'Доп наименование товара 1'
    PIN_ADDITIONAL_TITLE_2 = 'pin_additional_title_2', 'Доп наименование товара 2'
    PIN_ADDITIONAL_TITLE_3 = 'pin_additional_title_3', 'Доп наименование товара 3'
    PIN_ADDITIONAL_TITLE_4 = 'pin_additional_title_4', 'Доп наименование товара 4'
    PIN_ADDITIONAL_TITLE_5 = 'pin_additional_title_5', 'Доп наименование товара 5'
    PIN_ADDITIONAL_TITLE_6 = 'pin_additional_title_6', 'Доп наименование товара 6'
    PIN_ADDITIONAL_TITLE_7 = 'pin_additional_title_7', 'Доп наименование товара 7'
    PIN_ADDITIONAL_TITLE_8 = 'pin_additional_title_8', 'Доп наименование товара 8'
    PIN_ADDITIONAL_TITLE_9 = 'pin_additional_title_9', 'Доп наименование товара 9'
    PIN_ADDITIONAL_TITLE_10 = 'pin_additional_title_10', 'Доп наименование товара 10'

    PIN_HIDDEN_TITLE_ATTR_1 = 'pin_hidden_title_attr_1', 'Скрытый атрибут названия 1'
    PIN_HIDDEN_TITLE_ATTR_2 = 'pin_hidden_title_attr_2', 'Скрытый атрибут названия 2'
    PIN_HIDDEN_TITLE_ATTR_3 = 'pin_hidden_title_attr_3', 'Скрытый атрибут названия 3'
    PIN_HIDDEN_TITLE_ATTR_4 = 'pin_hidden_title_attr_4', 'Скрытый атрибут названия 4'
    PIN_HIDDEN_TITLE_ATTR_5 = 'pin_hidden_title_attr_5', 'Скрытый атрибут названия 5'
    PIN_HIDDEN_TITLE_ATTR_6 = 'pin_hidden_title_attr_6', 'Скрытый атрибут названия 6'
    PIN_HIDDEN_TITLE_ATTR_7 = 'pin_hidden_title_attr_7', 'Скрытый атрибут названия 7'
    PIN_HIDDEN_TITLE_ATTR_8 = 'pin_hidden_title_attr_8', 'Скрытый атрибут названия 8'
    PIN_HIDDEN_TITLE_ATTR_9 = 'pin_hidden_title_attr_9', 'Скрытый атрибут названия 9'
    PIN_HIDDEN_TITLE_ATTR_10 = 'pin_hidden_title_attr_10', 'Скрытый атрибут названия 10'
