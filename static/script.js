let currentQuestionIndex = parseInt(localStorage.getItem('currentQuestionIndex')) || 0; // Get stored index or start from 0
let responses = JSON.parse(localStorage.getItem('responses')) || []; // Get stored responses or start with empty array

const formId = window.location.pathname.split('/')[2];
let questions = [];

// Load questions from the backend
async function loadQuestions() {
    try {
        const response = await fetch('/api/questions');
        const data = await response.json();
        console.log('Fetched questions:', data); // Debug log
        questions = data;
        renderQuestion();
    } catch (error) {
        console.error('Error loading questions:', error);
    }
}

// Render the current question
function renderQuestion() {
    const question = questions[currentQuestionIndex];
    const questionContainer = document.getElementById('question-container');
    questionContainer.innerHTML = '';

    const questionElement = document.createElement('div');
    questionElement.classList.add('bg-gray-50', 'p-4', 'rounded-lg', 'shadow', 'border', 'border-gray-200', 'mb-6');

    const questionTitle = document.createElement('h3');
    questionTitle.textContent = `Question ${currentQuestionIndex + 1}: ${question.question}`;
    questionTitle.classList.add('font-semibold', 'text-lg', 'mb-4');
    questionElement.appendChild(questionTitle);

    question.choices.forEach((choice) => {
        const choiceLabel = document.createElement('label');
        choiceLabel.classList.add('block', 'cursor-pointer', 'p-2', 'rounded', 'hover:bg-blue-100', 'mb-2');

        const choiceInput = document.createElement('input');
        choiceInput.type = 'radio';
        choiceInput.name = `question${currentQuestionIndex}`;
        choiceInput.value = choice;
        choiceInput.classList.add('mr-2');

        choiceLabel.appendChild(choiceInput);
        choiceLabel.appendChild(document.createTextNode(choice));
        questionElement.appendChild(choiceLabel);
    });

    questionContainer.appendChild(questionElement);

    // Enable Next button if an answer is selected
    const nextButton = document.getElementById('next-button');
    nextButton.disabled = true;

    // Add event listener to enable "Next" button when an option is selected
    document.querySelectorAll(`input[name="question${currentQuestionIndex}"]`).forEach((input) => {
        input.addEventListener('change', () => {
            nextButton.disabled = false;
        });
    });

    // Next button click handler
    nextButton.onclick = () => {
        // Store response when moving to the next question
        const selectedOption = document.querySelector(`input[name="question${currentQuestionIndex}"]:checked`);
        if (selectedOption) {
            responses[currentQuestionIndex] = selectedOption.value;
        }

        // Store progress in localStorage
        localStorage.setItem('currentQuestionIndex', currentQuestionIndex);
        localStorage.setItem('responses', JSON.stringify(responses));

        if (currentQuestionIndex < questions.length - 1) {
            currentQuestionIndex++;
            renderQuestion();
        } else {
            showFinalFeedbackForm();
        }
    };
}

// Show the final feedback form
function showFinalFeedbackForm() {
    // Hide quiz question and show feedback form
    document.getElementById('question-container').innerHTML = '';
    document.getElementById('final-feedback').classList.remove('hidden');
    document.getElementById('next-button').classList.add('hidden');
}

// Submit feedback
document.getElementById('submit-feedback')?.addEventListener('click', async () => {
    const finalFeedbackText = document.getElementById('final-feedback-text').value;
    if (finalFeedbackText.trim()) {
        responses.push(finalFeedbackText);  // Add final feedback to responses

        // Send data to the server for storing in CSV
        try {
            const response = await fetch('/api/feedback', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ responses, finalFeedback: finalFeedbackText, formId }),
            });

            const data = await response.json();
            console.log('Feedback submitted:', data.message);
        } catch (error) {
            console.error('Error submitting feedback:', error);
        }
    }

    showThankYouMessage();
});

// Show thank you message after feedback submission
function showThankYouMessage() {
    document.getElementById('final-feedback').classList.add('hidden');
    document.getElementById('thank-you-message').classList.remove('hidden');

    // Clear localStorage after submission
    localStorage.removeItem('currentQuestionIndex');
    localStorage.removeItem('responses');
}

loadQuestions().catch(error => console.error('Error loading questions:', error));
