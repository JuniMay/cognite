import cognite
import unittest

class Testprompts(unittest.TestCase):

    def test_PromptTemplate_standard(self):
        template = cognite.prompts.template.PromptTemplate('cognite/prompts/template.yaml')
        # template.show()
        prompt = template.get_prompt(input1='hello', input2='world')
        print(prompt)
    
    def test_PromptTemplate_with_default(self):
        template = cognite.prompts.template.PromptTemplate('cognite/prompts/template.yaml')
        # template.show()
        prompt = template.get_prompt(input1='world')
        print(prompt)
    
    def test_PromptTemplate_without_sufficient_input(self):
        template = cognite.prompts.template.PromptTemplate('cognite/prompts/template.yaml')
        # template.show()
        prompt = template.get_prompt()
        print(prompt)

if __name__ == '__main__':
    unittest.main()