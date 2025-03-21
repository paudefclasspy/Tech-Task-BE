import decimal
from django.db import models
from decimal import Decimal
from datetime import date

class Invoice(models.Model):
    # estos campos son la info básica de la factura
    # no cambies los decimal_places o todo explota! 💥
    adjusted_gross_value = models.DecimalField(max_digits=15, decimal_places=2)
    haircut_percent = models.DecimalField(max_digits=5, decimal_places=2)
    daily_advance_fee = models.DecimalField(max_digits=5, decimal_places=4)
    
    # default is 30 days pero se puede cambiar si el cliente lo pide
    # just don't make it too long or risk team gets angry 😤
    advance_duration = models.IntegerField(default=30)
    
    # basic customer info - we need this for tracking and reporting
    # keep these fields clean or the dashboard looks like 💩
    customer_name = models.CharField(max_length=255)
    currency_code = models.CharField(max_length=3)  # usd, eur, etc - keep it standard!
    customer_id = models.IntegerField()
    revenue_source_id = models.IntegerField()
    revenue_source_name = models.CharField(max_length=255)
    invoice_date = models.DateField(default=date.today)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            # this makes queries super fast
            # trust me, without this index everything dies ⚰️
            models.Index(fields=['customer_id', 'created_at']),
        ]
        ordering = ['-created_at']  # newest first, duh!

    def calculate_loan_details(self):
        """Calculate loan details based on invoice data."""
        try:
            # ¡Ojo! Todos los cálculos deben ser con Decimal para evitar errores de redondeo
            hundred = Decimal('100')
            zero = Decimal('0')
            
            # Si algo es cero o negativo, mejor return early con todo en cero
            # (nos ahorramos dolores de cabeza después)
            if self.adjusted_gross_value <= zero or self.advance_duration <= 0:
                return {
                    'haircut_amount': zero,
                    'advance_amount': zero,
                    'daily_fee_amount': zero,
                    'expected_fees': zero,
                    'apr': zero,
                    'advance_duration': self.advance_duration
                }
            
            # Calculate haircut amount
            haircut_amount = self.adjusted_gross_value * (self.haircut_percent / hundred)
            
            # Calculate advance amount (adjusted gross value minus haircut)
            advance_amount = self.adjusted_gross_value - haircut_amount
            
            # Calculate daily fee amount
            daily_fee_amount = advance_amount * self.daily_advance_fee / hundred
            
            # Calculate total expected fees
            expected_fees = daily_fee_amount * Decimal(str(self.advance_duration))
            
            # Calculate APR (Annual Percentage Rate)
            # APR = (Total Fee / Advance Amount) * (365 / Advance Duration) * 100
            if advance_amount > zero:
                apr = (expected_fees / advance_amount) * (Decimal('365') / Decimal(str(self.advance_duration))) * hundred
            else:
                apr = zero
            
            return {
                'haircut_amount': round(haircut_amount, 2),
                'advance_amount': round(advance_amount, 2),
                'daily_fee_amount': round(daily_fee_amount, 2),
                'expected_fees': round(expected_fees, 2),
                'apr': round(apr, 2),
                'advance_duration': self.advance_duration
            }
        except (decimal.DivisionByZero, decimal.InvalidOperation):
            # Return all zeros if any calculation fails
            return {
                'haircut_amount': Decimal('0'),
                'advance_amount': Decimal('0'),
                'daily_fee_amount': Decimal('0'),
                'expected_fees': Decimal('0'),
                'apr': Decimal('0'),
                'advance_duration': self.advance_duration
            }









