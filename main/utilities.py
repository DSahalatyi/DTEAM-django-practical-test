import io
from openai import OpenAI
from xhtml2pdf import pisa
from django.conf import settings

from main.forms import SUPPORTED_LANGUAGES

client = OpenAI(
    api_key=settings.OPENAI_API_KEY,
)


def html_to_pdf(html: str) -> bytes | None:
    output = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("utf-8")), output)
    if not pdf.err:
        return output.getvalue()
    return None


def translate_text(text, target_language_code):
    if not text:
        return ""

    code_to_language = dict(SUPPORTED_LANGUAGES)
    target_language = code_to_language.get(target_language_code, "English")

    prompt = (
        f"Translate the following text to {target_language}."
        " Only provide the translated text, no extra words, no explanations.\n\n"
        f"{text}"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that translates text accurately.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
        )
        print(response)
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Translation error: {e}")
        return text
