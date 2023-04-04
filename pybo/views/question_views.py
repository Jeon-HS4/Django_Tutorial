from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone

from pybo.forms import QuestionForm
from pybo.models import Question


@login_required(login_url='common:login')
def question_create(request):
    if(request.method == 'POST'): # POST방식으로 전달
        form = QuestionForm(request.POST) # 유효하지 않은 데이터가 들어오면 오류 메세지가 저장됨
        if(form.is_valid()):    # 입력된 Form이 유효한 경우
            question = form.save(commit=False) #question 객체에 임시저장
            question.author = request.user  # author 속성에 로그인 계정 저장
            question.create_date = timezone.now() # 시간을 설정하고
            question.save() # 저장
            return redirect('pybo:index')
    else:   #GET방식으로 전달
        form = QuestionForm()
    context = {'form':form}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url="common:login")
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request,"수정 권한이 없습니다")
        return redirect('pybo:detail', question_id=question.id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form':form}
    return render(request, 'pybo/question-form.html', context)

@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')