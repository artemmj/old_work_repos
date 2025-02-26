CONSTANCE_ADDITIONAL_FIELDS = {
    'ckeditor': ['ckeditor_uploader.fields.RichTextUploadingFormField', {}],
}

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CONSTANCE_CONFIG = {
    'USER_AGREEMENT': ('', 'Пользовательское соглашение', 'ckeditor'),
    'POLICY': ('', 'Политика в отношении обработки персональных данных', 'ckeditor'),
    'ABOUT_PLATFORM': ('', 'О платформе', 'ckeditor'),
    '404': ('', '404', 'ckeditor'),

    'SEND_SMS': (True, 'Отправка смс', bool),
    'ENABLE_CHECKING_USER': (True, 'Проверка пользователя(для модерации)', bool),
    'INSPECTOR_PERCENT': (60.0, 'Процент начисления инспектору за выполненное задание', float),
    'SELF_INSPECTION_PRICE': ('200.00', 'Цена за самостоятельный осмотр', str),
    'CONFIRMATION_CODE_EXPIRED_TIME': (1, 'Время жизни кода-подтверждения (минуты)', int),
    'INSPECTION_TASK_ACTIVITY_TIME': (24, 'Время на активность инспектора по заданию (часы)', int),
    'INSPECTION_SEARCHING_TIME': (2, 'Время на поиск инспектора (часы)', int),
    'ORG_BALANCE_EMAIL': (
        'lezzhovmu@autodataspace.ru',
        'Почта, на которую слать письмо с инфой о пополнении баланса',
        str,
    ),

    'ASSIGNING_INSPECTION_TO_INSPECTOR': (
        'Вам поступил новый заказ на осмотр',
        'Назначение задания на инспектора',
        str,
    ),
    'TASK_ACCEPTED_BY_INSPECTOR': (
        'Ваше задание принято инспектором',
        'Заказчику задания, получает уведомление после принятия инспектором задания',
        str,
    ),
    'INSPECTION_COMPLETE': (
        'Ваше задание выполнено',
        'Заказчику задания, получает уведомления после завершения задания инспектором',
        str,
    ),
    'INSPECTION_ORGANIZATION_INSPECTOR_NEED_FIXES': (
        'Задание требует уточнений',
        'Инспектору организации, когда пришли исправления по заданию',
        str,
    ),
    'INSPECTION_SERVICE_INSPECTOR_NEED_FIXES': (
        'Задание требует уточнений',
        'Инспектору сервиса, когда пришли исправления по заданию',
        str,
    ),
    'INSPECTOR_MONEY_CAME': (
        'Ваш баланс пополнен на [ ]',
        'Инспектору сервиса, когда за задачу пришли деньги',
        str,
    ),
    'ISSUING_ORG_INSPECTOR': (
        'Вам назначены осмотры по заданию организации',
        'Инспектору организации, когда он назначен на задание',
        str,
    ),
    'ISSUING_SERVICE_INSPECTOR': (
        'Вам назначено новое задание',
        'Инспектору сервиса, когда он назначен на задание',
        str,
    ),
    'SHARE_TEMPLATE': (
        '[ ] поделился с вами новым шаблоном',
        'Когда шарят юзеру шаблон',
        str,
    ),
    'INVITE_ORGANIZATION': (
        'Вас пригласили в организацию [ ]',
        'Когда юзера добавляют в организацию',
        str,
    ),
    'ORGANIZATION_BALANCE_MONEY_CAME': (
        'Ваш баланс пополнен на [ ]',
        'Когда юзер пополнил баланс организации',
        str,
    ),
    'INSUFFICIENT_FUNDS': (
        'На вашем балансе недостаточно средств для завершения осмотра/для создания задания',
        'Когда у юзера недостаточно средств для создания задания или оплаты осмотра',
        str,
    ),
    'INSPECTOR_ACCR_NEW_FIXES': (
        'По вашему осмотру на аккредитацию пришли исправления',
        'Когда по осмотру на аккредитацию пришли исправления',
        str,
    ),
    'INSPECTOR_ACCR_SUCC_COMPLETE': (
        'Поздравляем, вы прошли аккредитацию на инспектора, заполните реквизиты для работы!',
        'Когда успешно прошли аккредитацию на инспектора',
        str,
    ),
    'CANT_GET_TASK_WITHOUT_REQUISITE': (
        'Вы не сможете получать задания на осмотр, пока не заполните реквизиты.',
        'Когда аккредитованный инспектор не заполнил реквизиты',
        str,
    ),
    'ADDRESS_QUERY_AND_LOCATION_TOGETHER_ERROR': (
        'Невозможно передать и query и location.',
        'Когда в address/ передали одновременно query и location',
        str,
    ),
    'CAR_INVALID_GOV_NUM_ERROR': (
        str(
            'Введите верный формат гос.номера:'
            'АА7777 777, A 777 AA 77, A 777 AA 777, AA 777 A 77, AA 777 77 ,АА 7777 77'    # noqa: WPS326
            'Для форматов гос. номеров А777АА77, А777АА777, АА777А77, '    # noqa: WPS326
            'АА777 77, АА777 777, АА7777 77, АА7777 777 используйте заглавные буквы кириллицы.\n'  # noqa: WPS326
            'Для форматов гос. номеров 7777 AA-7, 777 ААА 77 используйте заглавные буквы латиницы.',  # noqa: WPS326
        ),
        'Когда в car/ передали неверный гос. номер',
        str,
    ),
    'CITY_IMPORT_NEED_XLSX_ERROR': (
        'Требуется файл в формате .xlsx!',
        'Когда в city/ при импорте экселя передали файл некорректного формата',
        str,
    ),
    'FILE_DB_FILE_NOT_FOUND_ERROR': (
        'Не удалось найти файл БД.',
        'Когда в db_file/ не удалось найти файл базы данных',
        str,
    ),
    'INSPECTION_NEED_NULL_VALUE_ERROR': (
        'Проверьте, чтобы один из параметров обязательно был с null значением.',
        'Когда в inspection/ переданы два параметра с не null значением',
        str,
    ),
    'INSPECTION_IMPOSSIBLE_BIND_CLIENT_SIGN_ERROR': (
        'Невозможно привязать подпись клиента к осмотру, подпись в осмотре уже привязана.',
        'Когда в inspection/ невозможно привязать подпись клиента к осмотру',
        str,
    ),
    'INSPECTION_IMPOSSIBLE_BIND_INSPECTOR_SIGN_ERROR': (
        'Невозможно привязать подпись инспектора к осмотру, подпись в осмотре уже привязана.',
        'Когда в inspection/ невозможно привязать подпись инпектора к осмотру',
        str,
    ),
    'TASK_CAR_VALIDATE_SERIAL_NUM_ERROR': (
        'Авто с порядковый номер SERIAL_NUMBER в текущем задании уже существует.',
        'Когда в inspection_task/ в заданиях уже есть авто с таким порядковым номером',
        str,
    ),
    'TASK_VALIDATE_DATE_ERROR': (
        'Нельзя поставить дату осмотра позже DATE.',
        'Когда в inspection_task/ пытаются передать planed_date меньше, чем end_date',
        str,
    ),
    'TASK_NOT_INSPECTOR_SEARCH_BY_TASK_ERROR': (
        'По заданию нет поиска инспектора.',
        'Когда в inspection_task/ при отмене поиска инспектора нет объекта поиска',
        str,
    ),
    'TASK_DELETE_CARS_BUT_NON_DRAFT_ERROR': (
        'Для удаления машин, задание должно быть в статусе черновик.',
        'Когда в inspection_task/ при удалении автомоблилей статус задания не черновик',
        str,
    ),
    'ACCRED_USER_HAVE_REQUEST_ERROR': (
        'Пользователь уже подал заявку.',
        'Когда в accreditation_request/ пользователь повторно пытается создать заявку',
        str,
    ),
    'ORG_INVITATION_USER_IS_MEMBERSHIP_ERROR': (
        'Пользователь PHONE уже является членом организации.',
        'Когда в org_invitation/ пользователь уже является членом организации',
        str,
    ),
    'ORG_INVITATION_USER_HAVE_INVITE_ERROR': (
        'Пользователь PHONE уже имеет необработанное приглашение на вступление в организацию.',
        'Когда в org_invitation/ пользователь уже имеет приглашение в организацию',
        str,
    ),
    'ORG_NOT_FOUND_BY_INN_DADATA_ERROR': (
        'Не найдена организация по введенному ИНН в dadata.',
        'Когда в organization/ при создании не найдена огранизация по ИНН',
        str,
    ),
    'ORG_MEMBERSHIP_CANT_LEAVE_LAST_ORG_ERROR': (
        'Невозможно покинуть последнюю организацию.',
        'Когда пытаемся исключить из последней организации у пользователя',
        str,
    ),
    'ORG_ACTIVATE_SUB_INSUFFICIENT_FUNDS_ERROR': (
        'На балансе организации не достаточно средств!!!',
        'Когда пытаемся подключить подключить подписку, но недостаточно средств',
        str,
    ),
    'ORG_ACTIVATE_SUB_ALREADY_HAVE_SUB_ERROR': (
        'Уже есть активная подписка по выбранному тарифу.',
        'Когда пытаемся подключить подключить подписку, которая уже есть',
        str,
    ),
    'TEMPLATE_INVITATION_ALREADY_HAVE_ERROR': (
        'Приглашение уже создано.',
        'Когда создать приглашение к шаблону, которое уже есть',
        str,
    ),
    'TEMPLATE_DESTROY_LAST_TEMPLATE_ERROR': (
        'Невозможно удалить последний шаблон.',
        'Когда пытаемся удалить последний шаблон',
        str,
    ),
    'USER_HAVE_NOT_INSPECTOR_INFO_ERROR': (
        'Не удалось получить инфо инспектора у пользователя.',
        'Когда пытаемся добавить/убрать роль инспектора у пользователя, но ее нет',
        str,
    ),
    'CONFIRM_CODE_PHONE_NOT_FOUND_ERROR': (
        'Такой телефон не существует в системе.',
        'Когда при попытке отправить код подтверждения такой телефон не найдет',
        str,
    ),
    'CONFIRM_CODE_INCORRECT_ERROR': (
        'Неверный код подтверждения.',
        'Когда отправлен неверный код подтверждения',
        str,
    ),
    'CONFIRM_CODE_EXPIRED_ERROR': (
        'Срок действия кода подтверждения истек.',
        'Когда срок действия кода истек',
        str,
    ),
    'INN_INVALID_ERROR': (
        'ИНН невалидный.',
        'Если ИНН невалидный',
        str,
    ),
    'AGREEMENT_PROCESSING_NEED_ERROR': (
        'Необходимо согласие на персональных данных.',
        'Когда требуется согласие на обработку перс. данных',
        str,
    ),
    'AGREEMENT_POLICY_NEED_ERROR': (
        'Необходимо согласие c политикой конфиденциальности.',
        'Когда требуется согласие c политикой конфиденциальности',
        str,
    ),
    'ACCRED_USER_ALREADY_INSPECTOR_ERROR': (
        'За данным пользователем USER уже есть инспектор.',
        'Когда пытаемся создать объект инспектора у пользователя, но он уже есть',
        str,
    ),
    'BIND_REQUISITES_USER_IS_NOT_INSPECTOR_ERROR': (
        'За пользователем USER не закреплен инспектор.',
        'Когда за пользователем не закреплен инспектор',
        str,
    ),
    'BIND_REQUISITES_USER_ALREADY_HAVE_REQUISITES_ERROR': (
        'За пользователем USER уже закреплены реквизиты.',
        'Когда пытаемся привязать реквизиты, но они уже привязаны',
        str,
    ),
    'INSPECTOR_TRANSACTION_INSUFFICIENT_FUNDS_ERROR': (
        'На балансе инспектора не достаточно средств!!!',
        'Когда в транзакции инспектора недостаточно средств',
        str,
    ),
    'ORG_TRANSACTION_INSUFFICIENT_FUNDS_ERROR': (
        'На балансе организации не достаточно средств!!!',
        'Когда в транзакции организации недостаточно средств',
        str,
    ),
}

