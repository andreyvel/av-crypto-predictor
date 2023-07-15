import datetime
import dataclasses
import json


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if dataclasses.is_dataclass(obj):
            dct = dataclasses.asdict(obj)
            for k, v in dct.items():
                if isinstance(v, datetime.date):
                    v = v.replace(microsecond=0)
                    dct[k] = v.isoformat()

            return dct

        return super().default(obj)
