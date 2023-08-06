from nazca4sdk.datahandling.hotstorage.helper import transform, create_variables_frame
from nazca4sdk.datahandling.hotstorage.model.user_variable import UserVariable
from nazca4sdk.datahandling.kafka.kafka_sender import KafkaSender


class UserVariableSaver:
    def __init__(self):
        self._kafkaSender = KafkaSender()

    def save_variables(self, user_variables: [UserVariable]) -> bool:
        variables = transform(user_variables)
        if len(variables) == 0:
            return False
        user_variables_frame = create_variables_frame(variables)
        return self._kafkaSender.send_message("dataflow.fct.clickhouse", 'Variables', user_variables_frame)
