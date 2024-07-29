from django.db import models

class RiskAssessment(models.Model):
    field1 = models.CharField(max_length=100, default='default_value1')
    field2 = models.CharField(max_length=100, default='default_value2')
    field3 = models.CharField(max_length=100, default='default_value3')
    field4 = models.CharField(max_length=100, default='default_value4')
    field5 = models.CharField(max_length=100, default='default_value5')
    field6 = models.CharField(max_length=100, default='default_value6')
    field7 = models.CharField(max_length=100, default='default_value7')
    field8 = models.CharField(max_length=100, default='default_value8')

    def __str__(self):
        return self.field1

class Control(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    EFFECTIVENESS_CHOICES = [
        ('very_effective', 'Very Effective'),
        ('effective', 'Effective'),
        ('somewhat_effective', 'Somewhat Effective'),
        ('ineffective', 'Ineffective'),
    ]
    effectiveness = models.CharField(max_length=20, choices=EFFECTIVENESS_CHOICES)

    def __str__(self):
        return self.name

class AssessmentControl(models.Model):
    risk_assessment = models.ForeignKey(RiskAssessment, on_delete=models.CASCADE)
    control = models.ForeignKey(Control, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.risk_assessment.field1} - {self.control.name}"
