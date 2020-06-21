
pipeline {
    agent any

    triggers {
        cron('H 0 * * *') // run every night at midnight
    }

    stages {
        stage('') {
            steps {
                script {
                    python3 "/home/duck/projects/python3-4chan-scraper/my.py" board s
                }
            }
        }
    }
}
