# DevOps Assignment Portal

## Project Overview
This project is a Flask-based assignment submission portal developed for the DevOps Mid Exam.

Students can submit:
- Student Name
- Registration Number
- Assignment Title
- Submission URL

The application validates the submitted information and displays valid submissions.

## Technologies Used
- Python
- Flask
- Pytest
- Git and GitHub
- GitHub Actions
- Ngrok

## Project Structure
```text
DevOps_Mid_Exam/
├── .github/
│   └── workflows/
│       └── tests.yml
├── app.py
├── test_app.py
├── receiver.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Run the Application Locally

1. Clone the repository:

```bash
git clone https://github.com/mh5791738-tech/DevOps_Mid_Exam.git
cd DevOps_Mid_Exam
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the Flask application:

```bash
python app.py
```

4. Open your browser:

```text
http://127.0.0.1:5000
```

## Automated Testing

Run the tests using:

```bash
python -m pytest -v
```

The project includes three automated tests:

1. Valid assignment submission.
2. Missing registration number rejection.
3. Invalid URL rejection.

## Continuous Integration (CI)

GitHub Actions automatically runs the tests when code is pushed to the main branch or a pull request targets main.

The workflow:
1. Checks out the repository.
2. Sets up Python.
3. Installs dependencies.
4. Runs automated tests.
5. Generates a JSON test report.
6. Sends the report to the local computer.
7. Uploads test reports as GitHub Actions artifacts.

## Test Report Receiver

The local Flask receiver runs on port `5001`.

Configure the receiver token in PowerShell:

```powershell
$env:REPORT_RECEIVER_TOKEN = "YOUR_SECRET_TOKEN"
```

Start the receiver:

```powershell
python receiver.py
```

Expose the receiver using Ngrok:

```bash
ngrok http 5001
```

Configure these GitHub repository secrets:

- `REPORT_RECEIVER_URL`
- `REPORT_RECEIVER_TOKEN`

The receiver saves the latest report as `test-report.json` in the project directory.

The report contains repository details, branch, commit SHA, workflow run ID, timestamp, individual test results, and overall test statistics.

Reports are generated and sent for both successful and failed test runs.

## Demonstration

The project was demonstrated through three stages:

1. Successful pipeline execution with all three tests passing.
2. Intentional code defect causing one test to fail.
3. Fixing the defect and restoring a successful pipeline with all three tests passing.

## GitHub Repository

https://github.com/mh5791738-tech/DevOps_Mid_Exam