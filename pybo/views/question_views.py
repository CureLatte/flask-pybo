from flask import Blueprint, render_template, request, url_for, g, flash

from pybo.models import Question, Answer, User, question_voter

from ..forms import QuestionForm, AnswerForm

from datetime import datetime

from werkzeug.utils import redirect

from .. import db

from pybo.views.auth_views import login_required

from sqlalchemy import func

bp = Blueprint('question', __name__, url_prefix='/question')


@bp.route('/list/')
def _list():
    # 입력 파라미터
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    so = request.args.get('so', type=str, default='recent')

    # 정렬
    if so == 'recommend':
        sub_query = db.session.query(
            question_voter.c.question_id, func.count('*').label('num_voter')).group_by(question_voter.c.question_id).subquery()
        question_list = Question.query \
            .outerjoin(sub_query, Question.id == sub_query.c.question_id) \
            .order_by(sub_query.c.num_voter.desc(), Question.create_date.desc())
    elif so == 'popular':
        sub_query = db.session.query(
            Answer.question_id, func.count('*').label('num_answer')) \
            .group_by(Answer.question_id).subquery()
        question_list = Question.query \
            .outerjoin(sub_query, Question.id == sub_query.c.question_id) \
            .order_by(sub_query.c.num_answer.desc(), Question.create_date.desc())
    else:
        question_list = Question.query.order_by(Question.create_date.desc())


    # 조회
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(
            Answer.question_id, Answer.content, User.username).join(User, Answer.user_id == User.id).subquery()
        question_list = question_list \
            .join(User) \
            .outerjoin(sub_query, sub_query.c.question_id == Question.id) \
            .filter(Question.subject.ilike(search) |
                    Question.content.ilike(search) |
                    Question.content.ilike(search) |
                    sub_query.c.content.ilike(search) |
                    sub_query.c.username.ilike(search)
                    ) \
            .distinct()

    # 페이징
    question_list = question_list.paginate(page, per_page=10)
    return render_template('question/question_list.html', question_list=question_list, page=page, kw=kw, so=so)


@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get(question_id)
    return render_template('question/question_detail.html', question=question, form=form)


@bp.route('/create/', methods=('GET', 'POST'))
@login_required
def create():
    form = QuestionForm()
    if request.method == "POST" and form.validate_on_submit():
        question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now(),
                            user=g.user)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('question/question_form.html', form=form)


@bp.route('/modify/<int:question_id>', methods=('GET', 'POST'))
@login_required  # 로그인이 안되면 로그인 페이지로 이동하는 애너테이터
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:  # user가 질문의 유저가 아니면
        flash('수정 권한이 없습니다. ')  # flash error 발생
        return redirect(url_for('question.detail', question_id=question_id))  # question.detail로 재설정
    if request.method == 'POST':  # method가 POST이면 - 수정 후 Form
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)  # form 변수에 데이터( 화면에 입력되어 있는 데이터 )
            question.modify_date = datetime.now()  # 수정 일시 저장
            db.session.commit()
            return redirect(url_for('question.detail', question_id=question_id))
    else:
        form = QuestionForm(obj=question)
    return render_template('question/question_form.html', form=form)


@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash("삭제 권한이 없습니다.")
        return redirect(url_for('question.detail', question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question._list'))
