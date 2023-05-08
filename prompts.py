from langchain import PromptTemplate

is_x_jewish_prompt = PromptTemplate(
    input_variables=["name"],
    template="Is {name} ethnically Jewish?"
)

is_x_jewish_half_or_more_prompt = PromptTemplate(
    input_variables=["name"],
    template="Is {name} ethnically Jewish? Note, that an individual is considered Jewish if they are ethnically Jewish or if they are ethnically White and have at least one Jewish parent."
)

podcast_guest_list = PromptTemplate(
    input_variables=["show_name", "number"],
    template="Generate a list, in chronological order, of the {number} most recent guests on the {show_name} podcast."
)

get_ethnicity_simple = PromptTemplate(
    input_variables=["name"],
    template="What is the ethnicity of {name}? Categorize them to the best of your ability into one of the following: White, Jewish, Black, Asian, Hispanic, Other, or Unknown."
)


get_ethnicity = PromptTemplate(
    input_variables=["name"],
    template="What is the ethnicity of {name}? Categorize them to the best of your ability into one of the following: White, Jewish, Black, Asian, Hispanic, Other, or Unknown. Only respond with one word, the persons ethnicity category. If the individual is ethnically Jewish, please categorize them as Jewish and not White. If the individual is half Jewish, or has at least one Jewish parent, also classify them as Jewish. If the individual has only one Jewish grandparent and the rest of their grandparents are not Jewish, they should be classified as White. If you can't determine an individuals ethnicity, please categorize them as Unknown."
)

get_nationality = PromptTemplate(
    input_variables=["name"],
    template="What is the nationality of {name}?"
)
