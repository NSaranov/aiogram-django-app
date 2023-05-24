import datetime
import json
import re

from atlassian import Jira

from .models import JRUser, JRParentTask, JRTemplateCreateTask, JRTask
from .specifications import EmailQASUsers, CustomFieldsNameJira, LabelsIssueJira


class Service():
    # @sync_to_async()
    def __init__(self):
        pass

    @classmethod
    async def acreate(cls) -> object:
        try:
            self = Service()
            self.src_jira_browse = 'https://jira.sdvor.com/browse/'
            self.issue_transitions = {
                "backlog": "11",
                "in_progress": "31",
                "done": "41",
                "to_do": "51",
                "in_testing": "61"
            }
            self.issue_priority = {
                "Highest": "1",
                "High": "2",
                "Medium": "3",
            }
            user = await JRUser.aget_auth_data(email="svc_jirabot@sdvor.com")
            self.base_url = user.get('base_url', None)
            self.parent_task = await JRParentTask.aget_parent_task(key='QAS-1000')
            self.template_new_task = await JRTemplateCreateTask.aget_template_task(key_parent_task='QAS-1000')
            if self.base_url is None or self.parent_task is None or self.template_new_task is None:
                self.jira = None
            else:
                self.jira = Jira(
                    url=user["base_url"],
                    username=user["atlassian_email"],
                    token=user["atlassian_token"],
                    cloud=True
                )
            return self
        except Exception as ex_create_issue:
            print("Exception Create Issue = ", ex_create_issue)

    @staticmethod
    async def add_task_to_db(
            id: int,
            key: str,
            project_key: str | None,
            parent_key: str | None,
            summary: str | None,
            text: str | None,
            issuetype_name: str | None,
            link: str | None,
            label: str | None,
            date_time: datetime,
    ) -> {(JRTask, bool)}:
        return await JRTask.objects.aget_or_create(
            id=id,
            key=key,
            project_key=project_key,
            parent_key=parent_key,
            summary=summary,
            text=text,
            issuetype_name=issuetype_name,
            link=link,
            label=label,
            date_time=date_time,
        )

