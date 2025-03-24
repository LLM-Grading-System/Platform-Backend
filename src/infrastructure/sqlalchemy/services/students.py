from sqlmodel import col, or_, select

from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlalchemy.models import Student
from src.services.exceptions import NotFoundError, AlreadyExistError
from src.services.stundents import StudentDTO, StudentService


class SqlAlchemyStudentService(StudentService):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(self, username: str = "") -> list[StudentDTO]:
        query = select(Student)
        if username:
            query = query.where(
                or_(
                    col(Student.gh_username).ilike(f"%{username}%"),
                    col(Student.tg_username).ilike(f"%{username}%"),
                )
            )
        result = await self.session.execute(query)
        students = result.scalars().all()
        return [self.from_model_to_dto(student) for student in students]

    async def create(self, telegram_user_id: int, telegram_username: str, github_username: str) -> None:
        existing_student = await self._get_student_by_telegram_user_id(telegram_user_id)
        if existing_student:
            raise AlreadyExistError("Студент с таким профилем в телеграмме уже зарегистрирован")
        student = Student(tg_user_id=telegram_user_id, tg_username=telegram_username, gh_username=github_username)
        self.session.add(student)
        await self.session.commit()

    async def get_by_github_username(self, github_username: str) -> StudentDTO:
        student = await self._get_student_by_github_username(github_username)
        if not student:
            raise NotFoundError(f"Студента с привязанным GitHub профилем {github_username} не существует")
        return self.from_model_to_dto(student)

    async def get_by_telegram_user_id(self, telegram_user_id: int) -> StudentDTO:
        student = await self._get_student_by_telegram_user_id(telegram_user_id)
        if not student:
            raise NotFoundError(f"Студента с привязанным Telegram профилем не существует")
        return self.from_model_to_dto(student)

    @staticmethod
    def from_model_to_dto(model: Student) -> StudentDTO:
        return StudentDTO(
            student_id=str(model.student_id),
            telegram_user_id=model.tg_user_id,
            telegram_username=model.tg_username,
            github_username=model.gh_username,
            registered_at=model.registered_at,
        )

    async def _get_student_by_telegram_user_id(self, telegram_user_id: int) -> Student | None:
        query = select(Student).where(Student.tg_user_id == telegram_user_id)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def _get_student_by_github_username(self, github_username: str) -> Student | None:
        query = select(Student).where(Student.gh_username == github_username)
        result = await self.session.execute(query)
        return result.scalars().first()
