import markdown
import markdown.extensions.fenced_code
from app import app
from app import model


@app.route('/')
def index():
    readme_file = open("README.md", 'r', encoding='utf-8')
    md_template_string = markdown.markdown(
        readme_file.read(), extensions=["fenced_code"]
    )
    return md_template_string


@app.route('/get/')
@app.route('/get/<user_id>/')
@app.route('/get/<user_id>/<best_k>/')
def get_recommendation(user_id=None, best_k=1):
    if best_k is not None:
        best_k = int(best_k)
    return app.response_class(
        response = model.predict(user_id, best_k),
        status = 200,
        mimetype = 'application/json'
    )