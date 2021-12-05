from flask import render_template, request, redirect, url_for
from flask_login import login_required
from app.main.func import education_specialty, education_plans, db_filter_req
from app.programs import bp
from app.programs.forms import WorkProgramDatesUpdate, FieldsForm, ChoosePlan
from app.programs.func import wp_update_list, wp_dates_update
from app.programs.models import WorkProgramBunchData


@bp.route("/choose_plan", methods=["GET", "POST"])
@login_required
def choose_plan():
    form = ChoosePlan()
    form.edu_spec.choices = list(education_specialty().items())
    if request.method == "POST":
        edu_spec = request.form.get("edu_spec")
        form.edu_plan.choices = list(education_plans(edu_spec).items())
        if request.form.get("edu_plan") and form.validate_on_submit():
            edu_plan = request.form.get("edu_plan")
            return redirect(url_for("programs.fields_data", plan_id=edu_plan))
        return render_template("programs/choose_plan.html", active="programs", form=form, edu_spec=edu_spec)
    return render_template("programs/choose_plan.html", active="programs", form=form)


@bp.route("/fields_data/<int:plan_id>", methods=["GET", "POST"])
@login_required
def fields_data(plan_id):
    form = FieldsForm()
    plan_name = db_filter_req('plan_education_plans', 'id', plan_id)[0]['name']
    if request.method == "POST":
        wp_field = request.form.get("wp_fields")
        wp_method = getattr(WorkProgramBunchData(plan_id), wp_field)
        wp_data = wp_method()
        return render_template("programs/fields_data.html", active="programs", form=form, plan_name=plan_name,
                               wp_fields=wp_field, wp_data=wp_data)
    return render_template("programs/fields_data.html", active="programs", form=form, plan_name=plan_name)


@bp.route("/dates_update", methods=["GET", "POST"])
@login_required
def dates_update():
    form = WorkProgramDatesUpdate()
    form.edu_spec.choices = list(education_specialty().items())
    if request.method == "POST":
        edu_spec = request.form.get("edu_spec")
        form.edu_plan.choices = list(education_plans(edu_spec).items())
        if request.form.get("wp_dates_update") and form.validate_on_submit():
            edu_plan = request.form.get("edu_plan")
            date_methodical = (
                request.form.get("date_methodical")
                if request.form.get("date_methodical")
                else ""
            )
            document_methodical = (
                request.form.get("document_methodical")
                if request.form.get("document_methodical")
                else ""
            )
            date_academic = (
                request.form.get("date_academic")
                if request.form.get("date_academic")
                else ""
            )
            document_academic = (
                request.form.get("document_academic")
                if request.form.get("document_academic")
                else ""
            )
            date_approval = (
                request.form.get("date_approval")
                if request.form.get("date_approval")
                else ""
            )
            disciplines, non_exist = wp_update_list(edu_plan)
            results = []
            for disc in disciplines:
                load_info = wp_dates_update(
                    disc,
                    date_methodical,
                    document_methodical,
                    date_academic,
                    document_academic,
                    date_approval,
                )
                if load_info == 1:
                    results.append(disciplines[disc])
            return render_template(
                "programs/dates_update.html",
                active="programs",
                form=form,
                edu_plan=edu_plan,
                edu_spec=edu_spec,
                results=results,
                non_exist=non_exist,
            )
        else:
            return render_template(
                "programs/dates_update.html",
                active="programs",
                form=form,
                edu_spec=edu_spec,
            )
    return render_template("programs/dates_update.html", active="programs", form=form)
