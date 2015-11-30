from crudbuilder.abstract import BaseCrudBuilder


class TestModelCrud(BaseCrudBuilder):
    search_feilds = ['name']
    tables2_fields = ('name', 'email')
    tables2_css_class = "table table-bordered table-condensed"
    tables2_pagination = 20  # default is 10
    modelform_excludes = ['created_by']
