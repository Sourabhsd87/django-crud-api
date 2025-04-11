from django.db import models
from django.db.models.fields import DateTimeField
import uuid


# -------------------------------------------------------------------------------
# ModelAbstractBase
# -------------------------------------------------------------------------------
class ModelAbstractBase(models.Model):
    """
    Abstract base model.
    """

    created_on = DateTimeField(
        auto_now_add=True,
        help_text="Date and time when this entry was created in the system",
    )

    updated_on = DateTimeField(
        auto_now=True,
        help_text=("Date and time when the table data was last updated in the system"),
    )
    internal_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        help_text="Unique identification number for the table.",
        primary_key=True,
    )

    is_active = models.BooleanField(default=True, help_text="Is active?")

    # ---------------------------------------------------------------------------
    # Meta
    # ---------------------------------------------------------------------------
    class Meta:
        abstract = True
