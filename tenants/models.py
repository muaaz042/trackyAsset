from django.db import models
from django.utils.translation import gettext_lazy as _

class Tenant(models.Model):
    company_name = models.CharField(max_length=255)
    business_name = models.CharField(max_length=255)
    address = models.TextField()
    
    # Tax and Legal
    ntn_number = models.CharField(max_length=50, unique=True, verbose_name=_("NTN Number"))
    ntn_expiry_date = models.DateField(verbose_name=_("NTN Expiry Date"))
    
    # Subscription
    subscription_expiry_date = models.DateField()
    
    # Asset Encoding Config
    tenant_prefix = models.CharField(
        max_length=10, 
        unique=True, 
        help_text=_("Unique prefix used for asset encoding (e.g., 'ABC').")
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Tenant")
        verbose_name_plural = _("Tenants")

    def __str__(self):
        return f"{self.company_name} ({self.tenant_prefix})"