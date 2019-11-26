import wtforms
from flask_wtf import FlaskForm


class TaskForm(FlaskForm):
    name = wtforms.StringField(  # label="任务名称",
        render_kw={
            "class": "form-control",
            "placeholder": "任务名称"
        }
    )
    description = wtforms.TextField(
        render_kw={
            "class": "form-control",
            "placeholder": "任务描述"
        }
    )
    time = wtforms.DateField(
        render_kw={
            "class": "form-control",
            "placeholder": "任务时间"
        }
    )
    public = wtforms.StringField(
        render_kw={
            "class": "form-control",
            "placeholder": "公布任务人"
        }
    )
