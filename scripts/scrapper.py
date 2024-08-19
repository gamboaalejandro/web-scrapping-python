from selenium.webdriver.common.by import By

from data.models.database import DatabaseConnection
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

    def process_data(self):
        pass


class UrlContentExtractionStrategy(ExtractStrategy):

    def extrac_content(self, data):
        a_labels = []
        #Could be any html element to explors Url (all page)
        container = driver.find_element(By.ID, 'list-tab-pane')
        #miclase = self.another_strategy.extrac_content(container)
        hrefs = [link.get_attribute('href') for link in container.find_elements(By.TAG_NAME, 'a')]
        # SE REQUIERE CREAR ALGUNA ESTRATEGIA O ABSTRACCION QUE MANEJE LOS DISTINTOS ELEMENTOS EN EL HTML
        url = self.extract_url_content(hrefs, 'detalle-area-conocimiento')
        print(url)

        pass


class ExtractContentFromALabelStrategy(ExtractStrategy):

    def extrac_content(self, data):
        driver.get(data)
        hrefs = [link.get_attribute('href') for link in driver.find_elements(By.TAG_NAME, 'a')]
        url = self.extract_url_content(hrefs, 'oferta-academica')
        return self.another_strategy.extrac_content(url)
        # links = driver.find_elements(By.TAG_NAME, 'a')
        # for link in links:
        #
        #     href = link.get_attribute('href')
        #     if 'oferta-academica' in (href):
        #         print("encontre oferta academica")
        #         self.another_strategy.extrac_content(content)
        #     text = link.text
        #     print(f"Texto: {text} - URL: {href}")
        #
        # print("Extract dIVC")//


class ExtractKnowledgeAreaStrategy(ExtractStrategy):

    def extrac_content(self, data):
        #DATA LLEGA COMO EL HTML
        """
        LOGICA PARA EXTRAER LA INFORMACION DEL AREA DE CONOCIMIENTO
        """
        name_area = driver.find_element(By.CSS_SELECTOR, 'p.text-primary.text-start.fw-light.fs-5').text

        settings.logger.info('Logging configured')
        p_label = driver.find_element(By.CSS_SELECTOR, 'p.text-normal.text-justify.fs-6.fw-light.lh-lg')
        all_text_split = p_label.text.split('\n')
        description_text = p_label.text.split('\n')[0]
        '''CASO BORDE DE INGENIERIA ARQUITECTURA Y TECNOLOGIA DONDE HAY UL'''
        from data.models.knowledge_area import KnowledgeAreas
        if session.query(KnowledgeAreas).filter(KnowledgeAreas.name == name_area).first():
            return
        knowledge_area = KnowledgeAreas(
            name=name_area,
            description=description_text
        )
        session.add(knowledge_area)
        for p in all_text_split:
            if '-' in p:
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
            self.another_strategy.extrac_content(data)


class ExtractAcademicOfferStrategy(ExtractStrategy):

    def extrac_content(self, data):

        """
        LOGICA PARA EXTRAER LA INFORMACION DE LA OFERTA ACADEMICA
        """
        area = False
        find_detail_knowledge_area_flag = False
        driver.get(data)
        container = driver.find_element(By.ID, 'list-tab-pane')
        links = container.find_elements(By.TAG_NAME, 'a')
        for links in links:
            href = links.get_attribute('href')
            if 'detalle_area_conocimiento' in href and not find_detail_knowledge_area_flag:
                find_detail_knowledge_area_flag = True
                text = links.text
                from data.models.knowledge_area import KnowledgeAreas
                area = session.query(KnowledgeAreas).filter(KnowledgeAreas.name == text).first
            if 'detalle-programa' in href:
                text = links.text.split(' - ')[1]
                from data.models.knowledge_area import AcademicPrograms
                academic_area_exist = session.query(AcademicPrograms).filter(AcademicPrograms.name == text).first
                if academic_area_exist:
                    continue
                program = AcademicPrograms(
                    name=text,
                    KnowledgeAreas_id=area.id,
                    knowledge_area=area
                )
                session.add(program)

                print(f"Texto: {text} - URL: {href}")
        """
        FIN LOGICA PARA EXTRAER LA INFORMACION DE LA OFERTA ACADEMICA
        """
        session.commit()
        if self.another_strategy:
            self.another_strategy.extrac_content(data)

        pass
