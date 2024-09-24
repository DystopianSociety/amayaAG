from query_data import query_rag
from langchain_community.llms.ollama import Ollama

EVAL_PROMPT = """
Réponse attendue : {expected_response}
Réponse réelle : {actual_response}
---
(Répondez par 'vrai' ou 'faux') La réponse réelle correspond-elle à la réponse attendue ? 
"""


def test_query_one():
    assert query_and_validate(
        question="Quels sont les principaux défis auxquels Amaya Ag doit faire face pour améliorer la vie des petits exploitants agricoles, et comment la plateforme s'y prend-elle pour les surmonter?",
        expected_response="""Les missions d'Amaya Ag sont multiples et visent toutes à améliorer la vie des petits
exploitants agricoles. En augmentant la production grâce à des intrants et des conseils
de qualité, Amaya aide les agriculteurs à obtenir de meilleurs rendements. La
plateforme travaille également à élargir l'accès aux marchés, en certifiant les produits
pour leur ouvrir des opportunités locales et internationales. En outre, Amaya se
concentre sur la gestion des risques en offrant des assurances et des conseils
personnalisés, permettant aux agriculteurs de faire face plus efficacement aux défis
climatiques et sanitaires""",
    )


def test_query_two():
    assert query_and_validate(
        question="Quels sont les principaux obstacles que les petits exploitants agricoles doivent surmonter pour améliorer leur productivité et leur accès aux marchés, et quelles solutions pourraient être mises en place pour atténuer l'impact du changement climatique et améliorer leur accès au crédit et aux ressources?",
        expected_response="""L'agriculture est un secteur vital confronté à divers défis. La productivité des petits
exploitants agricoles reste souvent faible en raison de méthodes traditionnelles et d'un
accès limité à des technologies modernes. De plus, l'accès aux marchés est un
obstacle majeur pour de nombreux agriculteurs, réduisant leurs opportunités de vente
et de profit. Le changement climatique aggrave ces difficultés en rendant les conditions
de culture imprévisibles et souvent défavorables. En outre, le manque de ressources
comme les semences, les engrais et les équipements entrave la croissance agricole.
Enfin, les problèmes financiers sont omniprésents : les banques considèrent souvent
les petits agriculteurs comme des emprunteurs à haut risque, ce qui limite leur accès au
crédit nécessaire pour investir dans leurs exploitations.""",
    )


def query_and_validate(question: str, expected_response: str):
    response_text = query_rag(question)
    prompt = EVAL_PROMPT.format(
        expected_response=expected_response, actual_response=response_text
    )

    model = Ollama(model="mistral")
    evaluation_results_str = model.invoke(prompt)
    evaluation_results_str_cleaned = evaluation_results_str.strip().lower()

    print(prompt)

    if "vrai" in evaluation_results_str_cleaned:
        # Print response in Green if it is correct.
        print("\033[92m" + f"Response: {evaluation_results_str_cleaned}" + "\033[0m")
        return True
    elif "faux" in evaluation_results_str_cleaned:
        # Print response in Red if it is incorrect.
        print("\033[91m" + f"Response: {evaluation_results_str_cleaned}" + "\033[0m")
        return False
    else:
        raise ValueError(
            f"Invalid evaluation result. Cannot determine if 'true' or 'false'."
        )