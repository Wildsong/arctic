import strawberry
from datetime import datetime

@strawberry.type
class Ping:
    timestamp: datetime

@strawberry.type
class Licenses:
    id: int
    product: str
    user: str
    checkout: str

def get_ping() -> Ping:
    now = datetime.now()
    return Ping(
         timestamp = now
    )

def get_licenses() -> list[Licenses]:
    return [
        Licenses(
            id=0,
            product="ArcMap",
            user="User 1",
            checkout="2023-07-04",
        )
    ]

@strawberry.type
class Query:
    ping: Ping = strawberry.field(resolver=get_ping)
    licenses: list[Licenses] = strawberry.field(resolver=get_licenses)

schema = strawberry.Schema(query=Query)
