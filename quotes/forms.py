from django import forms

from quotes.models import Quote


class QuoteForm(forms.ModelForm):
    # ModelForm 을 설정하는 내부 클래스. 폼이 다룰 모델과 필드를 지정할 수 있다.
    class Meta:
        # 이 폼이 Quote 모델에 해당한다고 지정. 이 폼을 통해 사용자가 입력한 데이터는 Quote 모델의 필드에 맞게 처리됨.
        model = Quote
        # 이 폼에 포함될 모델 필드를 지정한다.
        fields = ["text", "author", "category"]
