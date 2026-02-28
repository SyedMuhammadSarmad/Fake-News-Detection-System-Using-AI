from django import forms


class NewsSubmissionForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 8, 'placeholder': 'Paste a news article or headline here…'}),
        min_length=20,
        max_length=10_000,
        label='News Text / Headline',
        help_text='Minimum 20 characters. Paste the full article for best accuracy.'
    )


class DatasetUploadForm(forms.Form):
    csv_file = forms.FileField(
        label='CSV File',
        help_text='Upload True.csv or Fake.csv (CSV format only).'
    )

    def clean_csv_file(self):
        f = self.cleaned_data['csv_file']
        if not f.name.lower().endswith('.csv'):
            raise forms.ValidationError('Only CSV files are accepted. Please upload a .csv file.')
        if f.size > 200 * 1024 * 1024:   # 200 MB limit
            raise forms.ValidationError('File too large. Maximum size is 200 MB.')
        return f
