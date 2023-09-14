from typing import List, Union
import datetime
from dataclasses import dataclass
from .key import Key

@dataclass
class JobOffer:
    company: Key
    _id: Key
    title: str
    description: str
    pay: int
    begin_date: datetime.date = None
    end_date: datetime.date = None
    interviewer: Key = None
    developer_interested: bool = False

    company_name: str = None
    interviewer_name: str = None