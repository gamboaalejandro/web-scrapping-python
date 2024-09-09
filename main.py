# This is a sample Python script.
from config import settings
from data.models.database import DatabaseConnection
from scripts.scrapper import ChromeScrapper, UrlDetailAreaExtractionStrategy, \
    ExtractKnowledgeAreaStrategy, ExtractAcademicOfferStrategy, ExtractContentFromALabelStrategy, \
    ExtractURLAcademicProgramsStrategy, ExtractAcademicProgramDescriptionStrategy

# Press Ctrl+F5 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from data.models.university_institute import UniversityInstitute

db = DatabaseConnection()

session = db.get_session()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    scrapper = ChromeScrapper(UrlDetailAreaExtractionStrategy(
            ExtractKnowledgeAreaStrategy(ExtractAcademicOfferStrategy(False))
    ))

    scrapping_academic_program = ChromeScrapper(
        ExtractURLAcademicProgramsStrategy(
            ExtractAcademicProgramDescriptionStrategy(False)
        ))
    #scrapper.scraper(settings.WEB_BASE_URL_PRIVATE)
    #scrapper.scraper(settings.WEB_BASE_URL_PUBLIC)
    scrapping_academic_program.scraper(settings.WEB_BASE_URL_PUBLIC)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
