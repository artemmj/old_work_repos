help_text = """

        condition - enum: ['equal', 'lt', 'gt', 'lte', 'gte']

        [
            {
                sku_group: {
                    skues: [
                        str uuid,
                        ...
                    ] - инфа по ску, может быть только одно ску
                    category: str - название категории, опционально
                },
                planogram: {
                    id: str uuid - id файла
                    file: str - url файла
                }
                question_group:{
                    name: - название блока
                    questions:[
                        {
                            question_id: str uuid - у вопроса для перехода на следующий экран is_condition=True
                            answer_id: str uuid - id ответа
                            availability_choices: [str uuid, ...]
                                - список возможного выбора для вопросов с типом availability
                            sku_id: str uuid - id sku для вопроса с типом availability
                        }
                        ...
                    ] - описание вопросов
                }
                condition: {
                    type: condition - тип условия
                    value: тип зависит от типа вопроса
                }, - может быть null, тогда вопрос безусловный (null в корневом элементе),
                paths:  [
                    {...} - такая же структура как в корневом элементе
                    ...
                ] - множество экранов для перехода
            }
            ...
        ]
        """
