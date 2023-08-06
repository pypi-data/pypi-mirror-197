# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['elb_log_analyzer']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.26.84,<2.0.0',
 'pandas>=1.5.3,<2.0.0',
 'requests>=2.28.2,<3.0.0',
 'streamlit>=1.17.0,<2.0.0']

setup_kwargs = {
    'name': 'elb-log-analyzer',
    'version': '0.5.0',
    'description': 'AWB ELB log analyzer',
    'long_description': '# ELB Log Analyzer\n\nTool for analyzing ELB logs for automating steps to retreive details of ip\'s user agent, total request count, to which urls requests were made along with their total count, and http methods in json format.\n\n## S3 Bucket Log Downloader\n\nDownloads S3 bucket objects that we created in specified time window.\n\n## Installation\n\n- Using Pip\n\n    ```bash\n    python3 -m pip install elb-log-analyzer\n    ```\n\n### AWS configuration\n\n- Create IAM policy with below configuration\n\n    ```json\n    {\n    "Version": "2012-10-17",\n    "Statement": [\n        {\n            "Sid": "S3ListSpecificDirectory",\n            "Effect": "Allow",\n            "Action": "s3:ListBucket",\n            "Resource": "arn:aws:s3:::alb-log-bucket-name"\n        },\n        {\n            "Sid": "S3GetSpecificDirectory",\n            "Effect": "Allow",\n            "Action": "s3:GetObject",\n            "Resource": "arn:aws:s3:::alb-log-bucket-name/AWSLogs/XXXXXXXXXXXX/elasticloadbalancing/aws-region/*"\n        }\n    ]\n    }\n    ```\n\n    > **Note**: above policy will allow user to list all contents in the bucket but download objects only from `s3://alb-log-bucket-name/AWSLogs/XXXXXXXXXXXX/elasticloadbalancing/aws-region/*`\n\n- Create AWS access keys\n\n- Use aws cli to configure access key for boto3\n\n    ```bash\n    aws configure\n    ```\n\n### S3 Bucket Log Downloader Usage\n\n- Print Help Menu.\n\n    ```bash\n    python3 -m elb_log_analyzer.s3_log -h\n    ```\n\n- Download all log files generated in 10 hours from now.\n\n    ```bash\n    python3 -m elb_log_analyzer.s3_log -b elb-log-bucket -p \'alb-log-bucket-name/AWSLogs/XXXXXXXXXXXX/elasticloadbalancing/aws-region/\' -H 10\n    ```\n\n- Download all log files generated in 40 mins from now.\n\n    ```bash\n    python3 -m elb_log_analyzer.s3_log -b elb-log-bucket -p \'alb-log-bucket-name/AWSLogs/XXXXXXXXXXXX/elasticloadbalancing/aws-region/\' -m 40\n    ```\n\n- Download all log files generated in 20 secs from now.\n\n    ```bash\n    python3 -m elb_log_analyzer.s3_log -b elb-log-bucket -p \'alb-log-bucket-name/AWSLogs/XXXXXXXXXXXX/elasticloadbalancing/aws-region/\' -s 20\n    ```\n\n- Download all log files generated in 10 hours, 40 mins and 20 secs from now and store in a directory.\n\n    ```bash\n    python3 -m elb_log_analyzer.s3_log -b elb-log-bucket -p \'alb-log-bucket-name/AWSLogs/XXXXXXXXXXXX/elasticloadbalancing/aws-region/\' --hours 10 --minutes 40 --seconds 20 -o \'./logs/downloads\'\n    ```\n\n## Analyzer\n\nAnalyzes downloaded log files.\n\n### Analyzer Usage\n\n- Print Help Menu\n\n    ```bash\n    python3 -m elb_log_analyzer -h\n    ```\n\n- Print json data on console\n\n    ```bash\n    python3 -m elb_log_analyzer -i [INPUT_LOG_FILE_PATH]\n    ```\n\n- Store json data in a file\n\n    ```bash\n    python3 -m elb_log_analyzer -i [INPUT_LOG_FILE_PATH] -o [OUTPUT_FILE_PATH]\n    ```\n\n    > **Note**: **INPUT_LOG_FILE_PATH** can be log file or a directory containing all log files ending with `.log` extension\n\n- Get IP details from IPAbuseDB\n\n    ```bash\n    python3 -m elb_log_analyzer -i [LOG_FILE_PATH] -t [REQUESTS_THRESHOLD_VALUE] -k [IP_ABUSE_DB_API_KEY] -o [OUTPUT_FILE_PATH]\n    ```\n\n## Alerts\n\nSend alert to slack channel with abusive ip details.\n\n### Usage\n\n- Send alert from analyzed file\n\n    ```bash\n    python elb_log_analyzer.alerts -w [SLACK_WEBHOOK] -f [ANALYZED_LOG_FILE_LOCATION]\n    ```\n\n## Dashboard\n\nDashboard to visualize data.\n\n### Dashboard Installation\n\n- Install requirements\n\n    ```bash\n    python3 -m pip install dashboard/requirements.txt\n    ```\n\n### Usage\n\n- Start App\n\n    ```bash\n    streamlit run dashboard/app.py\n    ```\n\n- Enter Log File/Directory Path\n\n## Publish package to pypi\n\n- Using poetry\n\n    ```bash\n    python3 -m poetry publish --build --username [PYPI_USERNAME] --password [PYPI_PASSWORD]\n    ```\n\n## Usage Summary\n\n- Download log files\n\n    ```bash\n    python3 -m elb_log_analyzer.s3_log -b elb-log-bucket -p \'alb-log-bucket-name/AWSLogs/XXXXXXXXXXXX/elasticloadbalancing/aws-region/\' -H [HOURS] -o logs\n    ```\n\n- Analyze Log Files\n\n    ```bash\n    python3 -m elb_log_analyzer -i logs -o log.json -t [REQUEST_THRESHOLD] -k [IP_ABUSE_API_KEY] \n    ```\n\n- Send Alert to slack with client ips having total number of requests greater than threshold requests\n\n    ```bash\n    python -m elb_log_analyzer.alerts -w [SLACK_WEBHOOK] -f [ANALYZED_LOG_FILE_LOCATION]\n    ```\n\n- Visualize Analyzed Logs using Dashboard\n\n    ```bash\n    streamlit run dashboard/app.py\n    ```\n\n## Docker\n\n- Pull image\n\n    ```bash\n    docker pull dmdhrumilmistry/elb-log-analyzer\n    ```\n\n- Start Container\n\n    ```bash\n    docker run -it --rm dmdhrumilmistry/elb-log-analyzer "elb_log_analyzer -h"\n    ```\n',
    'author': 'Dhrumil Mistry',
    'author_email': '56185972+dmdhrumilmistry@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8, !=2.7.*, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*, !=3.7.*',
}


setup(**setup_kwargs)
