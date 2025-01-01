import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load the pre-trained language model (replace with your preferred model)
model_name = "gpt2"  # Example: gpt2, gpt-j-6B 
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def generate_quiz_question(text):
    """
    Generates a quiz question and answer options using a language model.

    Args:
        text: The text to generate the quiz from.

    Returns:
        A dictionary containing the question, options, and correct answer.
    """
    prompt = f"""
    **Instructions:** 

    1. **Create a multiple-choice quiz question** based on the following text: 
       "{text}"

    2. **Ensure:**
       - The question is relevant to the provided text.
       - There are **four** answer options (including one correct answer).
       - The answer options are plausible and not easily distinguishable as incorrect.

    3. **Output the question and answer options in the following format:**
       **Question:** <question_text>
       **Options:**
           - <option_1>
           - <option_2>
           - <option_3>
           - <option_4>
       **Correct Answer:** <correct_answer>

    **Example:**

    **Instructions:** 

    1. **Create a multiple-choice quiz question** based on the following text: 
       "The quick brown fox jumps over the lazy dog."

    2. **Ensure:** 
       - ... (as above)

    3. **Output the question and answer options in the following format:**
       **Question:** What is the subject of the sentence?
       **Options:**
           - dog
           - fox
           - brown
           - jumps
       **Correct Answer:** fox

    **Now, generate the quiz question based on the provided text:** 
    """

    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    outputs = model.generate(input_ids, max_length=256, do_sample=True, top_p=0.9, top_k=50)
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Extract question, options, and answer from the generated text
    # (Implement robust parsing logic based on the expected output format)
    try:
        question = generated_text.split("**Question:** ")[1].split("**Options:**")[0].strip()
        options_str = generated_text.split("**Options:** ")[1].split("**Correct Answer:**")[0].strip()
        options = [option.strip() for option in options_str.split("-")]
        answer = generated_text.split("**Correct Answer:** ")[1].strip()
    except IndexError:
        print("Error parsing generated text. Please refine the prompt or try again.")
        return None

    return {"question": question, "options": options, "answer": answer}

def display_quiz(questions):
    """
    Displays the quiz on the Streamlit app.

    Args:
        questions: A list of dictionaries representing the quiz questions.
    """
    st.title("AI-Generated Quiz")

    for i, question in enumerate(questions):
        st.write(f"**Question {i+1}:** {question['question']}")
        selected_option = st.radio("Select your answer:", question["options"])
        st.write("---")

        if selected_option == question["answer"]:
            st.success("Correct!")
        else:
            st.error("Incorrect")

if __name__ == "__main__":
    text = """
    ‘Make 2025 New Beginning, Not as World Divided but as Nations United,’ 
    Secretary-General Urges in New Year Message
    Following is the text of UN Secretary-General António Guterres’ New Year video 
    message for 2025:
    Throughout 2024, hope has been hard to find.  Wars are causing enormous pain, 
    suffering and displacement.  Inequalities and divisions are rife — fuelling 
    tensions and mistrust. 
    And today I can officially report that we have just endured a decade of deadly 
    heat.  The top ten 10 hottest years on record have happened in the last 10 years, 
    including 2024.  This is climate breakdown — in real time.  We must exit this road 
    to ruin — and we have no time to lose. 
    In 2025, countries must put the world on a safer path by dramatically slashing 
    emissions and supporting the transition to a renewable future.  It is essential — 
    and it is possible. 
    Even in the darkest days, I’ve seen hope power change.  I see hope in activists — 
    young and old — raising their voices for progress.  I see hope in the humanitarian 
    heroes overcoming enormous obstacles to support the most vulnerable people.  I see 
    hope in developing countries fighting for financial and climate justice.  I see 
    hope in the scientists and innovators breaking new ground for humanity.  And I 
    saw hope in September, when world leaders came together to adopt the Pact for 
    the Future. 
    The Pact is a new push to build peace through disarmament and prevention.  To 
    reform the global financial system so it supports and represents all countries.  To 
    push for more opportunities for women and young people.  To build guardrails so 
    technologies put people over profits and rights over runaway algorithms.  And 
    always, to stick to the values and principles enshrined by human rights, 
    international law and the United Nations Charter. 
    There are no guarantees for what’s ahead in 2025.  But I pledge to stand with 
    all those who are working to forge a more peaceful, equal, stable and healthy 
    future for all people.  Together, we can make 2025 a new beginning.  Not as a 
    world divided.  But as nations united.
    """

    num_questions = 4  # Adjust as needed
    questions = []
    for _ in range(num_questions):
        question_data = generate_quiz_question(text)
        if question_data:
            questions.append(question_data)

    if questions:
        display_quiz(questions)
    else:
        st.error("Failed to generate quiz questions. Please try again later.")
