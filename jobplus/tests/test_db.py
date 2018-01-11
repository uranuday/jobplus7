from jobplus.models import User, Company, Job, Application



class TestUser:
    def test_user(self, db):
        assert User.query.count() == 0
        user = User(username='admin', password='123456',role=User.ROLE_ADMIN, email='admin@job.com')
        db.session.add(user)
        db.session.commit()

        assert User.query.count() == 1
        assert User.query.first() == user

        db.session.delete(user)
        db.session.commit()

        assert User.query.count() == 0


    def test_com(self, db):
        assert Company.query.count() == 0
        com = Company(company_name='测试公司', location='北京', description='hello')
        db.session.add(com)
        db.session.commit()

        assert Company.query.count() == 1

        db.session.delete(com)
        db.session.commit()

        assert Company.query.count() == 0

    def test_job(self, db, company):
        assert Job.query.count() == 1

        job = Job(job_title='software engineer', requirements='10 years', salary='50k')
        job.company = Company.query.first()

        db.session.add(job)
        db.session.commit()

        assert Job.query.count() == 2