CONSTANCE_CONFIG_FIELDSETS = {
    'Инфо настройки': (
        'USER_AGREEMENT',
        'POLICY',
        'ABOUT_PLATFORM',
        '404',
    ),
    'Настройки проекта': (
        'SEND_SMS',
        'ENABLE_CHECKING_USER',
        'INSPECTOR_PERCENT',
        'SELF_INSPECTION_PRICE',
        'CONFIRMATION_CODE_EXPIRED_TIME',
        'INSPECTION_TASK_ACTIVITY_TIME',
        'INSPECTION_SEARCHING_TIME',
        'ORG_BALANCE_EMAIL',
    ),
    'Настройки текстов уведомлений': (
        'ASSIGNING_INSPECTION_TO_INSPECTOR',
        'TASK_ACCEPTED_BY_INSPECTOR',
        'INSPECTION_COMPLETE',
        'INSPECTION_ORGANIZATION_INSPECTOR_NEED_FIXES',
        'INSPECTION_SERVICE_INSPECTOR_NEED_FIXES',
        'INSPECTOR_MONEY_CAME',
        'ISSUING_ORG_INSPECTOR',
        'ISSUING_SERVICE_INSPECTOR',
        'SHARE_TEMPLATE',
        'INVITE_ORGANIZATION',
        'ORGANIZATION_BALANCE_MONEY_CAME',
        'INSUFFICIENT_FUNDS',
        'INSPECTOR_ACCR_NEW_FIXES',
        'INSPECTOR_ACCR_SUCC_COMPLETE',
        'CANT_GET_TASK_WITHOUT_REQUISITE',
    ),
    'Настройки текстов ошибок': (
        'ADDRESS_QUERY_AND_LOCATION_TOGETHER_ERROR',
        'CAR_INVALID_GOV_NUM_ERROR',
        'CITY_IMPORT_NEED_XLSX_ERROR',
        'FILE_DB_FILE_NOT_FOUND_ERROR',
        'INSPECTION_NEED_NULL_VALUE_ERROR',
        'INSPECTION_IMPOSSIBLE_BIND_CLIENT_SIGN_ERROR',
        'INSPECTION_IMPOSSIBLE_BIND_INSPECTOR_SIGN_ERROR',
        'TASK_CAR_VALIDATE_SERIAL_NUM_ERROR',
        'TASK_VALIDATE_DATE_ERROR',
        'TASK_NOT_INSPECTOR_SEARCH_BY_TASK_ERROR',
        'TASK_DELETE_CARS_BUT_NON_DRAFT_ERROR',
        'ACCRED_USER_HAVE_REQUEST_ERROR',
        'ORG_INVITATION_USER_IS_MEMBERSHIP_ERROR',
        'ORG_INVITATION_USER_HAVE_INVITE_ERROR',
        'ORG_NOT_FOUND_BY_INN_DADATA_ERROR',
        'ORG_MEMBERSHIP_CANT_LEAVE_LAST_ORG_ERROR',
        'ORG_ACTIVATE_SUB_INSUFFICIENT_FUNDS_ERROR',
        'ORG_ACTIVATE_SUB_ALREADY_HAVE_SUB_ERROR',
        'TEMPLATE_INVITATION_ALREADY_HAVE_ERROR',
        'TEMPLATE_DESTROY_LAST_TEMPLATE_ERROR',
        'USER_HAVE_NOT_INSPECTOR_INFO_ERROR',
        'CONFIRM_CODE_PHONE_NOT_FOUND_ERROR',
        'CONFIRM_CODE_INCORRECT_ERROR',
        'CONFIRM_CODE_EXPIRED_ERROR',
        'INN_INVALID_ERROR',
        'AGREEMENT_PROCESSING_NEED_ERROR',
        'AGREEMENT_POLICY_NEED_ERROR',
        'ACCRED_USER_ALREADY_INSPECTOR_ERROR',
        'BIND_REQUISITES_USER_IS_NOT_INSPECTOR_ERROR',
        'BIND_REQUISITES_USER_ALREADY_HAVE_REQUISITES_ERROR',
        'INSPECTOR_TRANSACTION_INSUFFICIENT_FUNDS_ERROR',
        'ORG_TRANSACTION_INSUFFICIENT_FUNDS_ERROR',
    ),
}
