from faker import Faker
from random import randint
from jobplus.models import db, User, Personal, Company, Job, JobWanted

f = Faker(locale='zh_CN')

#生成随即汉字
def Unicode():
    val = randint(0x4e00, 0x9fbf)
    return chr(val)

#生成user
def iter_user():
    for i in range(20):
        yield User(
                name=str(f.random_int())+f.user_name(),
                email=f.ascii_email(),
                password='000000',
                role=f.random_element(elements=(10,20,30)),
                )



#生成公司和个人信息,文件路径暂时未生成，logo,简历
def iter_personal():
    for user in User.query:
        print('user.role',user.role)
        if user.role == 10:
            yield Personal(
                    user_id=user.id,
                    name=f.name(),
                    phone=f.phone_number(),
                    jobyear=f.random_int(0,100),
                    )
        elif user.role == 20:

            name = Unicode()+f.company()
            print(name)
            yield Company(
                    user_id=user.id,
                    name=name,
                    #name=Unicode()+f.company(),
                    address=f.address(),
                    url='https://www.baidu.com',
                    phone=f.phone_number(),
                    summary=f.sentence(),
                    field=f.random_element(elements=('医药', '互联网', '金融')),
                    financing=f.random_element(elements=('A轮','B轮','C轮','天使轮')),
                    )

#职位信息
def iter_job():
    for company in Company.query:
        for i in range(randint(0,10)):
            pay_int = f.random_int(0,100)*1000
            yield Job(
                    company_id=company.id,
                    name=f.job(),
                    min_pay= pay_int,
                    max_pay=f.random_int(0,100)*1000+pay_int,
                    address=f.address(),
                    label=f.random_element(elements=('互联网','销售','管理')),
                    jobyear=f.random_int(0,100),
                    education=f.random_element(elements=('无限制','专科','本科','博士'))
                    )

# 生成投递表
def iter_jobwanted():
    for personal in Personal.query:
        for job in Job.query:
            if randint(0,1) == 0:
                yield JobWanted(
                        job_id=job.id,
                        personal_id=personal.id,
                        company_id= job.company_id,
                        state=f.random_element(elements=(1,2,3))
                        )
def run():
    for user in iter_user():
        db.session.add(user)
    for company in iter_personal():
        db.session.add(company)
    for job in iter_job():
        db.session.add(job)
    for jobwanted in iter_jobwanted():
        db.session.add(jobwanted)
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()

