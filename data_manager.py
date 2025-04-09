import json
import os
from typing import Dict, List, Optional


class DataManager:
    def __init__(self, data_file="disaster_data.json"):
        self.data_file = data_file
        self.fallecidos = []
        self.pacientes_hospitales = {}
        self.load_data()

    def load_data(self):
        """Cargar datos desde el archivo JSON si existe"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    self.fallecidos = data.get("fallecidos", [])
                    self.pacientes_hospitales = data.get("pacientes_hospitales", {})
            else:
                # Datos iniciales si no existe el archivo
                self.fallecidos = [
                    "Andrés Pichardo", "Aneuris Viña", "Carolina Pérez Flores",
                    "Cheila Berroa", "Daniel Taveras Polanco", "Diego Armando Severino",
                    "Élva Gálvez", "Génesis de León", "Héctor Bienvenido Peguero Ramírez",
                    "Indira Disla Méndez", "Lorenzo Ricardo", "Lourdes Ricard",
                    "Luis Emilio Solís", "María Isabel Guerrero", "Nelsy Milagros Cruz",
                    "Nidia Carolina Solano", "Paulino Lorenzo", "Pedro Cepeda",
                    "Ramón Alberto Santana Benítez", "Randy Alexander Rodríguez",
                    "Vianka Reyes", "Julio Cesar Valera", "Aracelis Rodríguez",
                    "Cesar López Gronell", "Desnaud Wilmord", "Fray Luis Rosario",
                    "Isabel Betania Cabrera", "Miguel Ángel Pérez Suarez",
                    "Nelsida Sánchez", "Ruth Delania Santana", "Tony Enrique Blanco Cabrera",
                    "Yaris Francisco Holguin Arias"
                ]
                self.pacientes_hospitales = {
                    "Hospital Darío Contreras": [
                        {"nombre": "Giselle Guerrero", "edad": 35},
                        {"nombre": "Pedro Espinal"},
                        {"nombre": "Ruddy Alonzo", "edad": 44},
                        {"nombre": "Viviana Díaz", "edad": 34},
                        {"nombre": "Marisol Chalas", "edad": 58},
                        {"nombre": "Pamela Montoya", "edad": 33},
                        {"nombre": "Douglas García", "edad": 42},
                        {"nombre": "Carlos Martínez", "edad": 42},
                        {"nombre": "Carolina Rodríguez", "edad": 43},
                        {"nombre": "Elianta Quintero"},
                        {"nombre": "José Candelario", "edad": 55},
                        {"nombre": "Jonathan Natera"},
                        {"nombre": "Katherine Coronado"},
                        {"nombre": "Lucía Castilla", "edad": 43},
                        {"nombre": "Ingrid Reyes", "edad": 64},
                        {"nombre": "Giselle Ogando"},
                        {"nombre": "Víctor de la Cruz", "edad": 67},
                        {"nombre": "Martin Bautista", "edad": 50},
                        {"nombre": "Simeón Mueses", "edad": 42},
                        {"nombre": "Manuela Vólquez"},
                        {"nombre": "Evelin Mariela Navarro de León", "edad": 35}
                    ],
                    "Hospital Marcelino Vélez Santana": [
                        {"nombre": "Milagros Acosta", "edad": 27},
                        {"nombre": "Christian Marques", "edad": 40},
                        {"nombre": "Marla Urbáez", "edad": 21},
                        {"nombre": "Karla Sánchez", "edad": 31},
                        {"nombre": "Ricardo Archstore Lir"},
                        {"nombre": "Juliana V. Castillo Vargas"},
                        {"nombre": "Ivelisse Reynoso", "edad": 53},
                        {"nombre": "Ricardo Gilbert Julián", "edad": 59},
                        {"nombre": "Jorge Santana"},
                        {"nombre": "Brenda Ortega"}
                    ],
                    "Hospital Vinicio Calventi": [
                        {"nombre": "Víctor Manuel de la Cruz", "edad": 67}
                    ],
                    "Hospital Ney Arias Lora": [
                        {"nombre": "Kevin Patricio", "edad": 42},
                        {"nombre": "Elena Almánzar", "edad": 49},
                        {"nombre": "Danilda Amado Figueroa", "edad": 31},
                        {"nombre": "Héctor Brito", "edad": 34},
                        {"nombre": "Jesús Ramírez", "edad": 35},
                        {"nombre": "Dominicana Acosta", "edad": 48},
                        {"nombre": "Feliz Manuel Soto", "edad": 53},
                        {"nombre": "Elsa Espinal Arias", "edad": 31},
                        {"nombre": "Rosbely Pérez", "edad": 45},
                        {"nombre": "Ana Montero", "edad": 32},
                        {"nombre": "Juan Arturo Soto", "edad": 48},
                        {"nombre": "Germán Jorge", "edad": 38},
                        {"nombre": "Geraldine Bastardo", "edad": 37},
                        {"nombre": "José Abreu Santana", "edad": 26},
                        {"nombre": "Gilberto Encarnación", "edad": 36},
                        {"nombre": "Jenine Mena", "edad": 40},
                        {"nombre": "Luis Alberto Saavedra", "edad": 56},
                        {"nombre": "Alba Montero", "edad": 33},
                        {"nombre": "Victor Manuel Rodríguez", "edad": 31},
                        {"nombre": "Anny Montero"},
                        {"nombre": "Lenin Manuel Díaz"},
                        {"nombre": "Félix Soto", "edad": 53},
                        {"nombre": "Moisés Torres Pión", "edad": 31},
                        {"nombre": "Francisco Aurelio Martínez", "edad": 44},
                        {"nombre": "Alba María Rojas", "edad": 44},
                        {"nombre": "Danilda Figueroa", "edad": 29}
                    ],
                    "Hospital Moscoso Puello": [
                        {"nombre": "Yaitza Marín", "edad": 56}
                    ],
                    "Hospital Salvador B. Gautier": [
                        {"nombre": "Jennifer Taveras", "edad": 24},
                        {"nombre": "Carlos Rolando Cepín Martínez", "edad": 38},
                        {"nombre": "Bartolo Reyes", "edad": 55}
                    ]
                }
                self.save_data()
        except Exception as e:
            print(f"Error al cargar datos: {e}")

    def save_data(self):
        """Guardar datos en archivo JSON"""
        data = {
            "fallecidos": self.fallecidos,
            "pacientes_hospitales": self.pacientes_hospitales
        }
        with open(self.data_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    def check_fallecido_exists(self, nombre: str) -> bool:
        """Verificar si un fallecido ya existe en la lista"""
        return nombre in self.fallecidos

    def add_fallecido(self, nombre: str) -> bool:
        """Añadir un nuevo fallecido a la lista"""
        if self.check_fallecido_exists(nombre):
            return False

        # Verificar si la persona está en algún hospital
        for hospital, pacientes in self.pacientes_hospitales.items():
            for i, paciente in enumerate(pacientes):
                if paciente["nombre"] == nombre:
                    # Eliminar de la lista de pacientes
                    pacientes.pop(i)
                    break

        self.fallecidos.append(nombre)
        self.save_data()
        return True

    def check_paciente_exists(self, nombre: str) -> Dict:
        """Verificar si un paciente ya existe en algún hospital"""
        for hospital, pacientes in self.pacientes_hospitales.items():
            for paciente in pacientes:
                if paciente["nombre"] == nombre:
                    return {"exists": True, "hospital": hospital}

        # Verificar si está en la lista de fallecidos
        if nombre in self.fallecidos:
            return {"exists": True, "fallecido": True}

        return {"exists": False}

    def add_paciente(self, nombre: str, hospital: str, edad: Optional[int] = None) -> Dict:
        """Añadir un nuevo paciente a un hospital"""
        check = self.check_paciente_exists(nombre)

        if check.get("exists"):
            if check.get("fallecido"):
                return {"success": False, "message": "La persona está en la lista de fallecidos"}
            return {"success": False, "message": f"El paciente ya existe en {check.get('hospital')}"}

        # Crear el nuevo paciente
        nuevo_paciente = {"nombre": nombre}
        if edad:
            nuevo_paciente["edad"] = edad

        # Añadir el paciente al hospital
        if hospital not in self.pacientes_hospitales:
            self.pacientes_hospitales[hospital] = []

        self.pacientes_hospitales[hospital].append(nuevo_paciente)
        self.save_data()
        return {"success": True}

    def get_all_data(self) -> Dict:
        """Obtener todos los datos"""
        return {
            "fallecidos": self.fallecidos,
            "pacientes_hospitales": self.pacientes_hospitales
        }

    def get_data_for_model(self) -> str:
        """Obtener datos formateados para enviar al modelo"""
        data_text = "Lista de fallecidos confirmados:\n"
        for fallecido in self.fallecidos:
            data_text += f"- {fallecido}\n"

        data_text += "\nPacientes en hospitales:\n"
        for hospital, pacientes in self.pacientes_hospitales.items():
            data_text += f"\n{hospital}:\n"
            for paciente in pacientes:
                if 'edad' in paciente:
                    data_text += f"- {paciente['nombre']}, {paciente['edad']} años\n"
                else:
                    data_text += f"- {paciente['nombre']}\n"

        return data_text