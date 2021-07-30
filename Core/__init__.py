from flask import Flask, redirect
from flask import Blueprint, jsonify, request, render_template, flash, url_for


def register_blueprints(app):
    from paragraph import bp as paragraph_bp
    app.register_blueprint(paragraph_bp)


# def register_plugin(app):
#     db.init_app(app)


def create_app():
    app = Flask(__name__)
   #  app.config.from_object('config')
    register_blueprints(app)
   #  register_plugin(app)
   #  with app.app_context():
   #      db.create_all()
   #      # init_data()
    return app

app = create_app()

@app.route("/", methods=("GET", "POST"))
def base():
    return render_template("base.html")

if __name__ == '__main__':
   app.run(host='0.0.0.0', debug=False)