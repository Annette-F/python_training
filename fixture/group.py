from selenium.webdriver.common.by import By
from model.group import Group


class GroupHelper:
    def __init__(self, app):
        self.app = app

    def open_groups_page(self):
        wd = self.app.wd
        if not (wd.current_url.endswith('/group.php') and len(wd.find_elements(By.NAME, 'new')) > 0):
            wd.find_element(By.LINK_TEXT, 'groups').click()

    def change_field_value(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element(By.NAME, field_name).click()
            wd.find_element(By.NAME, field_name).clear()
            wd.find_element(By.NAME, field_name).send_keys(text)

    def fill_group_form(self, group):
        wd = self.app.wd
        self.change_field_value('group_name', group.name)
        self.change_field_value('group_header', group.header)
        self.change_field_value('group_footer', group.footer)

    def create(self, group):
        wd = self.app.wd
        self.open_groups_page()
        # init group creation
        wd.find_element(By.NAME, 'new').click()
        self.fill_group_form(group)
        # submit group creation
        wd.find_element(By.NAME, 'submit').click()
        self.return_to_groups_page()
        self.group_cashe = None

    def select_first_group(self):
        wd = self.app.wd
        wd.find_element(By.NAME, 'selected[]').click()

    def select_group_by_index(self, index):
        wd = self.app.wd
        wd.find_elements(By.NAME, 'selected[]')[index].click()

    def delete_first_group(self):
        self.delete_group_by_index(0)
        self.group_cashe = None

    def delete_group_by_index(self, index):
        wd = self.app.wd
        self.open_groups_page()
        self.select_group_by_index(index)
        # submit deletion
        wd.find_element(By.NAME, 'delete').click()
        self.return_to_groups_page()
        self.group_cashe = None

    def modify_first_group(self):
        self.modify_group_by_index(0)
        self.group_cashe = None

    def modify_group_by_index(self, index, new_group_data):
        wd = self.app.wd
        self.open_groups_page()
        self.select_group_by_index(index)
        # open modification form
        wd.find_element(By.NAME, 'edit').click()
        # fill group form
        self.fill_group_form(new_group_data)
        # submit modification
        wd.find_element(By.NAME, 'update').click()
        self.return_to_groups_page()
        self.group_cashe = None

    def return_to_groups_page(self):
        wd = self.app.wd
        wd.find_element(By.LINK_TEXT, 'group page').click()

    def count(self):
        wd = self.app.wd
        self.open_groups_page()
        return len(wd.find_elements(By.NAME, 'selected[]'))

    group_cashe = None

    def get_group_list(self):
        if self.group_cashe is None:
            wd = self.app.wd
            self.open_groups_page()
            self.group_cashe = []
            for element in wd.find_elements(By.CSS_SELECTOR, 'span.group'):
                text = element.text
                group_id = element.find_element(By.NAME, 'selected[]').get_attribute('value')
                self.group_cashe.append(Group(name=text, id=group_id))
        return list(self.group_cashe)
