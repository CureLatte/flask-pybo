from flask_wtf import FlaskForm  # flask_wtf
from wtforms import StringField, TextAreaField, PasswordField, \
    EmailField  # StringField : 문자열(한줄) form, TextAreaField : 텍스트열 form
# from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, \
    Email  # DataRequired : 데이터가 입력되어있는지 확인하는 함수 cf) Email(이메일 점검), Length(길이점검)


class QuestionForm(FlaskForm):  # 질문 폼 정의
    subject = StringField('제목', validators=[DataRequired("제목은 필수 입려 항목입니다. ")])
    content = TextAreaField('내용', validators=[DataRequired("내용은 필수 입력 항목입니다. ")])


class AnswerForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다. ')])


class UserCreateForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password1 = PasswordField('비밀번호', validators=[DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다.')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])
    email = EmailField('이메일', [DataRequired(), Email()])


class UserLoginForm(FlaskForm):  # 입력을 받을 때는 항상 form을 사용하자
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('비밀번호', validators=[DataRequired()])


class CommentForm(FlaskForm):
    content=TextAreaField('내용', validators=[DataRequired()])