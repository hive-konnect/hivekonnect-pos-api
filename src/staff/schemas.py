
class StaffCreate:   
    shop_id: str
    user_id: str
    role: str
    display_name: str

class StaffResponse:
    id: str
    shop_id: str
    user_id: str
    role: str
    display_name: str

    class Config:
        from_attributes = True