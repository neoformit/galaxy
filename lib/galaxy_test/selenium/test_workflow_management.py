from .framework import (
    EXAMPLE_WORKFLOW_URL_1,
    retry_assertion_during_transitions,
    selenium_test,
    SeleniumTestCase,
    UsesWorkflowAssertions,
)


class WorkflowManagementTestCase(SeleniumTestCase, UsesWorkflowAssertions):

    ensure_registered = True

    @selenium_test
    def test_import_from_url(self):
        self.workflow_index_open()
        self._workflow_import_from_url()

        table_elements = self.workflow_index_table_elements()
        assert len(table_elements) == 1

        new_workflow = table_elements[0].find_element_by_css_selector(".workflow-dropdown")
        assert "TestWorkflow1 (imported from URL)" in new_workflow.text, new_workflow.text

    @selenium_test
    def test_view(self):
        self.workflow_index_open()
        self._workflow_import_from_url()
        self.workflow_index_click_option("View external link")
        assert self.driver.current_url == EXAMPLE_WORKFLOW_URL_1
        self.driver.back()
        self.components.workflows.external_link.wait_for_visible()
        # font-awesome title handling broken... https://github.com/FortAwesome/vue-fontawesome/issues/63
        # title_element = external_link_icon.find_element_by_tag_name("title")
        # assert EXAMPLE_WORKFLOW_URL_1 in title_element.text
        self.workflow_index_click_option("View")
        workflow_show = self.components.workflow_show
        title_item = self.components.workflow_show.title.wait_for_visible()
        assert "TestWorkflow1" in title_item.text
        annotation_item = workflow_show.annotation.wait_for_visible()
        assert "simple workflow" in annotation_item.text
        self.screenshot("workflow_manage_view")
        # TODO: Test display of steps...

    @selenium_test
    def test_rename(self):
        self.workflow_index_open()
        self._workflow_import_from_url()
        self.workflow_index_rename("CoolNewName")

        @retry_assertion_during_transitions
        def check_name():
            name = self.workflow_index_name()
            assert "CoolNewName" == name, name

        check_name()

    @selenium_test
    def test_download(self):
        self.workflow_index_open()
        self._workflow_import_from_url()
        # TODO: fill this test out - getting downloaded files in general through Selenium is a bit tough,
        # going through the motions though should catch a couple potential problems.
        self.workflow_index_click_option("Download")

    @selenium_test
    def test_tagging(self):
        self.workflow_index_open()
        self._workflow_import_from_url()

        self.workflow_index_click_tag_display()
        self.tagging_add(["cooltag"])

        @retry_assertion_during_transitions
        def check_tags():
            self.assertEqual(self.workflow_index_tags(), ["cooltag"])

        check_tags()
        self.screenshot("workflow_manage_tags")

    @selenium_test
    def test_index_search(self):
        self.workflow_index_open()
        self._workflow_import_from_url()
        self.workflow_index_rename("searchforthis")
        self._assert_showing_n_workflows(1)
        self.screenshot("workflow_manage_search")

        self.workflow_index_search_for("doesnotmatch")
        self._assert_showing_n_workflows(0)

        self.workflow_index_search_for()
        self._assert_showing_n_workflows(1)

        self.workflow_index_search_for("searchforthis")
        self._assert_showing_n_workflows(1)
