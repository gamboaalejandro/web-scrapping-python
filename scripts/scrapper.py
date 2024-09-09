import re
from selenium.webdriver.common.by import By

from data.models.database import DatabaseConnection
from data.models.knowledge_area import AcademicPrograms
from data.models.university_institute import university_knowledge_association, UniversityInstitute
from scripts.base.StrategyInterface import ExtractStrategy
from scripts.base.WebDriverSingleton import WebDriverSingleton
from scripts.base.asbtract_scrapper import ScrapperUrlInterface
from config import settings

driver = WebDriverSingleton.get_instance()
db = DatabaseConnection()
session = db.get_session()


class ChromeScrapper(ScrapperUrlInterface):
    html_to_scrap = ''

    def __init__(self, extraction_strategy: ExtractStrategy):
        super().__init__(extraction_strategy)

    def scraper(self, url):
        super().scraper(url)

    def fetch_page(self, url):
        # Navegar a la URL deseada
        # url = config.settings.WEB_BASE_URL_PUBLIC
        WebDriverSingleton.get_instance().get(url)
        # Obtener el contenido de la página
        page_content = WebDriverSingleton.get_instance().page_source
        self.html_to_scrap = page_content
        return page_content

    def extract_data(self):
        return self.extraction_strategy.extrac_content(self.html_to_scrap)


class UrlDetailAreaExtractionStrategy(ExtractStrategy):

    def extrac_content(self, data):
        a_labels = []
        # Could be any html element to explors Url (all page)
        container = driver.find_element(By.ID, 'list-tab-pane')
        # miclase = self.another_strategy.extrac_content(container)
        hrefs = list(set([link.get_attribute('href') for link in
                          container.find_elements(By.XPATH, "//a[contains(@href, 'detalle-area-conocimiento')]")]))
        # SE REQUIERE CREAR ALGUNA ESTRATEGIA O ABSTRACCION QUE MANEJE LOS DISTINTOS ELEMENTOS EN EL HTML
        url = self.extract_url_content(hrefs, 'detalle-area-conocimiento')
        print(url)

        pass


class ExtractContentFromALabelStrategy(ExtractStrategy):

    def extrac_content(self, data):
        hrefs = [link.get_attribute('href') for link in driver.find_elements(By.TAG_NAME, 'a')]
        url = self.extract_url_content(hrefs, 'oferta-academica')
        return url


class ExtractKnowledgeAreaStrategy(ExtractStrategy):

    def extrac_content(self, data):
        # DATA LLEGA COMO EL HTML
        """
        LOGICA PARA EXTRAER LA INFORMACION DEL AREA DE CONOCIMIENTO
        """
        driver.get(data)
        name_area = (driver.find_element(By.CSS_SELECTOR, 'p.text-primary.text-start.fw-light.fs-5')
                     .text.replace('(ver oferta)', '').strip())
        academic_offer = driver.find_element(By.XPATH, "//a[contains(@href, 'oferta-academica')]")
        href_value = academic_offer.get_attribute('href')
        p_label = driver.find_element(By.CSS_SELECTOR, 'p.text-normal.text-justify.fs-6.fw-light.lh-lg')
        all_text_split = self.extract_ul_content() if self.extract_ul_content() else [item.replace('-', '') for item in
                                                                                      p_label.text.split('\n') if
                                                                                      '-' in item]

        description_text = p_label.text.split('\n')[0]
        from data.models.knowledge_area import KnowledgeAreas
        if not session.query(KnowledgeAreas).filter(KnowledgeAreas.name == name_area).first():

            knowledge_area = KnowledgeAreas(
                name=name_area,
                description=description_text
            )
            session.add(knowledge_area)
            for p in all_text_split:
                from data.models.knowledge_area import SkillsForKnowledgeAreas
                skill = SkillsForKnowledgeAreas(
                    name=p,
                    knowledge_area_id=knowledge_area.id,
                    knowledge_area=knowledge_area
                )
                session.add(skill)

            session.commit()
        """
        FIN LOGICA PARA EXTRAER LA INFORMACION DEL AREA DE CONOCIMIENTO
        """
        if self.another_strategy:
            self.another_strategy.extrac_content(href_value)
        """
        NOTA; este conjunto de clases se encuentran acopladas unas a otras ya que es necesario detallar la estrategia de scrapping para 
        extrar informacion especifica del URL brindado, si se requiere hacer scrapping de otra pagina estas estrategias podrian no funcionar 
        """

    def extract_ul_content(self):
        li_text = []
        ul_tags = driver.find_element(By.CSS_SELECTOR, 'div.col-10.p-6').find_elements(By.TAG_NAME, 'li')
        for ul in ul_tags:
            li_text.append(ul.text)
            print(ul.text)
        if li_text:
            return li_text
        return []


