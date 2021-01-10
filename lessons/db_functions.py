from .models import Subject, SubjectClassLocal
from organisations.models import Organisation


def extendOrganisationSubject(org, sub_name):
  Subject.objects.create(name=sub_name, organisation=org)


def addSubjectToGroup(group, subName, subject):
  SubjectClassLocal.objects.create(name=subName, subject=subject, group=group)


def addClassToTeacher(classLocal, teacher):
  classLocal.teachers.add(teacher)


def removeTeacherFromClass(classLocal, teacher):
  classLocal.teachers.remove(teacher)

def addLessonToClass(classLocal):
  Lesson