import os
import uuid
from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.db.models import Sum, Q, F
from django.db.models.functions import Coalesce

def food_photo_upload_path(instance, filename):
    """
    Generates a secure, randomized UUID-based upload path for food photographs,
    preventing file collisions, path traversal, and enumeration.
    """
    ext = os.path.splitext(filename)[1].lower()
    now = timezone.now()
    return f"food_photos/{now.strftime('%Y/%m')}/{uuid.uuid4().hex}{ext}"


class FoodListing(models.Model):
    """
    Core Food Listing model representing food donations posted by Donors.
    Statuses kept simple: available, claimed, completed, expired.
    """
    STATUS_AVAILABLE = 'available'
    STATUS_CLAIMED = 'claimed'
    STATUS_COMPLETED = 'completed'
    STATUS_EXPIRED = 'expired'

    STATUS_CHOICES = [
        (STATUS_AVAILABLE, 'Available'),
        (STATUS_CLAIMED, 'Claimed'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_EXPIRED, 'Expired'),
    ]

    donor = models.ForeignKey(
        'accounts.Donor',
        on_delete=models.CASCADE,
        related_name='listings'
    )
    location = models.ForeignKey(
        'locations.Location',
        on_delete=models.PROTECT,
        related_name='listings'
    )
    food_name = models.CharField(max_length=200, help_text="e.g. Cooked Rice & Curry, Fresh Apples, Bread Rolls")
    description = models.TextField(blank=True, null=True, help_text="Preparation details, ingredients, or dietary info")
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Total initial quantity"
    )
    unit = models.CharField(
        max_length=50,
        help_text="Units: portions, kg, boxes, packets, meals, litres"
    )
    expires_at = models.DateTimeField(
        db_index=True,
        help_text="Exact expiry deadline"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_AVAILABLE,
        db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Food Listing"
        verbose_name_plural = "Food Listings"
        ordering = ['expires_at']
        indexes = [
            models.Index(fields=['status', 'expires_at'], name='listing_stat_exp_idx'),
        ]

    def __str__(self):
        return f"{self.food_name} ({self.quantity} {self.unit}) - {self.get_status_display()}"

    @classmethod
    def with_annotated_quantities(cls, queryset=None):
        """
        Annotates a FoodListing queryset with _claimed_sum and _annotated_quantity_available
        to eliminate N+1 aggregate queries when rendering listing cards.
        """
        from claims.models import Claim
        now = timezone.now()
        base_qs = queryset if queryset is not None else cls.objects.all()
        claimed_sum = Coalesce(
            Sum(
                'claims__claimed_quantity',
                filter=Q(claims__status=Claim.STATUS_COMPLETED) |
                       Q(claims__status=Claim.STATUS_PENDING, claims__pickup_deadline__gt=now)
            ),
            Decimal('0.00'),
            output_field=models.DecimalField(max_digits=10, decimal_places=2)
        )
        return base_qs.annotate(_claimed_sum=claimed_sum).annotate(
            _annotated_quantity_available=F('quantity') - F('_claimed_sum')
        )

    @classmethod
    def visible_to_recipients(cls):
        """
        Returns only listings that are available and have not passed expiry.
        Optimized with select_related, prefetch_related, and annotated available quantity
        to completely eliminate N+1 queries.
        """
        return cls.with_annotated_quantities(
            cls.objects.filter(
                status=cls.STATUS_AVAILABLE,
                expires_at__gt=timezone.now()
            ).select_related('donor__user', 'location').prefetch_related('photos')
        )

    @property
    def remaining_time(self):
        """
        Calculates remaining duration dynamically (never stored).
        """
        now = timezone.now()
        if self.expires_at > now:
            return self.expires_at - now
        return timezone.timedelta(0)

    @property
    def is_expired(self):
        """
        Returns True if current time has surpassed expires_at or status is expired.
        """
        if self.status == self.STATUS_EXPIRED:
            return True
        return timezone.now() >= self.expires_at

    @property
    def quantity_available(self):
        """
        Calculates available quantity by subtracting completed claims and active pending claims.
        If pre-computed via queryset annotation (_annotated_quantity_available), uses it directly
        to eliminate N+1 queries.
        Expired and cancelled claims do NOT reduce quantity.
        Rounds to exactly 2 decimal places.
        """
        if hasattr(self, '_annotated_quantity_available') and self._annotated_quantity_available is not None:
            remaining = Decimal(str(self._annotated_quantity_available))
            return max(Decimal('0.00'), remaining).quantize(Decimal('0.01'))

        from claims.models import Claim
        now = timezone.now()
        claimed_sum = self.claims.filter(
            Q(status=Claim.STATUS_COMPLETED) |
            Q(status=Claim.STATUS_PENDING, pickup_deadline__gt=now)
        ).aggregate(total=Sum('claimed_quantity'))['total']

        if claimed_sum is None:
            claimed_sum = Decimal('0.00')
        else:
            claimed_sum = Decimal(str(claimed_sum))

        remaining = Decimal(str(self.quantity)) - claimed_sum
        remaining = max(Decimal('0.00'), remaining)
        return remaining.quantize(Decimal('0.01'))

class FoodPhoto(models.Model):
    listing = models.ForeignKey(
        FoodListing,
        on_delete=models.CASCADE,
        related_name='photos'
    )

    image = models.ImageField(
        upload_to=food_photo_upload_path
    )

    caption = models.CharField(
        max_length=200,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at', 'id']

    def __str__(self):
        return f"Photo #{self.pk} - {self.listing.food_name}"