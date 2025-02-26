from apps.helpers.services import AbstractService


class DocumentStatisticBlockService(AbstractService):
    def __init__(self, serializer_data) -> None:
        self.serializer_data = serializer_data

    def process(self):
        list_cs = []
        cs_sum = 0
        cs_aver = 0

        for doc in self.serializer_data:
            cs = doc.get('counter_scan')
            if cs:
                list_cs.append(doc.get('counter_scan'))

        if list_cs:
            cs_sum = sum(list_cs)
            cs_aver = cs_sum / len(list_cs)

        return {
            'docs_count': len(self.serializer_data),
            'count_sum': round(cs_sum, 3),
            'count_aver': round(cs_aver, 3),
        }