# Tasks QAS-1000
    def get_keys_project_and_issue(self, str_includes_keys: str):
        text = str_includes_keys.strip()
        regex = str(r'^([A-Z]{3,})([\s]{,1})(-)([\s]{,1})([0-9]{1,})(.*)$')
        template_replace = str(r'{"project_key":"\1","issue_key":"\1\3\5"}')
        match_value = re.search(regex, text)
        result = match_value.expand(template_replace) if match_value else None
        project_key = None
        issue_key = None
        if result is not None:
            keys = json.loads(result)
            project_key = keys['project_key'] if keys else None
            issue_key = keys['issue_key'] if keys else None
        return project_key, issue_key

    def define_transition_and_labels(self,
                                     fields_subtask: dict | None,
                                     fields_task: dict | None):
        """
         Для jira.sdvor.com/rest/api/2/issue/
        { "priority": { "id": "?" } }:       Приоритет задачи
           "3"    - Medium
           "2"    - High
           "1"    - Highest
        { "customfield_10014": "QAS-1000" }:  Ключ Epic-задачи
        """

        c_done = self.issue_transitions['done']
        c_in_testing = self.issue_transitions['in_testing']
        c_backlog = self.issue_transitions['backlog']
        c_highest = "1"
        c_high = "2"
        c_epic_key_review_tasks = 'QAS-1000'

        if fields_subtask is None or fields_task is None:
            return None, None
        if fields_task.get(CustomFieldsNameJira['epic_key'], None) == c_epic_key_review_tasks and \
                fields_subtask['reporter']['emailAddress'] in EmailQASUsers:
            if fields_subtask['priority']['id'] in [c_highest, c_high]:
                return None, {"labels": [LabelsIssueJira['req_deblock']]}
            else:
                return c_done, {"labels": [LabelsIssueJira['issue_autoclosed']]}
        else:
            return None, None

    def get_transiton_and_labels_qas(self, descr_req):
        transition = None
        labels = None
        task_key = None
        structure_task = None
        structure_subtask = None
        jira = self.jira
        # Обработка полей Формирование transition  задачи
        project_key, subtask_key = self.get_keys_project_and_issue(descr_req)
        if project_key == 'QAS':
            try:
                structure_subtask = jira.issue(subtask_key) if subtask_key else None
            except Exception as ex_get_issue:
                print("Exception Get Issue = ", ex_get_issue)
                return transition, labels, subtask_key, task_key

            if 'fields' in structure_subtask:
                structure_subtask = structure_subtask['fields']
                if 'parent' in structure_subtask:
                    task_key = structure_subtask['parent']['key'] \
                        if structure_subtask['parent'] else None

            if task_key is not None:
                structure_task = jira.issue(task_key)
                structure_task = structure_task['fields']

            transition, labels = self.define_transition_and_labels(structure_subtask,
                                                                   structure_task)
        return transition, labels, subtask_key, task_key

    async def create_issue_jira_to_QAS_1000(self, new_task, descr_req, reviewer_req, date_time, request):
        if new_task is None or self.jira is None:
            return
        jira = self.jira
        # Формирование статуса задачи

        transition, labels, subtask_key, task_key = self.get_transiton_and_labels_qas(descr_req)

        if reviewer_req == '':
            value_reviever = None
        else:
            value_reviever = reviewer_req
        # Формирования структуры полей новой задачи
        request_body = {
            "project": {
                "key": self.parent_task["project_key"]
            },
            "customfield_10014": self.parent_task["key"],

            "summary": new_task["summary"],
            "description": new_task["description"],
            "issuetype": {
                "id": self.parent_task["issuetype_name_child"]
            },

        }

        # CustomFieldsNameJira['epic_key']: self.parent_task["key"],
        # CustomFieldsNameJira['sap_req_reviewer']: reviewer_req,

        # Создание новой задачи
        try:
            resp_new_task = None
            resp_new_task = jira.create_issue(fields=request_body)
        except Exception as ex_create_issue:
            print("Exception Create Issue = ", ex_create_issue)

        # Добавляю номер запроса
        try:
            resp_add_request_to_field = None
            resp_add_request_to_field = self.jira.update_issue_field(resp_new_task['key'], {"customfield_10500": request})
            is_request_to_field = True
        except Exception as ex_add_request_to_field:
            print("Exception Add Request To Field Exemption Issues = ", ex_add_request_to_field)

        if resp_new_task is not None:

            # Установка состояния для новой задачи, и задач с которыми она связана
            return_transition = None
            if transition is not None:
                try:
                    resp_status_new_task = None
                    resp_status_task = None
                    resp_status_subtask = None
                    resp_status_new_task = jira.set_issue_status_by_transition_id(resp_new_task['key'], transition)
                    resp_status_task = jira.set_issue_status_by_transition_id(task_key, transition)
                    resp_status_subtask = jira.set_issue_status_by_transition_id(subtask_key, transition)
                    return_transition = get_key(self.issue_transitions, transition)
                except Exception as ex_set_status:
                    print("Exception Set Issues Status = ", ex_set_status)
            # Установка метки для задач с которыми связана новой задача
            return_label = None
            if labels is not None:
                try:
                    resp_status_new_task = None
                    resp_status_task = None
                    resp_status_subtask = None
                    resp_status_new_task = jira.update_issue_field(resp_new_task['key'], labels)
                    resp_status_task = jira.update_issue_field(task_key, labels)
                    resp_status_subtask = jira.update_issue_field(subtask_key, labels)
                    return_label = labels['labels'][0]
                except Exception as ex_set_labels:
                    print("Exception Set Issues Labels = ", ex_set_labels)

            await Service().add_task_to_db(
                id=resp_new_task['id'],
                key=resp_new_task['key'],
                project_key=self.parent_task['project_key'],
                parent_key=self.parent_task['key'],
                summary=new_task['summary'],
                text=descr_req,
                issuetype_name=self.parent_task['issuetype_name_child'],
                link=resp_new_task['self'],
                label=self.template_new_task['id_label__label'],
                date_time=date_time)

            return self.parent_task['key'], \
                   resp_new_task['key'], \
                   self.src_jira_browse + resp_new_task['key'], \
                   return_label, \
                   return_transition
        return None, None, None

    async def get_summary_descr_text(self, data_sap_req, date_time):
        numb_req = data_sap_req['numb']
        descr_req = data_sap_req['descr']
        type_req = data_sap_req['type']
        owner_req = data_sap_req['owner']
        reviewer_req = data_sap_req['reviewer'] if data_sap_req['reviewer'] else " "
        date_lock = str(date_time.now().strftime('%d.%m.%Y'))
        static_txt = {
            "summary_pref": "QA",
            "numb_req": "*Номер запроса:* ",
            "descr_req": "*Описание:* ",
            "type_req": "*Тип:* ",
            "owner_req": "*Владелец:* ",
            "reviewer_req": "*Рецензент:* ",
            "date_lock": "*Дата деблокирования:* ",
        }
        # Описание
        content_descr_part_1 = '{0}{1}\n{2}{3}\n'.format(static_txt["descr_req"], descr_req,
                                                         static_txt["numb_req"], numb_req)
        content_descr_part_2 = '{0}{1}\n{2}{3}\n'.format(static_txt["owner_req"], owner_req,
                                                         static_txt["reviewer_req"], reviewer_req)
        content_descr_part_3 = '{0}{1}\n{2}{3}'.format(static_txt["type_req"], type_req,
                                                       static_txt["date_lock"], date_lock)
        content_descr = content_descr_part_1 + content_descr_part_2 + content_descr_part_3
        # Тема и описание задачи
        summary_descr_txt = {
            "summary": "[{}] {} - {}".format(static_txt["summary_pref"], numb_req, descr_req),
            "description": content_descr
        }
        return summary_descr_txt

