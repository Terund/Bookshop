from shop import db, create_app
from flask_script import Manager, Server
from flask_migrate import MigrateCommand, Migrate

app = create_app("develop")

manage = Manager(app)
manage.add_command("runserver", Server(use_debugger=True, host="0.0.0.0", port=5000))

manage.add_command("db", MigrateCommand)

Migrate(app, db)  # 数据库迁移


if __name__ == '__main__':
    manage.run()
