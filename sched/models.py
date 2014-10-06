from datetime import datetime
from sqlalchemy import Boolean, Column
from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Appointment(Base):

    """An appointment on the calendar."""
    __tablename__ = 'appointment'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    title = Column(String(255))
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    allday = Column(Boolean, default=False)
    location = Column(String(255))
    description = Column(Text)

    @property
    def duration(self):
        delta = self.end - self.start
        return delta.days * 24 * 60 * 60 + delta.seconds

    def __repr__(self):
        return ('<{self.__class__.__name__}: {self.id}>'.format(self=self))


if __name__ == '__main__':  # pragma: no cover
    from datetime import timedelta
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine('sqlite:///sched.db', echo=True)

    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    now = datetime.now()

    session.add(Appointment(
        title='Important Meeting',
        start=now + timedelta(days=3),
        end=now + timedelta(days=3, seconds=3600),
        allday=False,
        location='The Office'))
    session.commit()

    session.add(Appointment(
        title='Past Meeting',
        start=now - timedelta(days=3),
        end=now - timedelta(days=3, seconds=3600),
        allday=False,
        location='The Office'))
    session.commit()

    session.add(Appointment(
        title='Follow Up',
        start=now + timedelta(days=4),
        end=now + timedelta(days=4, seconds=3600),
        allday=False,
        location='The Office'))
    session.commit()

    session.add(Appointment(
        title='Day Off',
        start=now + timedelta(days=5),
        end=now + timedelta(days=5),
        allday=True))
    session.commit()

    # Create. Add a new model instance to the session.
    appt = Appointment(
        title='My Appointment',
        start=now,
        end=now + timedelta(seconds=1800),
        allday=False)

    session.add(appt)
    session.commit()

    # Update. Update the object in place, then commit.
    appt.title = 'Your Appointment'
    session.commit()

    # Delete. Tell the session to delete the object.
    session.delete(appt)
    session.commit()

    # Get an appointment by ID.
    appt = session.query(Appointment).get(1)

    # Get all appointments.
    appts = session.query(Appointment).all()

    # Get all appointments before right now, after right now.
    appts = session.query(Appointment).filter(
        Appointment.start < datetime.now()).all()
    appts = session.query(Appointment).filter(
        Appointment.start >= datetime.now()).all()

    # Get all appointments before a certain date.
    appts = session.query(Appointment).filter(
        Appointment.start <= datetime(2013, 5, 1)).all()

    # Get the first appointment matching the filter query.
    appt = session.query(Appointment).filter(
        Appointment.start <= datetime(2013, 5, 1)).first()
