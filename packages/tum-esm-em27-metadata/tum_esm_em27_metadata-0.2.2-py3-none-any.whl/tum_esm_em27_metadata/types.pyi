from pydantic import BaseModel
from typing import Literal

class Location(BaseModel):
    location_id: str
    details: str
    lon: float
    lat: float
    alt: float
    class Config:
        extra: str

class SensorUTCOffset(BaseModel):
    from_date: str
    to_date: str
    utc_offset: float
    class Config:
        extra: str

class SensorPressureCalibrationFactor(BaseModel):
    from_date: str
    to_date: str
    factor: float
    class Config:
        extra: str

class SensorDifferentPressureDataSource(BaseModel):
    from_date: str
    to_date: str
    source: str
    class Config:
        extra: str

class SensorLocation(BaseModel):
    from_date: str
    to_date: str
    location_id: str
    class Config:
        extra: str

class Sensor(BaseModel):
    sensor_id: str
    serial_number: int
    utc_offsets: list[SensorUTCOffset]
    different_pressure_data_source: list[SensorDifferentPressureDataSource]
    pressure_calibration_factors: list[SensorPressureCalibrationFactor]
    locations: list[SensorLocation]
    class Config:
        extra: str

class CampaignStation(BaseModel):
    sensor_id: str
    default_location_id: str
    direction: Literal['north', 'east', 'south', 'west', 'center']
    class Config:
        extra: str

class Campaign(BaseModel):
    campaign_id: str
    from_date: str
    to_date: str
    stations: list[CampaignStation]
    class Config:
        extra: str

class SensorDataContext(BaseModel):
    sensor_id: str
    serial_number: int
    utc_offset: float
    pressure_data_source: str
    pressure_calibration_factor: float
    date: str
    location: Location
    class Config:
        extra: str
