from flask import Blueprint, render_template

root_bp = Blueprint("rootPage", __name__)

@root_bp.route("/")
def root():
  return render_template("root.html")