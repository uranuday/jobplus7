import os
import json
from random import randint
from faker import Faker
from jobplus.models import db, User, Company, Job


fake = Faker()


def iter_companies():
    with open(os.path.join(os.path.dirname(__file__), '..', 'datas', 'company.json')) as f:
        companies = json.load(f)
    for company in companies:
        yield Company(
                company_name = company['name'],
                logo_url = company['logo_url'],
                description = company['description'],
                slogan = company['slogan'],
                website = "http://www.kernel.org"
                )


def iter_jobs():
    with open(os.path.join(os.path.dirname(__file__), '..', 'datas', 'job.json')) as f:
        jobs = json.load(f)
    for job in jobs:
        for i in range(1,6):
            company = Company.query.get(i)
            description = ''
            for sentence in fake.sentences(6):
                description += sentence + '\r'
            requirements = ''
            for sentence in fake.sentences(6):
                requirements += sentence + '\r'
            yield Job(
                    job_title = job['job_title'],
                    location = job['location'],
                    description = description,
                    salary = job['salary'],
                    exp_requirement = job['exp_requirement'],
                    edu_requirement = job['edu_requirement'],
                    company = company,
                    requirements = requirements
                    )


def iter_users():
    company = Company.query.get(1)
    yield User(
            username = "admin",
            name = "萧峰",
            email = "admin@jobplus.com",
            password = "123456",
            role = 30
            )

    yield User(
            username = "puser",
            name = "段誉",
            email = "puser@p.com",
            password = "123456",
            role = 10
            )

    yield User(
            username = "cuser",
            name = "虚竹",
            email = "cuser@c.com",
            password = "123456",
            role = 20,
            company = company
            )



def create_db():
    db.drop_all()
    db.create_all()

    for company in iter_companies():
        db.session.add(company)

    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()


    for job in iter_jobs():
        db.session.add(job)

    for user in iter_users():
        db.session.add(user)

    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()







