import cognite
import unittest

class Testprompts(unittest.TestCase):
    def test_PromptTemplate(self):
        template = cognite.prompts.template.PromptTemplate('prompts/chatgpt.yaml')
        prompt = template(input='hello world', history=[("a", "b")])
        
    # def test_PromptTemplate_standard(self):
    #     template = cognite.prompts.template.PromptTemplate('prompts/template.yaml')
    #     # template.show()
    #     prompt = template(input1='hello', input2='world')
    #     print(prompt)
    
    # def test_PromptTemplate_with_default(self):
    #     template = cognite.prompts.template.PromptTemplate('prompts/template.yaml')
    #     # template.show()
    #     prompt = template(input1='world')
    #     print(prompt)

if __name__ == '__main__':
    unittest.main()