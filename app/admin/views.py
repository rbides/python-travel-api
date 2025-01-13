from sqladmin import ModelView

from app.database.models.travel import TravelEntity


class TravelAdmin(ModelView, model=TravelEntity):
    column_list = [
        TravelEntity.id,
        TravelEntity.name,
        TravelEntity.destination,
        TravelEntity.price,
        TravelEntity.departure,
        TravelEntity.created_at,
        TravelEntity.updated_at,
    ]


# If we wanted to use a view for User table,
# check this link
# https://aminalaee.dev/sqladmin/cookbook/working_with_passwords/
