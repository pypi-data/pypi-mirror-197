================
TODO
================

- [ ] Add a testing framework using LLM's as testers
- [ ] Add unit testing for each module and integrations tests
- [ ] Add CI/CD before pushing to master
- [ ] Create a pipeline object to chain modules together (black box it)
- [ ] Add visualization
    - [ ] Add visualization for pipeline creation with injected resources
    - [ ] Inspect modules and resources during execution
    - [ ] Add a way to save and load pipelines
    - [ ] Compile the code to a single file
    - [ ] Sell as a service
- [ ] Add module caching with vector databases for nlp
- [ ] Add top level caching (caching the general state)


==============
How to build
==============
pip install -r requirements.txt

`python setup.py sdist bdist_wheel`

twine upload dist/*

twine upload -u 'kael558' -p 'A6C4Yh@uMuwrsdg' --repository-url https://upload.pypi.org/legacy/ dist/*

pip install --index-url "https://test.pypi.org/simple/<package_name>"





================
How to use
================

Resource
----------
Defines interfaces for resources that can be used by the pipeline.
.. code-block:: python

    @resource(name="TextGenerator")
    class LLMTextGenerator(ABC):
        @abstractmethod
        def complete(self, prompt: str) -> str:
            return True

    class OpenAITextGenerator(ABC):
        def __init__(self, api_key: str):
            openai.api_key = api_key

        def complete(self, prompt: str) -> str:
            return openai.Completion.create(
                engine="davinci",
                prompt=prompt,
                temperature=0.9,
                max_tokens=150,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0.6,
                stop=["\n", " Human:", " AI:"],
            )


Module
-----------
Transformers will transform the data in some way.
.. code-block:: python

    @module(name="LowerCase")
    def lowercase(input: str):
        return input.lower()

They can use resources:
.. code-block:: python

    @module(name="OpenAI")
    def openai(input: str, resource: OpenAITextGenerator):
        return resource.complete(input)

Control
---------
Control modules will redirect the flow of logic.

.. code-block:: python

    @control(name="hasFinalAnswer")
    def final_answer(input: str):

        if "Final Answer" in input:
            return 1
        else:
            return 2







