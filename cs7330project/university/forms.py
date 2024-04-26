from django import forms
from .models import Evaluation

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = [
            'method', 'levelA_stu_num', 'levelB_stu_num', 
            'levelC_stu_num', 'levelF_stu_num', 'improvement_suggestions'
        ]
        labels = {
            'method': 'Evaluation Method',
            'levelA_stu_num': 'Number of A level students',
            'levelB_stu_num': 'Number of B level students',
            'levelC_stu_num': 'Number of C level students',
            'levelF_stu_num': 'Number of F level students',
            'improvement_suggestions': 'Improvement Suggestions'
        }
