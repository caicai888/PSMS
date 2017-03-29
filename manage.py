from flask.ext.script import Manager, Server
# from flask_script import Manager, Server
from flask.ext.migrate import Migrate, MigrateCommand
# from flask_migrate import Migrate, MigrateCommand
import main
import PSMS

manager = Manager(PSMS.app)
migrate = Migrate(PSMS.app, main.db)
manager.add_command('db', MigrateCommand)

# manager.add_command("server", Server())
@manager.shell
def make_shell_context():
    """Create a python CLI.

    return: Default import object
    type: `Dict`
    """
    return dict(app=PSMS.app,
                db = main.db,
                Users=main.models.User)

if __name__ == '__main__':
    manager.run()