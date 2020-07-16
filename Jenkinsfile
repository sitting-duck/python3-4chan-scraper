
pipeline {
    agent any

    triggers {
        cron('H 0 * * *') // run every night at midnight
    }

    stages {
        stage('') {
            steps {
                script {
                    sh """#!/bin/bash
                    source /home/duck/.venv/py3/bin/activate # activates python venv. take this out if you dont' have one 
                    python3 "/home/duck/projects/python3-4chan-scraper/scraper.py" board s /home/duck/projects/datasets
                    """
                }
            }
        }
    }
}