# Old Tasks QAS-1000
    async def get_tasks_for_close(self, days_ago_value: int):
        jira = self.jira
        # JQL выражение
        jql_request = 'issuekey in childIssuesOf("QAS-1000") and ' \
                      'updatedDate < startOfDay(-' + str(days_ago_value) + 'd) and ' \
                      'status in ("In Progress", "IN TESTING", Backlog, "To Do") ' \
                      'ORDER BY key ASC'
        try:
            resp_get_tasks = None
            resp_get_tasks = self.jira.jql(jql_request)
        except Exception as ex_get_jql:
            print("Exception JQL Get Old Issue = ", ex_get_jql)
        return resp_get_tasks

    async def close_tasks(self, in_list_tasks):
        labels = {'labels': [LabelsIssueJira['issue_closed_due_to_obsolescence']]}
        list_link = []
        issue_count = 0
        if in_list_tasks.get('issues', None) is not None:
            for structure_fields in in_list_tasks['issues']:
                # Изменяю состояние
                is_set_transition = False
                if structure_fields.get('key', None) is not None:
                    try:
                        resp_change_status = None
                        resp_change_status = self.jira.set_issue_status_by_transition_id(structure_fields['key'],
                                                                                         self.issue_transitions['done'])
                        is_set_transition = True
                    except Exception as ex_set_status:
                        print("Exception Change Issues Status = ", ex_set_status)
                # Устанавливаю комментарий
                if is_set_transition:
                    try:
                        resp_add_labels = self.jira.update_issue_field(structure_fields['key'], labels)
                    except Exception as ex_add_labels:
                        print("Exception Add Issues Labels = ", ex_add_labels)
                    # Добавляю в лист ссылок закрытых задач
                    issue_count = issue_count + 1
                    list_link.append({
                        'link': self.src_jira_browse + structure_fields['key'],
                        'priority': get_key(self.issue_priority, structure_fields['fields']['priority']['id'])
                    })
        return issue_count, list_link

# Tasks Exemption
    async def find_task_exemption(self, request):
        jql_request = 'issuekey in childIssuesOf("QAS-3010") AND ' \
                      '"Transport Request " ~ "' + str(request) + '"'
        task = None
        try:
            resp_get_tasks = None
            resp_get_tasks = self.jira.jql(jql_request)
            if resp_get_tasks.get('issues', None) is not None:
                for structure_fields in resp_get_tasks['issues']:
                    return structure_fields
        except Exception as ex_get_jql:
            print("Exception JQL Get Exemption Issue = ", ex_get_jql)
        return task

    async def create_task_exemption(self, request, email, summary_dict, text):
        key_epic_exemption = 'QAS-3010'
        request_body = {
            "project": {
                "key": self.parent_task["project_key"]
            },
            "customfield_10014": key_epic_exemption,
            "summary": summary_dict["summary"],
            "issuetype": {
                "id": self.parent_task["issuetype_name_child"]
            },
        }

        # Создание новой задачи
        try:
            resp_new_task = None
            resp_new_task = self.jira.create_issue(fields=request_body)
        except Exception as ex_create_issue:
            print("Exception Create Exemption Issue = ", ex_create_issue)

        issue_key = resp_new_task.get('key', None)

        # Добавляю комментарий
        try:
            resp_add_comment = None
            resp_add_comment = self.jira.issue_add_comment(issue_key, text)
        except Exception as ex_add_comment:
            print("Exception JQL Add Comment to Exemption Issue = ", ex_add_comment)

        # Добавляю наблюдающих
        is_email_not_correct = False
        if email == '':
            is_email_empty = True
        else:
            is_email_empty = False
        list_watchers = []
        list_watchers.extend(EmailQASUsers)
        list_watchers.append(email)
        for watcher in list_watchers:
            try:
                resp_add_watcher = None
                resp_add_watcher = self.jira.issue_add_watcher(issue_key, watcher)
            except Exception as ex_add_watcher:
                print("Exception Add Watchers To Exemption Issues = ", ex_add_watcher)
                is_email_not_correct = True

        # Добавляю номер запроса
        try:
            resp_add_request_to_field = None
            resp_add_request_to_field = self.jira.update_issue_field(issue_key, {"customfield_10500": request })
            is_request_to_field = True
        except Exception as ex_add_request_to_field:
            print("Exception Add Request To Field Exemption Issues = ", ex_add_request_to_field)

        return issue_key, self.src_jira_browse + issue_key, True, is_email_empty, is_email_not_correct

    async def modify_task_exemption(self, task, email, text):
        issue_key = task.get('key', None)
        # Добавляю комментарий
        try:
            resp_add_comment = None
            resp_add_comment = self.jira.issue_add_comment(issue_key, text)
        except Exception as ex_add_comment:
            print("Exception JQL Add Comment to Exemption Issue = ", ex_add_comment)

        try:
            resp_change_status = None
            resp_change_status = self.jira.set_issue_status_by_transition_id( issue_key, self.issue_transitions['to_do'])
            is_set_transition = True
        except Exception as ex_set_status:
            print("Exception Change Exemption Issues Status = ", ex_set_status)

        return issue_key, self.src_jira_browse + issue_key, False

