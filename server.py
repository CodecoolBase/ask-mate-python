from server_python import config
from server_python import sv_questions
from server_python import sv_general
from server_python import sv_answers
from server_python import sv_comments
from server_python import sv_tags
from server_python import sv_credentials
from server_python import sv_users



if __name__ == "__main__":
    config.app.run(
        debug=True,
        port=5004,
        host='0.0.0.0'
)