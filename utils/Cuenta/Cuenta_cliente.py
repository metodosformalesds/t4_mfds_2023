from datetime import datetime

from utils.Cuenta.Cuenta import Cuenta


class Cuenta_Cliente(Cuenta):
    def __init__(self, name: str, C_negocio: str) -> None:
        super().__init__()
        self.__table_name = 'UACJ-PAY_Cuenta_Cliente'
        self.propietario = name
        self.CLABE_negocio = C_negocio
    
    def get_variable_names(self):
        item = {
                'CLABE': self.get_CLABE(),
                'num_tarjeta': self.num_tarjeta,
                'CSV': self.get_CVC(),
                'fecha_vencimiento': self.fecha_vencimiento,
                'created': self.created,
                'propietario': self.propietario.split(),
                'pais': self.pais,
                'CLABE_negocio': self.CLABE_negocio
            }
        return item
    
    def create_cliente(self):
        try:
            item = {
                'CLABE': {'N': self.get_CLABE()},
                'num_tarjeta': {'S': self.num_tarjeta},
                'CSV': {'S': self.get_CVC()},
                'fecha_vencimiento': {'S': self.fecha_vencimiento},
                'created': {'S': self.created},
                'propietario': {'SS': self.propietario.split()},
                'pais': {'S': self.pais},
                'CLABE_negocio': {'N': self.CLABE_negocio}
            }
            
            self.client.put_item(TableName=self.__table_name, Item=item)
            
        except Exception as e:
            print(e)
        