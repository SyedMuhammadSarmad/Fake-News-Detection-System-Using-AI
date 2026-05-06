from django.conf import settings
from django.db import models


class NewsArticle(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='articles'
    )
    text = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f'Article #{self.pk} by {self.user.username}'

    def short_text(self):
        return self.text[:80] + '...' if len(self.text) > 80 else self.text


class AnalysisResult(models.Model):
    article = models.OneToOneField(
        NewsArticle,
        on_delete=models.CASCADE,
        related_name='result'
    )
    verdict = models.CharField(max_length=10)          # 'Real' or 'Fake'
    confidence_score = models.FloatField()              # 0.0 – 100.0
    analyzed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.verdict} ({self.confidence_score:.1f}%) — Article #{self.article_id}'

    


class Dataset(models.Model):
    filename = models.CharField(max_length=255)
    file = models.FileField(upload_to='',blank=True,null=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='uploaded_datasets'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.filename


class ModelMetrics(models.Model):
    accuracy = models.FloatField()
    precision = models.FloatField()
    recall = models.FloatField()
    f1_score = models.FloatField()
    trained_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-trained_at']
        verbose_name = 'Model Metrics'
        verbose_name_plural = 'Model Metrics'

    @property
    def accuracy_pct(self):
        return round(self.accuracy * 100, 1)

    @property
    def precision_pct(self):
        return round(self.precision * 100, 1)

    @property
    def recall_pct(self):
        return round(self.recall * 100, 1)

    @property
    def f1_pct(self):
        return round(self.f1_score * 100, 1)

    def __str__(self):
        return (
            f'Acc={self.accuracy:.3f} P={self.precision:.3f} '
            f'R={self.recall:.3f} F1={self.f1_score:.3f} '
            f'@ {self.trained_at.strftime("%Y-%m-%d %H:%M")}'
        )


class UsageReport(AnalysisResult):
    """Proxy model — gives Usage Reports its own admin page (no extra DB table)."""
    class Meta:
        proxy = True
        verbose_name        = 'Usage Report'
        verbose_name_plural = 'Usage Reports'
