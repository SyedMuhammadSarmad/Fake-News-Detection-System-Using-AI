import csv
import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import NewsSubmissionForm
from .models import AnalysisResult, ModelMetrics, NewsArticle


def _require_verified(request):
    """Return a redirect response if the user is not verified, else None."""
    if not request.user.verified:
        messages.warning(
            request,
            'Your account is pending admin approval. '
            'Please wait until an administrator verifies your account.'
        )
        return redirect('login')
    return None


@login_required
def dashboard(request):
    guard = _require_verified(request)
    if guard:
        return guard

    recent_articles = (
        NewsArticle.objects
        .filter(user=request.user)
        .select_related('result')[:5]
    )
    latest_metrics = ModelMetrics.objects.first()   # ordered by -trained_at
    model_ready = os.path.exists(
        os.path.join(settings.ML_MODEL_DIR, 'model.joblib')
    )
    return render(request, 'news/dashboard.html', {
        'recent_articles': recent_articles,
        'latest_metrics': latest_metrics,
        'model_ready': model_ready,
    })


@login_required
def analyze(request):
    guard = _require_verified(request)
    if guard:
        return guard

    result_data = None
    form = NewsSubmissionForm()

    if request.method == 'POST':
        form = NewsSubmissionForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            model_dir = str(settings.ML_MODEL_DIR)

            try:
                from ml.predictor import predict
                prediction = predict(text, model_dir)
            except FileNotFoundError:
                messages.error(
                    request,
                    'The AI model has not been trained yet. '
                    'Please ask the administrator to upload a dataset and train the model.'
                )
                return render(request, 'news/analyze.html', {'form': form})
            except Exception as e:
                messages.error(request, f'Analysis failed: {e}')
                return render(request, 'news/analyze.html', {'form': form})

            # Persist to DB
            article = NewsArticle.objects.create(user=request.user, text=text)
            AnalysisResult.objects.create(
                article=article,
                verdict=prediction['verdict'],
                confidence_score=prediction['confidence'],
            )
            result_data = prediction

    return render(request, 'news/analyze.html', {
        'form': form,
        'result': result_data,
    })


@login_required
def history(request):
    guard = _require_verified(request)
    if guard:
        return guard

    articles = (
        NewsArticle.objects
        .filter(user=request.user)
        .select_related('result')
    )
    return render(request, 'news/history.html', {'articles': articles})


@login_required
def export_csv(request):
    guard = _require_verified(request)
    if guard:
        return guard

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="analysis_history.csv"'

    writer = csv.writer(response)
    writer.writerow(['#', 'Submitted At', 'Text (first 100 chars)', 'Verdict', 'Confidence (%)', 'Analyzed At'])

    articles = (
        NewsArticle.objects
        .filter(user=request.user)
        .select_related('result')
    )
    for i, article in enumerate(articles, 1):
        res = getattr(article, 'result', None)
        writer.writerow([
            i,
            article.submitted_at.strftime('%Y-%m-%d %H:%M'),
            article.text[:100].replace('\n', ' '),
            res.verdict if res else 'N/A',
            res.confidence_score if res else 'N/A',
            res.analyzed_at.strftime('%Y-%m-%d %H:%M') if res else 'N/A',
        ])

    return response

'''
register(request)

  Two scenarios depending on request type:
  - GET (user just visits the page) → create empty form → show registration page
  - POST (user submitted the form) → validate data → if valid, save user to DB → redirect to login with success message   

  form.is_valid() checks:
  - No empty required fields
  - Email is valid format
  - Username not already taken
  - Password1 matches password2

  profile(request)

  Same pattern:
  - GET → load form pre-filled with current user's data
  - POST → validate → save changes → redirect back to profile

  instance=request.user is key — it tells the form "this is an existing user, update them" instead of creating a new one. 

  @login_required
  — if someone tries to visit /accounts/profile/ without being logged in, Django automatically redirects them to the login   page. Without this decorator anyone could access the profile page.

  messages.success()
  — stores a one-time flash message that gets displayed on the next page (like "Registration successful!").
'''