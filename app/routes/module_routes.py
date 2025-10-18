from flask import Blueprint, render_template
from ..models import Module
from flask_login import login_required
import markdown  # Add this import

module_bp = Blueprint('module', __name__, url_prefix='/modules')

@module_bp.route('/')
@login_required
def list_modules():
    modules = Module.query.all()
    return render_template('modules/list.html', modules=modules)

@module_bp.route('/view/<int:module_id>')
@login_required
def view_module(module_id):
    module = Module.query.get_or_404(module_id)
    html_content = markdown.markdown(module.content or "")  # Convert Markdown to HTML
    return render_template('modules/view.html', module=module, html_content=html_content)
