from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange


class ChoosePlan(FlaskForm):
    edu_spec = SelectField("Специальность:", coerce=str, validators=[DataRequired()])
    edu_plan = SelectField(
        "План:", coerce=str, validators=[DataRequired()])


class FieldsForm(FlaskForm):
    wp_fields = SelectField("Выберите поле:", coerce=str, choices=[
            ('names', "Название программы"),
            ('reviewers_ext', 'Рецензенты'),
            ('purposes', "Цели"),
            ('tasks', "Задачи"),
            ('place_in_structure', "Место в структуре ООП"),
            ('no_next_disc', "Пояснение к таблице с последующими дисциплинами (информация об отсутствии)"),
            ('templan_info', "Примечание к тематическому плану"),
            ('self_provision', "Обеспечение самостоятельной работы"),
            ('test_criteria', "Критерии оценки для сдачи промежуточной аттестации в форме тестирования"),
            ('authorprint', "Автор(ы) рабочей программы (для печати)"),
            ('course_works', "Тематика курсовых работ"),
            ('practice', "Практикум"),
            ('control_works', "Тематика контрольных работ"),
            ('exam_form_desc', "Примерные оц. средства для пров. пром. атт. обучающихся по дисциплине"),
            ('task_works', "Задачи"),
            ('tests', "Тесты"),
            ('internet', "Ресурсы информационно-телекоммуникационной сети Интернет"),
            ('software', "Программное обеспечение"),
            ('ref_system', "Базы данных, информационно-справочные и поисковые системы"),
            ('materials_base', "Описание материально-технической базы"),
        ],
            validators=[DataRequired()])
    fields_data = SubmitField("Сформировать")


class WorkProgramDatesUpdate(ChoosePlan):  # добавить валидаторы для дат
    date_methodical = StringField(
        "Дата методического совета",
        validators=[Length(min=10, max=10, message="Формат даты - ГГГГ-ММ-ДД")],
    )
    document_methodical = IntegerField(
        "Номер документа методического совета",
        validators=[NumberRange(max=99, message="Номер протокола от 1 до 99")],
    )
    date_academic = StringField(
        "Дата Ученого совета",
        validators=[Length(min=10, max=10, message="Формат даты - ГГГГ-ММ-ДД")],
    )
    document_academic = IntegerField(
        "Номер документа Ученого совета",
        validators=[NumberRange(max=99, message="Номер протокола (от 1 до 99)")],
    )
    date_approval = StringField(
        "Дата утверждения",
        validators=[Length(min=10, max=10, message="Формат даты - ГГГГ-ММ-ДД")],
    )
    wp_dates_update = SubmitField("Обновить данные")
