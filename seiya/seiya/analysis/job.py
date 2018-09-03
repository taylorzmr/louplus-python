from io import BytesIO

from sqlalchemy import func, Float, select, and_
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

from seiya.db import engine, Session, JobModel


def count_top10():
    session = Session()
    rows = session.query(
        JobModel.city,
        func.count(JobModel.city).label('count')
    ).group_by(JobModel.city).order_by('count desc').limit(10)
    return [row._asdict() for row in rows]


def salary_top10():
    session = Session()
    rows = session.query(
        JobModel.city,
        func.avg(
            (JobModel.salary_lower + JobModel.salary_upper) / 2
        ).cast(Float).label('salary')
    ).filter(
        and_(JobModel.salary_lower > 0, JobModel.salary_upper > 0)
    ).group_by(JobModel.city).order_by('salary desc').limit(10)
    return [row._asdict() for row in rows]


def _hot_tags():
    df = pd.read_sql(select([JobModel.tags]), engine)

    df = pd.concat([pd.Series(row['tags'].split(' '))
                    for _, row in df.iterrows()]).reset_index()
    del df['index']
    df.columns = ['tag']

    df = df[df['tag'] != '""']
    df = df[df['tag'] != '']

    return df.groupby(['tag']).size().sort_values(ascending=False)


def hot_tags():
    rows = []
    for item in _hot_tags().items():
        rows.append({'tag': item[0], 'count': item[1]})

    return rows


def hot_tags_plot(format='png'):
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    mpl.rcParams['axes.unicode_minus'] = False
    mpl.rcParams['figure.figsize'] = 10, 5

    s = _hot_tags()

    plt.bar(s.index[:10], s.values[:10])

    img = BytesIO()
    plt.savefig(img, format=format)

    return img.getvalue()


def experience_stat():
    session = Session()
    rows = session.query(
        func.concat(
            JobModel.experience_lower, '-', JobModel.experience_upper, '年'
        ).label('experience'),
        func.count('experience').label('count')
    ).group_by('experience').order_by('count desc')
    return [row._asdict() for row in rows]


def education_stat():
    session = Session()
    rows = session.query(
        JobModel.education,
        func.count(JobModel.education).label('count')
    ).group_by('education').order_by('count desc')
    return [row._asdict() for row in rows]


def salary_by_city_and_education():
    session = Session()
    rows = session.query(
        JobModel.city,
        JobModel.education,
        func.avg(
            (JobModel.salary_lower + JobModel.salary_upper) / 2
        ).cast(Float).label('salary')
    ).filter(
        and_(JobModel.salary_lower > 0, JobModel.salary_upper > 0)
    ).group_by(JobModel.city, JobModel.education).order_by(JobModel.city.desc())
    return [row._asdict() for row in rows]
