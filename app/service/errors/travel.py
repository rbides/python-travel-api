class TravelNotFoundException(Exception):

    def __init__(self, detail: str = "Travel not found."):
        self.detail = detail
