@component(icon="👤")
class Persona(Block):
    """👤 Who the product serves — an empathy map: name, role, goal, frustrations, a quote; says, thinks, does, feels."""
    kept_in = Attr(str, column="save")      # the learner's file it is read from, and 💾 kept in
    source  = Attr("Form")                  # the form whose fields it reads, when it has no fence of its own

    @source.getter
    def source(self):
        return _lc_ref(self, "data-bind")

    @property
    def data(self):
        return _lc_doc_data(self)
