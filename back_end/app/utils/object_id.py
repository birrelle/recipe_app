from pydantic import BaseModel, Field
from bson import ObjectId
from pydantic.json import ENCODERS_BY_TYPE

# Create a custom type for PyObjectId
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not PyObjectId.is_valid(v):
            raise ValueError("Invalid PyObjectId")
        return PyObjectId(v)

    # @classmethod
    # def __modify_schema__(cls, field_schema):
    #     field_schema.update(type="string")
