from django.db import models


class Application(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('interview', 'Interview'),
        ('offer', 'Offer'),
        ('rejected', 'Rejected'),
    ]

    company = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    applied_date = models.DateField()
    job_link = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role} at {self.company}"
    
    notes = models.TextField(blank=True)
    salary = models.IntegerField()        # <-- add this line
    created_at = models.DateTimeField(auto_now_add=True)
    salary = models.IntegerField(null=True, blank=True)