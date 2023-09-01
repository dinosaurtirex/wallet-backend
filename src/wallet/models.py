from tortoise import fields
from tortoise.models import Model


class Balance(Model):

    id          = fields.IntField(pk=True)
    currency    = fields.CharField(max_length=64, null=False)
    amount      = fields.FloatField(null=False)
    tag         = fields.CharField(max_length=128, null=True)
    description = fields.TextField(null=True)
    owner       = fields.ForeignKeyField("models.User")
    added_at    = fields.DatetimeField(auto_now_add=True)

    async def serialize(self) -> dict:
        return {
            "id":          self.id,
            "currency":    self.currency,
            "amount":      self.amount,
            "tag":         self.tag,
            "description": self.description,
            "added_at":    str(self.added_at)
        }