class TestCriteria:

    def __init__(self, name, criteria):
        self.name = name
        self.criteria = criteria
        self.evaluated = False
        self.passed = False

    def evaluate(self, args):
        self.evaluated = True
        self.passed = self.criteria(args)        
        return self.passed

    def passed(self):
        return self.passed
    
    def is_evaluated(self):
        return self.evaluated

    def get_name(self):
        return self.name

class TestReport:

    def __init__(self, request = None):
        self.request = request
        self.criterias = []
        self.first_criteria_to_fail = None
        self.passed_criteria = 0
        self.response = None
        self.in_progress = True
        self.approved = False

    def add_criteria(self, name, criteria):
        self.criterias.append(TestCriteria(name, criteria))

    def set_response(self, response):
        self.response = response

    def evaluate(self):
        
        if self.in_progress:

            result = True
            self.passed_criteria = 0

            for criteria in self.criterias:
            
                curr = criteria.evaluate(self.response)
                result = result and curr

                if curr:
                    self.passed_criteria += 1
                else:
                    self.first_criteria_to_fail = criteria
                    break

            self.approved = result
            self.in_progress = False
        
        return self.approved

    def is_in_progress(self):
        return self.in_progress
    
    def is_accepted(self):
        return self.approved

    def get_first_criteria_to_fail(self):
        return self.first_criteria_to_fail

    def get_passed_criterias(self):
        return self.passed_criteria

    def get_total_criterias(self):
        return len(self.criterias)
    
    def get_request(self):
        return self.request

    def get_response(self):
        return self.response