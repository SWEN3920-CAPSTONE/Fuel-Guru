import decimal
import json

from config import (AmenityTagSchema, AmenityTypeSchema,
                    GasPriceSuggestionSchema,
                    GasStationSchema, GasTypeSchema, PostTypeSchema,
                    PromotionSchema, ReviewSchema, UserSchema,
                    UserTypeSchema, AmenityTag, AmenityType, GasPriceSuggestion,
                    GasType, PostType, Promotion, Review, GasStation, User, UserType)


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)


def to_dump(data, file):
    json.dump(data, file, indent='\t', cls=DecimalEncoder)


base = 'model/example_outputs'

schemas_types = [(UserSchema, User, 59, 62),
                 (AmenityTypeSchema, AmenityType, 0, 2),
                 (PromotionSchema, Promotion, 0, 2),
                 (GasTypeSchema, GasType, 0, 2),
                 (GasPriceSuggestionSchema, GasPriceSuggestion, 7, 90),
                 (AmenityTagSchema, AmenityTag, 0, 5),
                 (PostTypeSchema, PostType, 0, 2),
                 (UserTypeSchema, UserType, 0, 2),
                 (ReviewSchema, Review, 645, 649),
                 (GasStationSchema, GasStation, 6, 8)
                 ]

for MSchema, MType, start, end in schemas_types:
    with open(f'{base}/{MSchema.__name__.lower()}_{MType.__name__.lower()}.json', 'w') as file:
        to_dump(MSchema(many=True).dump(MType.query.all()[start:end]), file)