# Tasks Alarm
    async def find_task_alarm(self, table, code_place):
        jql_request = 'issuekey in childIssuesOf("QAS-736") and ' \
                      '"Table" ~ "' + str(table) + '" and '\
                      '"Code place" ~ "' + str(code_place) + '"'
        task = None
        try:
            resp_get_tasks = None
            resp_get_tasks = self.jira.jql(jql_request)
            if resp_get_tasks.get('issues', None) is not None:
                for structure_fields in resp_get_tasks['issues']:
                    return structure_fields
        except Exception as ex_get_jql:
            print("Exception JQL Get Alarm Issue = ", ex_get_jql)
        return task

    async def create_task_alarm(self, table, code_place, summary_dict, comment):
        key_epic_alarm = 'QAS-736'
        request_body = {
            "project": {
                "key": self.parent_task["project_key"]
            },
            "customfield_10014": key_epic_alarm,
            "summary": summary_dict["summary"],
            "issuetype": {
                "id": self.parent_task["issuetype_name_child"]
            },
        }

        # Создание новой задачи
        try:
            resp_new_task = None
            resp_new_task = self.jira.create_issue(fields=request_body)
        except Exception as ex_create_issue:
            print("Exception Create Alarm Issue = ", ex_create_issue)

        issue_key = resp_new_task.get('key', None)

        # Добавляю комментарий
        try:
            resp_add_comment = None
            resp_add_comment = self.jira.issue_add_comment(issue_key, comment)
        except Exception as ex_add_comment:
            print("Exception JQL Add Comment to Alarm Issue = ", ex_add_comment)

        # Добавляю наблюдающих
        list_watchers = []
        list_watchers.extend(EmailQASUsers)
        for watcher in list_watchers:
            try:
                resp_add_watcher = None
                resp_add_watcher = self.jira.issue_add_watcher(issue_key, watcher)
            except Exception as ex_add_watcher:
                print("Exception Add Watchers To Alarm Issues = ", ex_add_watcher)

        # Добавляю номер запроса
        try:
            resp_add_request_to_field = None
            resp_add_request_to_field = self.jira.update_issue_field(issue_key, {"customfield_10502": table,
                                                                                 "customfield_10503": code_place })
            is_request_to_field = True
        except Exception as ex_add_request_to_field:
            print("Exception Add Request To Field Alarm Issues = ", ex_add_request_to_field)
        return issue_key, self.src_jira_browse + issue_key, True

    async def modify_task_alarm(self, task, table, code_place, comment):
        issue_key = task.get('key', None)
        # Добавляю комментарий
        try:
            resp_add_comment = None
            resp_add_comment = self.jira.issue_add_comment(issue_key, comment)
        except Exception as ex_add_comment:
            print("Exception JQL Add Comment to Alarm Issue = ", ex_add_comment)
        # Изменяем статус
        try:
            resp_change_status = None
            resp_change_status = self.jira.set_issue_status_by_transition_id( issue_key, self.issue_transitions['to_do'])
            is_set_transition = True
        except Exception as ex_set_status:
            print("Exception Change Exemption Issues Status = ", ex_set_status)

        return issue_key, self.src_jira_browse + issue_key, False

def get_key(in_dict: dict, in_value: str | int):
    for key, value in in_dict.items():
        if value == in_value:
            return key
