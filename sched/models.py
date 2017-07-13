import sys
sys.path.append('/Users/johntran/Documents/virtualenv/scheduler/lib/python2.7/site-packages')

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import synonym, relationship
from werkzeug import check_password_hash, generate_password_hash


Base = declarative_base()


class User(Base):
    '''A user login, with credentials and authentication'''
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    name = Column('name', String(200))
    email = Column(String(100), unique=True, nullable=False)
    active = Column(Boolean, default=True)

    _password = Column('password', String(100))

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        if password:
            password = password.strip()
        self._password = generate_password_hash(password)

    password_descriptor = property(_get_password, _set_password)
    password = synonym('_password', descriptor=password_descriptor)

    def check_password(self, password):
        if self.password == None:
            return False
        password = password.strip()
        if not password:
            return False
        return check_password_hash(self.password, password)

    @classmethod
    def authenticate(cls, query, email, password):
        email = email.strip().lower()
        user = query(cls).filter(cls.email==email).first()
        if user is None:
            return None, False
        if not user.active:
            return user, False
        return user, user.check_password(password)

    def get_id(self):
        return str(self.id)

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        True

class Appointment(Base):
    '''An appointment on the calendar'''
    __tablename__ = 'appointment'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    title = Column(String(25), nullable=False)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    allday = Column(Boolean, default=False)
    location = Column(String(25))
    description = Column(String(25))
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship(User, lazy='joined', join_depth=1)

    @property
    def duration(self):
        delta = self.end - self.start
        return delta.days * 24 * 60 * 60 + delta.seconds

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))


if __name__ == '__main__':
    from datetime import timedelta
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine('sqlite:///sched.db', echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    now = datetime.now()

    session.add(
        Appointment(
            title='Important Meeting',
            start=now+timedelta(days=3),
            end=now+timedelta(days=3, seconds=3600),
            allday=False,
            location='The Office',
            user_id=1
        )
    )
    session.commit()

    session.add(
        Appointment(
            title='Past Meeting',
            start=now-timedelta(days=3),
            end=now-timedelta(days=3, seconds=3600),
            allday=False,
            location='The Office',
            user_id=1
        )
    )
    session.commit()

    session.add(
        Appointment(
            title='Follow Up',
            start=now+timedelta(days=4),
            end=now+timedelta(days=4, seconds=3600),
            allday=False,
            location='The Office',
            user_id=1
        )
    )
    session.commit()

    session.add(
        Appointment(
            title='Day Off',
            start=now+timedelta(days=5),
            end=now+timedelta(days=5),
            allday=True,
            user_id=1
        )
    )
    session.commit()

    session.add(
        User(
            created=now,
            modified=now,
            name='John Tran',
            email='john.tran@mkacyber.com',
            active=True,
            password='ASDFasdf1234!'
        )
    )
    session.commit()

    # Create. Add a new model instance to the session
    appt = Appointment(
        title='My Appointment',
        start=now,
        end=now+timedelta(seconds=1800),
        allday=False,
        user_id=1
    )
    session.add(appt)
    session.commit()

    # Update. Update the object in place, then commit
    appt.title = 'Your Appointment'
    session.commit()

    # Delete. Tell the session to delete the object
    session.delete(appt)
    session.commit()

    # Get an appointment by ID
    appt = session.query(Appointment).get(1)

    # Get all appointments
    appts = session.query(Appointment).all()

    # Get all appointments before right now, after right now
    appts = session.query(Appointment).filter(
        Appointment.start < datetime.now()).all()
    appts = session.query(Appointment).filter(
        Appointment.start >= datetime.now()).all()

    # Get all appointments before a certain date
    appts = session.query(Appointment).filter(
        Appointment.start <= datetime(2020, 5, 1)).all()

    # Get the first appointments before a certain date
    appt = session.query(Appointment).filter(
        Appointment.start <= datetime(2020, 5, 1)).first()

    # Get the first user in the database
    users = session.query(User).all()
    user = users[0]
    