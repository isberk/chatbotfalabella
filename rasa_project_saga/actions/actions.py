from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

# ====================================================================
# SIMULACIÓN DE BASES DE DATOS DE FALABELLA
# ====================================================================

PEDIDOS_DB = {
    "123456": {
        "estado": "En tránsito",
        "fecha_entrega": "2025-12-05",
        "producto": "Smart TV Samsung 50\"",
        "cliente": "Carlos Morón"
    },
    "987654": {
        "estado": "Entregado",
        "fecha_entrega": "2025-11-20",
        "producto": "Juego de sábanas",
        "cliente": "Isabel Villanueva"
    },
    "101010": {
        "estado": "Pendiente de pago",
        "fecha_entrega": "N/A",
        "producto": "Laptop Gamer ASUS",
        "cliente": "Steven Lara"
    }
}

PRODUCTOS_DB = {
    "laptops": {
        "stock": "Disponible en todas las tiendas y en línea",
        "promocion": "15% de descuento con CMR hasta fin de mes."
    },
    "zapatillas": {
        "stock": "Stock limitado en tallas grandes",
        "promocion": "Envío gratis a Lima Metropolitana."
    },
    "smart tv": { 
        "stock": "Agotado en línea, disponible en tienda de Jockey Plaza.",
        "promocion": "Sin promociones activas."
    },
    "ropa": {
        "stock": "Amplio stock en categorías de invierno",
        "promocion": "3x2 en marcas seleccionadas."
    },
    "lavadora": { 
        "stock": "Disponible para entrega en 72 horas.",
        "promocion": "12 cuotas sin intereses con tarjeta CMR."
    },
    "zapatos": { 
        "stock": "Amplio stock en todas las tallas.",
        "promocion": "10% de descuento en la segunda unidad."
    }
}


# ====================================================================
# ACCIÓN 1: CONSULTAR ESTADO DE PEDIDO
# ====================================================================
class ActionConsultarPedido(Action):

    def name(self) -> Text:
        return "action_consultar_pedido"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        numero_pedido = next(tracker.get_latest_entity_values("numero_pedido"), None)
        
        if not numero_pedido:
            dispatcher.utter_message(template="utter_ask_pedido")
            return []
            
        pedido_info = PEDIDOS_DB.get(numero_pedido)

        if pedido_info:
            estado = pedido_info["estado"]
            fecha = pedido_info["fecha_entrega"]
            producto = pedido_info["producto"]
            cliente = pedido_info["cliente"]
            
            mensaje = (
                f"Hola {cliente}, he verificado tu pedido {numero_pedido} ({producto}):\n"
                f"- Estado actual: {estado}.\n"
                f"- Fecha estimada de entrega: {fecha}."
            )
            dispatcher.utter_message(text=mensaje)
            
        else:
            dispatcher.utter_message(text=f"Lo siento, no encuentro un pedido con el número {numero_pedido}. Por favor, verifica el número e intenta de nuevo.")

        return [SlotSet("numero_pedido", None)] 


class ActionConsultarStock(Action):

    def name(self) -> Text:
        return "action_consultar_stock"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        producto = next(tracker.get_latest_entity_values("producto"), None)

        if producto:
            producto = producto.lower()

        if not producto:
            dispatcher.utter_message(template="utter_ask_producto")
            return []

        producto_info = PRODUCTOS_DB.get(producto)

        if producto_info:
            stock = producto_info["stock"]
            promocion = producto_info["promocion"]

            mensaje = (
                f"Aquí tienes la información para {producto.title()}:\n"
                f"- Disponibilidad: {stock}.\n"
                f"- Promoción: {promocion}."
            )
            dispatcher.utter_message(text=mensaje)

        else:
            dispatcher.utter_message(text=f"Actualmente no tengo información detallada para {producto.title()}. ¿Puedo ayudarte con otra categoría?")

        return [SlotSet("producto", None)]
