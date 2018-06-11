import pytest

from jobplus.app import create_app
from jobplus.models import db as database
from jobplus.models import User, Job, Application, Company



@pytest.fixture
def app():
    return create_app('testing')


@pytest.fixture
def db(app):
    with app.app_context():
        database.drop_all()
        database.create_all()
        return database


@pytest.fixture
def company(db):
    company = Company(company_name='jobplus', location='beijing', description='this is jobplus')
    job = Job(job_title='software_engineer', requirements='python', salary='100k')
    job.company = company
    db.session.add(company)
    db.session.commit()
    return company, job


@pytest.yield_fixture
def client(app):
    with app.test_client() as client:
        yield client
