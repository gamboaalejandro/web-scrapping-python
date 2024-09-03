# This is a sample Python script.
from config import settings
from data.models.database import DatabaseConnection
from scripts.scrapper import ChromeScrapper, UrlContentExtractionStrategy, \
    ExtractKnowledgeAreaStrategy, ExtractAcademicOfferStrategy, ExtractContentFromALabelStrategy

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
    scrapper = ChromeScrapper(UrlContentExtractionStrategy(
        ExtractContentFromALabelStrategy(
            ExtractKnowledgeAreaStrategy(
                ExtractAcademicOfferStrategy(False))
        )

    ))

    #record = session.query(UniversityInstitute).all()
    session.commit()
    # scrapper.scraper(settings.WEB_BASE_URL_PUBLIC)
    scrapper.scraper(settings.WEB_BASE_URL_PRIVATE)
    print(data)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
