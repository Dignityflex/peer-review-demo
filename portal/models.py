from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Paper(models.Model):
    title = models.CharField(max_length=255)
    abstract = models.TextField()
    category = models.CharField(max_length=100)
    pdf_url = models.URLField(blank=True, help_text="Link to external PDF or Google Drive")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='papers')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Review(models.Model):
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('paper', 'reviewer')  # Prevents duplicate reviews from the same person

    def __str__(self):
        return f"{self.reviewer.username} on {self.paper.title} ({self.score}/5)"