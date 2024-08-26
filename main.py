# This is a sample Python script.
from config import settings
from data.models.database import DatabaseConnection
from data.models.knowledge_area import KnowledgeAreas, SkillsForKnowledgeAreas, AcademicPrograms
from scripts.scrapper import ChromeScrapper, UrlContentExtractionStrategy, ExtractContentFromALabelStrategy, \
    ExtractKnowledgeAreaStrategy, ExtractAcademicOfferStrategy

# Press Ctrl+F5 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from data.models.university_institute import UniversityInstitute

db = DatabaseConnection()

session = db.get_session()


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press F9 to toggle the breakpoint.
    settings.logger.info('Logging configured')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    session.query(KnowledgeAreas).filter(KnowledgeAreas.name == 'name_area').first()
    scrapper = ChromeScrapper(UrlContentExtractionStrategy(
        ExtractContentFromALabelStrategy(
            ExtractKnowledgeAreaStrategy(
                ExtractAcademicOfferStrategy(False))
        )
    ))

    #record = session.query(UniversityInstitute).all()
    session.commit()
    data = scrapper.scraper(settings.WEB_BASE_URL_PUBLIC)

    print(data)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
