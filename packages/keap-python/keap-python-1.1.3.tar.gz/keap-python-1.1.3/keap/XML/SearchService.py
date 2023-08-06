from keap.XML import BaseService


class SearchService(BaseService):
    def __init__(self, keap):
        super().__init__(keap)

    def get_search_report(self, savedSearchId, userId, pageNumber):
        return self.call("getSavedSearchResultsAllFields", savedSearchId, userId, pageNumber)