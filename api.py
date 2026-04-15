from __future__ import annotations
import enum
from typing import Annotated
from livekit.agents import llm
from db_driver import DatabaseDriver

DB = DatabaseDriver()

class CarDetails(enum.Enum):
    VIN = "vin"
    Make = "make"
    Model = "model"
    Year = "year"

class AssistantFnc(llm.FunctionContext): # En la 1.5 vuelve a estar en llm
    def __init__(self):
        super().__init__()
        self._car_details = {
            CarDetails.VIN: "",
            CarDetails.Make: "",
            CarDetails.Model: "",
            CarDetails.Year: ""
        }
    
    def get_car_str(self):
        return "\n".join([f"{k.value}: {v}" for k, v in self._car_details.items()])
    
    @llm.ai_callable(description="lookup a car by its vin")
    def lookup_car(self, vin: Annotated[str, llm.TypeInfo(description="The vin of the car")]):
        result = DB.get_car_by_vin(vin)
        if not result: return "Car not found"
        self._car_details.update({
            CarDetails.VIN: result.vin, CarDetails.Make: result.make,
            CarDetails.Model: result.model, CarDetails.Year: result.year
        })
        return f"Car details: {self.get_car_str()}"

    def has_car(self):
        return self._car_details[CarDetails.VIN] != ""