class ExtractAcademicOfferStrategy(ExtractStrategy):

    def extrac_content(self, link):

        """
        LOGICA PARA EXTRAER LA INFORMACION DE LA OFERTA ACADEMICA
        """
        area = False
        university = False
        university_exists = False
        find_detail_knowledge_area_flag = False
        driver.get(link)
        container = driver.find_element(By.ID, 'list-tab-pane')
        links = container.find_elements(By.TAG_NAME, 'a')
        for links in links:
            href = links.get_attribute('href')

            if 'detalle-ieu' in href:
                university_exists = session.query(UniversityInstitute).filter(
                    UniversityInstitute.university_name == links.text.replace('(GESTIÓN PÚBLICA)', '').strip()).first()
                if not university_exists:
                    university = UniversityInstitute(
                        university_name=re.sub(r'\(GESTIÓN PÚBLICA\)|\(GESTIÓN PRIVADA\)', '', links.text).strip()
                    )
                    session.add(university)
                    session.commit()

            if 'detalle-area-conocimiento' in href:
                find_detail_knowledge_area_flag = True
                text = links.text
                from data.models.knowledge_area import KnowledgeAreas
                area = session.query(KnowledgeAreas).filter(KnowledgeAreas.name == text).first()

                if area and university:
                    # Crear la relación muchos a muchos si el área de conocimiento y la universidad existen
                    if university not in area.universities:
                        area.universities.append(university)
                        session.commit()
                if university_exists:

                    if university_exists not in area.universities:
                        area.universities.append(university_exists)
                        session.commit()

            if 'detalle-programa' in href and find_detail_knowledge_area_flag:
                text = links.text.split(' - ')[1]
                academic_area_exist = session.query(AcademicPrograms).filter(AcademicPrograms.name == text).first()
                if not academic_area_exist:

                    program = AcademicPrograms(
                        name=text,
                        KnowledgeAreas_id=area.id,
                        knowledge_area=area
                    )
                    if university and not university_exists:
                        session.add(program)
                        session.commit()
                    if university_exists:
                        session.add(program)
                        session.commit()
                    session.commit()
                else:

                    if university and not university_exists:
                        session.add(academic_area_exist)
                        session.commit()
                    if university_exists:
                        session.add(academic_area_exist)
                        session.commit()

                print(f"Texto: {text} - URL: {href}")
        """
        FIN LOGICA PARA EXTRAER LA INFORMACION DE LA OFERTA ACADEMICA
        """
        if self.another_strategy:
            self.another_strategy.extrac_content(link)

        pass


class ExtractURLAcademicProgramsStrategy(ExtractStrategy):
    def extrac_content(self, data):
        hrefs = list(set([link.get_attribute('href') for link in
                          driver.find_elements(By.XPATH, "//a[contains(@href, 'detalle-programa')]")]))
        self.extract_url_content(hrefs, 'detalle-programa')

        pass


class ExtractAcademicProgramDescriptionStrategy(ExtractStrategy):
    def extrac_content(self, data):
        driver.get(data)
        description_element = \
            driver.find_element(By.XPATH, "//dl[@class='row']").text.split("DESCRIPCIÓN:")[1].split("PERIODICIDAD")[
                0].replace("\n", "")
        academic_program = \
            driver.find_element(By.XPATH, "//dl[@class='row']").text.split("PROGRAMA ACADÉMICO:")[1].split("CÓDIGO:")[
                0].replace("\n", "")

        """
        LOGICA SCRAPPER PARA EXTRAER EL DESCRIPTION DE LAS OFERTAS ACADEMICAS
        """
        academic_program_bd = session.query(AcademicPrograms).filter(AcademicPrograms.name == academic_program).first()
        if academic_program_bd:
            academic_program_bd.description = description_element
            session.commit()
        else:
            settings.logger.error("NO SE ENCONTRO EL PROGRAMA ACADEMICO")
        pass
