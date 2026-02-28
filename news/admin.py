import base64
import io
import os

import matplotlib
matplotlib.use('Agg')   # MUST be before any other matplotlib import
import matplotlib.pyplot as plt

from django.conf import settings
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import path, reverse

from .models import AnalysisResult, Dataset, ModelMetrics, NewsArticle


# ─────────────────────────────────────────────────────────────────────────────
#  Helper — metrics chart
# ─────────────────────────────────────────────────────────────────────────────

def _generate_metrics_chart(metrics_qs) -> str:
    """
    TODO(human) — implement the metrics visualisation function below.

    Steps:
      1. If the queryset is empty, return an empty string ''
      2. Extract four lists from metrics_qs (iterate, each object has
         .accuracy .precision .recall .f1_score .trained_at):
            labels     = [m.trained_at.strftime('%m/%d %H:%M') for m in metrics_qs]
            accuracies = [m.accuracy   for m in metrics_qs]
            precisions = [m.precision  for m in metrics_qs]
            recalls    = [m.recall     for m in metrics_qs]
            f1s        = [m.f1_score   for m in metrics_qs]
      3. Create figure:  fig, ax = plt.subplots(figsize=(10, 5))
      4. Plot four lines (use ax.plot):
            ax.plot(labels, accuracies,  marker='o', label='Accuracy')
            ax.plot(labels, precisions,  marker='s', label='Precision')
            ax.plot(labels, recalls,     marker='^', label='Recall')
            ax.plot(labels, f1s,         marker='D', label='F1-Score')
      5. Style the chart:
            ax.set_ylim(0, 1.05)
            ax.set_xlabel('Training Run')
            ax.set_ylabel('Score')
            ax.set_title('Model Performance Over Time')
            ax.legend()
            fig.tight_layout()
      6. Save to a bytes buffer and encode as base64:
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            encoded = base64.b64encode(buf.read()).decode('utf-8')
      7. Free memory:  plt.close(fig)
      8. Return encoded  (embed in template as <img src="data:image/png;base64,{{ chart }}">)
    """
    pass


# ─────────────────────────────────────────────────────────────────────────────
#  NewsArticle admin
# ─────────────────────────────────────────────────────────────────────────────

@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display  = ['id', 'user', 'short_text', 'submitted_at']
    list_filter   = ['submitted_at']
    search_fields = ['user__username', 'text']
    readonly_fields = ['submitted_at']

    def short_text(self, obj):
        return obj.text[:60] + '…' if len(obj.text) > 60 else obj.text
    short_text.short_description = 'Text Preview'


# ─────────────────────────────────────────────────────────────────────────────
#  AnalysisResult admin
# ─────────────────────────────────────────────────────────────────────────────

@admin.register(AnalysisResult)
class AnalysisResultAdmin(admin.ModelAdmin):
    list_display  = ['id', 'article', 'verdict', 'confidence_score', 'analyzed_at']
    list_filter   = ['verdict', 'analyzed_at']
    search_fields = ['article__user__username']
    readonly_fields = ['analyzed_at']


# ─────────────────────────────────────────────────────────────────────────────
#  Dataset admin
# ─────────────────────────────────────────────────────────────────────────────

@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display  = ['filename', 'uploaded_by', 'uploaded_at']
    readonly_fields = ['uploaded_at']
    search_fields = ['filename']

    def save_model(self, request, obj, form, change):
        obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)


# ─────────────────────────────────────────────────────────────────────────────
#  ModelMetrics admin  (with custom "Retrain" button)
# ─────────────────────────────────────────────────────────────────────────────

@admin.register(ModelMetrics)
class ModelMetricsAdmin(admin.ModelAdmin):
    list_display    = ['accuracy', 'precision', 'recall', 'f1_score', 'trained_at']
    readonly_fields = ['accuracy', 'precision', 'recall', 'f1_score', 'trained_at']
    change_list_template = 'admin/news/modelmetrics/change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('retrain/', self.admin_site.admin_view(self.retrain_view), name='retrain_model'),
        ]
        return custom_urls + urls

    def retrain_view(self, request):
        if request.method != 'POST':
            return HttpResponseRedirect(
                reverse('admin:news_modelmetrics_changelist')
            )

        dataset_dir = str(settings.MEDIA_ROOT)
        model_dir   = str(settings.ML_MODEL_DIR)

        try:
            from ml.trainer import train_model
            metrics = train_model(dataset_dir, model_dir)
            ModelMetrics.objects.create(**metrics)
            self.message_user(
                request,
                f'Model retrained successfully! '
                f'Accuracy: {metrics["accuracy"]:.1%}  |  '
                f'F1: {metrics["f1_score"]:.1%}',
                messages.SUCCESS
            )
        except FileNotFoundError as e:
            self.message_user(request, str(e), messages.ERROR)
        except Exception as e:
            self.message_user(request, f'Training failed: {e}', messages.ERROR)

        return HttpResponseRedirect(
            reverse('admin:news_modelmetrics_changelist')
        )

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        metrics_qs = ModelMetrics.objects.order_by('trained_at')
        extra_context['chart'] = _generate_metrics_chart(metrics_qs)
        return super().changelist_view(request, extra_context=extra_context)
