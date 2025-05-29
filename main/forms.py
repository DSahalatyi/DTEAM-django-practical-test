from django import forms

SUPPORTED_LANGUAGES = [
    ("en", "English"),
    ("kw", "Cornish"),
    ("gv", "Manx"),
    ("br", "Breton"),
    ("iu", "Inuktitut"),
    ("kl", "Kalaallisut"),
    ("rom", "Romani"),
    ("oc", "Occitan"),
    ("lad", "Ladino"),
    ("se", "Northern Sami"),
    ("hsb", "Upper Sorbian"),
    ("csb", "Kashubian"),
    ("zza", "Zazaki"),
    ("cv", "Chuvash"),
    ("liv", "Livonian"),
    ("tsd", "Tsakonian"),
    ("srm", "Saramaccan"),
    ("bi", "Bislama"),
]


class EmailForm(forms.Form):
    email = forms.EmailField()


class TranslateCVForm(forms.Form):
    language = forms.ChoiceField(
        choices=SUPPORTED_LANGUAGES,
        label="Translate to",
        widget=forms.Select(attrs={"class": "form-control ml-2"}),
    )
