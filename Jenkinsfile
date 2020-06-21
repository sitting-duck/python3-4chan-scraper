
pipeline {
    agent any

    triggers {
        cron('H 0 * * *') // run every night at midnight
    }

    stages {
        stage('') {
            steps {
                script {
                    sh """
                    source ~/.venv/py3/bin/activate
                    python3 "~/projects/python3-4chan-scraper/my.py" board s
                    """
                }
            }
        }
    }
}
